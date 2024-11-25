import os
import gc
import re
import sys
import torch
import torch.nn.functional as F
import torchcrepe
import faiss
import librosa
import numpy as np
from scipy import signal
from torch import Tensor

now_dir = os.getcwd()
sys.path.append(now_dir)

from rvc.lib.predictors.RMVPE import RMVPE0Predictor
from rvc.lib.predictors.FCPE import FCPEF0Predictor

import logging

logging.getLogger("faiss").setLevel(logging.WARNING)

# Constants for high-pass filter
FILTER_ORDER = 5
CUTOFF_FREQUENCY = 48  # Hz
SAMPLE_RATE = 16000  # Hz
bh, ah = signal.butter(
    N=FILTER_ORDER, Wn=CUTOFF_FREQUENCY, btype="high", fs=SAMPLE_RATE
)

input_audio_path2wav = {}


class AudioProcessor:
    """
    A class for processing audio signals, specifically for adjusting RMS levels.
    """

    def change_rms(
        source_audio: np.ndarray,
        source_rate: int,
        target_audio: np.ndarray,
        target_rate: int,
        rate: float,
    ) -> np.ndarray:
        """
        Adjust the RMS level of target_audio to match the RMS of source_audio, with a given blending rate.

        Args:
            source_audio: The source audio signal as a NumPy array.
            source_rate: The sampling rate of the source audio.
            target_audio: The target audio signal to adjust.
            target_rate: The sampling rate of the target audio.
            rate: The blending rate between the source and target RMS levels.
        """
        # Calculate RMS of both audio data
        rms1 = librosa.feature.rms(
            y=source_audio,
            frame_length=source_rate // 2 * 2,
            hop_length=source_rate // 2,
        )
        rms2 = librosa.feature.rms(
            y=target_audio,
            frame_length=target_rate // 2 * 2,
            hop_length=target_rate // 2,
        )

        # Interpolate RMS to match target audio length
        rms1 = F.interpolate(
            torch.from_numpy(rms1).float().unsqueeze(0),
            size=target_audio.shape[0],
            mode="linear",
        ).squeeze()
        rms2 = F.interpolate(
            torch.from_numpy(rms2).float().unsqueeze(0),
            size=target_audio.shape[0],
            mode="linear",
        ).squeeze()
        rms2 = torch.maximum(rms2, torch.zeros_like(rms2) + 1e-6)

        # Adjust target audio RMS based on the source audio RMS
        adjusted_audio = (
            target_audio
            * (torch.pow(rms1, 1 - rate) * torch.pow(rms2, rate - 1)).numpy()
        )
        return adjusted_audio


class Autotune:
    """
    A class for applying autotune to a given fundamental frequency (F0) contour.
    """

    def __init__(self, ref_freqs):
        """
        Initializes the Autotune class with a set of reference frequencies.

        Args:
            ref_freqs: A list of reference frequencies representing musical notes.
        """
        self.ref_freqs = ref_freqs
        self.note_dict = self.ref_freqs  # No interpolation needed

    def autotune_f0(self, f0, f0_autotune_strength):
        """
        Autotunes a given F0 contour by snapping each frequency to the closest reference frequency.

        Args:
            f0: The input F0 contour as a NumPy array.
        """
        autotuned_f0 = np.zeros_like(f0)
        for i, freq in enumerate(f0):
            closest_note = min(self.note_dict, key=lambda x: abs(x - freq))
            autotuned_f0[i] = freq + (closest_note - freq) * f0_autotune_strength
        return autotuned_f0


class Pipeline:
    """
    The main pipeline class for performing voice conversion, including preprocessing, F0 estimation,
    voice conversion using a model, and post-processing.
    """

    def __init__(self, tgt_sr, config):
        """
        Initializes the Pipeline class with target sampling rate and configuration parameters.

        Args:
            tgt_sr: The target sampling rate for the output audio.
            config: A configuration object containing various parameters for the pipeline.
        """
        self.x_pad = config.x_pad
        self.x_query = config.x_query
        self.x_center = config.x_center
        self.x_max = config.x_max
        self.is_half = config.is_half
        self.sample_rate = 16000
        self.window = 160
        self.t_pad = self.sample_rate * self.x_pad
        self.t_pad_tgt = tgt_sr * self.x_pad
        self.t_pad2 = self.t_pad * 2
        self.t_query = self.sample_rate * self.x_query
        self.t_center = self.sample_rate * self.x_center
        self.t_max = self.sample_rate * self.x_max
        self.time_step = self.window / self.sample_rate * 1000
        self.f0_min = 50
        self.f0_max = 1100
        self.f0_mel_min = 1127 * np.log(1 + self.f0_min / 700)
        self.f0_mel_max = 1127 * np.log(1 + self.f0_max / 700)
        self.device = config.device
        self.ref_freqs = [
            49.00,  # G1
            51.91,  # G#1 / Ab1
            55.00,  # A1
            58.27,  # A#1 / Bb1
            61.74,  # B1
            65.41,  # C2
            69.30,  # C#2 / Db2
            73.42,  # D2
            77.78,  # D#2 / Eb2
            82.41,  # E2
            87.31,  # F2
            92.50,  # F#2 / Gb2
            98.00,  # G2
            103.83,  # G#2 / Ab2
            110.00,  # A2
            116.54,  # A#2 / Bb2
            123.47,  # B2
            130.81,  # C3
            138.59,  # C#3 / Db3
            146.83,  # D3
            155.56,  # D#3 / Eb3
            164.81,  # E3
            174.61,  # F3
            185.00,  # F#3 / Gb3
            196.00,  # G3
            207.65,  # G#3 / Ab3
            220.00,  # A3
            233.08,  # A#3 / Bb3
            246.94,  # B3
            261.63,  # C4
            277.18,  # C#4 / Db4
            293.66,  # D4
            311.13,  # D#4 / Eb4
            329.63,  # E4
            349.23,  # F4
            369.99,  # F#4 / Gb4
            392.00,  # G4
            415.30,  # G#4 / Ab4
            440.00,  # A4
            466.16,  # A#4 / Bb4
            493.88,  # B4
            523.25,  # C5
            554.37,  # C#5 / Db5
            587.33,  # D5
            622.25,  # D#5 / Eb5
            659.25,  # E5
            698.46,  # F5
            739.99,  # F#5 / Gb5
            783.99,  # G5
            830.61,  # G#5 / Ab5
            880.00,  # A5
            932.33,  # A#5 / Bb5
            987.77,  # B5
            1046.50,  # C6
        ]
        self.autotune = Autotune(self.ref_freqs)
        self.note_dict = self.autotune.note_dict
        self.model_rmvpe = RMVPE0Predictor(
            os.path.join("rvc", "models", "predictors", "rmvpe.pt"),
            is_half=self.is_half,
            device=self.device,
        )

    def get_f0_crepe(
        self,
        x,
        f0_min,
        f0_max,
        p_len,
        hop_length,
        model="full",
    ):
        """
        Estimates the fundamental frequency (F0) of a given audio signal using the Crepe model.

        Args:
            x: The input audio signal as a NumPy array.
            f0_min: Minimum F0 value to consider.
            f0_max: Maximum F0 value to consider.
            p_len: Desired length of the F0 output.
            hop_length: Hop length for the Crepe model.
            model: Crepe model size to use ("full" or "tiny").
        """
        x = x.astype(np.float32)
        x /= np.quantile(np.abs(x), 0.999)
        audio = torch.from_numpy(x).to(self.device, copy=True)
        audio = torch.unsqueeze(audio, dim=0)
        if audio.ndim == 2 and audio.shape[0] > 1:
            audio = torch.mean(audio, dim=0, keepdim=True).detach()
        audio = audio.detach()
        pitch: Tensor = torchcrepe.predict(
            audio,
            self.sample_rate,
            hop_length,
            f0_min,
            f0_max,
            model,
            batch_size=hop_length * 2,
            device=self.device,
            pad=True,
        )
        p_len = p_len or x.shape[0] // hop_length
        source = np.array(pitch.squeeze(0).cpu().float().numpy())
        source[source < 0.001] = np.nan
        target = np.interp(
            np.arange(0, len(source) * p_len, len(source)) / p_len,
            np.arange(0, len(source)),
            source,
        )
        f0 = np.nan_to_num(target)
        return f0

    def get_f0_hybrid(
        self,
        methods_str,
        x,
        f0_min,
        f0_max,
        p_len,
        hop_length,
    ):
        """
        Estimates the fundamental frequency (F0) using a hybrid approach combining multiple methods.

        Args:
            methods_str: A string specifying the methods to combine (e.g., "hybrid[crepe+rmvpe]").
            x: The input audio signal as a NumPy array.
            f0_min: Minimum F0 value to consider.
            f0_max: Maximum F0 value to consider.
            p_len: Desired length of the F0 output.
            hop_length: Hop length for F0 estimation methods.
        """
        methods_str = re.search("hybrid\[(.+)\]", methods_str)
        if methods_str:
            methods = [method.strip() for method in methods_str.group(1).split("+")]
        f0_computation_stack = []
        print(f"Calculating f0 pitch estimations for methods {str(methods)}")
        x = x.astype(np.float32)
        x /= np.quantile(np.abs(x), 0.999)
        for method in methods:
            f0 = None
            if method == "crepe":
                f0 = self.get_f0_crepe_computation(
                    x, f0_min, f0_max, p_len, int(hop_length)
                )
            elif method == "rmvpe":
                f0 = self.model_rmvpe.infer_from_audio(x, thred=0.03)
                f0 = f0[1:]
            elif method == "fcpe":
                self.model_fcpe = FCPEF0Predictor(
                    os.path.join("rvc", "models", "predictors", "fcpe.pt"),
                    f0_min=int(f0_min),
                    f0_max=int(f0_max),
                    dtype=torch.float32,
                    device=self.device,
                    sample_rate=self.sample_rate,
                    threshold=0.03,
                )
                f0 = self.model_fcpe.compute_f0(x, p_len=p_len)
                del self.model_fcpe
                gc.collect()
            f0_computation_stack.append(f0)

        f0_computation_stack = [fc for fc in f0_computation_stack if fc is not None]
        f0_median_hybrid = None
        if len(f0_computation_stack) == 1:
            f0_median_hybrid = f0_computation_stack[0]
        else:
            f0_median_hybrid = np.nanmedian(f0_computation_stack, axis=0)
        return f0_median_hybrid

    def get_f0(
        self,
        input_audio_path,
        x,
        p_len,
        pitch,
        f0_method,
        filter_radius,
        hop_length,
        f0_autotune,
        f0_autotune_strength,
        inp_f0=None,
    ):
        """
        Estimates the fundamental frequency (F0) of a given audio signal using various methods.

        Args:
            input_audio_path: Path to the input audio file.
            x: The input audio signal as a NumPy array.
            p_len: Desired length of the F0 output.
            pitch: Key to adjust the pitch of the F0 contour.
            f0_method: Method to use for F0 estimation (e.g., "crepe").
            filter_radius: Radius for median filtering the F0 contour.
            hop_length: Hop length for F0 estimation methods.
            f0_autotune: Whether to apply autotune to the F0 contour.
            inp_f0: Optional input F0 contour to use instead of estimating.
        """
        global input_audio_path2wav
        if f0_method == "crepe":
            f0 = self.get_f0_crepe(x, self.f0_min, self.f0_max, p_len, int(hop_length))
        elif f0_method == "crepe-tiny":
            f0 = self.get_f0_crepe(
                x, self.f0_min, self.f0_max, p_len, int(hop_length), "tiny"
            )
        elif f0_method == "rmvpe":
            f0 = self.model_rmvpe.infer_from_audio(x, thred=0.03)
        elif f0_method == "fcpe":
            self.model_fcpe = FCPEF0Predictor(
                os.path.join("rvc", "models", "predictors", "fcpe.pt"),
                f0_min=int(self.f0_min),
                f0_max=int(self.f0_max),
                dtype=torch.float32,
                device=self.device,
                sample_rate=self.sample_rate,
                threshold=0.03,
            )
            f0 = self.model_fcpe.compute_f0(x, p_len=p_len)
            del self.model_fcpe
            gc.collect()
        elif "hybrid" in f0_method:
            input_audio_path2wav[input_audio_path] = x.astype(np.double)
            f0 = self.get_f0_hybrid(
                f0_method,
                x,
                self.f0_min,
                self.f0_max,
                p_len,
                hop_length,
            )

        if f0_autotune is True:
            f0 = Autotune.autotune_f0(self, f0, f0_autotune_strength)

        f0 *= pow(2, pitch / 12)
        tf0 = self.sample_rate // self.window
        if inp_f0 is not None:
            delta_t = np.round(
                (inp_f0[:, 0].max() - inp_f0[:, 0].min()) * tf0 + 1
            ).astype("int16")
            replace_f0 = np.interp(
                list(range(delta_t)), inp_f0[:, 0] * 100, inp_f0[:, 1]
            )
            shape = f0[self.x_pad * tf0 : self.x_pad * tf0 + len(replace_f0)].shape[0]
            f0[self.x_pad * tf0 : self.x_pad * tf0 + len(replace_f0)] = replace_f0[
                :shape
            ]
        f0bak = f0.copy()
        f0_mel = 1127 * np.log(1 + f0 / 700)
        f0_mel[f0_mel > 0] = (f0_mel[f0_mel > 0] - self.f0_mel_min) * 254 / (
            self.f0_mel_max - self.f0_mel_min
        ) + 1
        f0_mel[f0_mel <= 1] = 1
        f0_mel[f0_mel > 255] = 255
        f0_coarse = np.rint(f0_mel).astype(np.int_)

        return f0_coarse, f0bak

    def voice_conversion(
        self,
        model,
        net_g,
        sid,
        audio0,
        pitch,
        pitchf,
        index,
        big_npy,
        index_rate,
        version,
        protect,
    ):
        """
        Performs voice conversion on a given audio segment.

        Args:
            model: The feature extractor model.
            net_g: The generative model for synthesizing speech.
            sid: Speaker ID for the target voice.
            audio0: The input audio segment.
            pitch: Quantized F0 contour for pitch guidance.
            pitchf: Original F0 contour for pitch guidance.
            index: FAISS index for speaker embedding retrieval.
            big_npy: Speaker embeddings stored in a NumPy array.
            index_rate: Blending rate for speaker embedding retrieval.
            version: Model version ("v1" or "v2").
            protect: Protection level for preserving the original pitch.
        """
        with torch.no_grad():
            pitch_guidance = pitch != None and pitchf != None
            # prepare source audio
            feats = (
                torch.from_numpy(audio0).half()
                if self.is_half
                else torch.from_numpy(audio0).float()
            )
            feats = feats.mean(-1) if feats.dim() == 2 else feats
            assert feats.dim() == 1, feats.dim()
            feats = feats.view(1, -1).to(self.device)
            # extract features
            feats = model(feats)["last_hidden_state"]
            feats = (
                model.final_proj(feats[0]).unsqueeze(0) if version == "v1" else feats
            )
            # make a copy for pitch guidance and protection
            feats0 = feats.clone() if pitch_guidance else None
            if (
                index
            ):  # set by parent function, only true if index is available, loaded, and index rate > 0
                feats = self._retrieve_speaker_embeddings(
                    feats, index, big_npy, index_rate
                )
            # feature upsampling
            feats = F.interpolate(feats.permute(0, 2, 1), scale_factor=2).permute(
                0, 2, 1
            )
            # adjust the length if the audio is short
            p_len = min(audio0.shape[0] // self.window, feats.shape[1])
            if pitch_guidance:
                feats0 = F.interpolate(feats0.permute(0, 2, 1), scale_factor=2).permute(
                    0, 2, 1
                )
                pitch, pitchf = pitch[:, :p_len], pitchf[:, :p_len]
                # Pitch protection blending
                if protect < 0.5:
                    pitchff = pitchf.clone()
                    pitchff[pitchf > 0] = 1
                    pitchff[pitchf < 1] = protect
                    feats = feats * pitchff.unsqueeze(-1) + feats0 * (
                        1 - pitchff.unsqueeze(-1)
                    )
                    feats = feats.to(feats0.dtype)
            else:
                pitch, pitchf = None, None
            p_len = torch.tensor([p_len], device=self.device).long()
            audio1 = (
                (net_g.infer(feats, p_len, pitch, pitchf, sid)[0][0, 0])
                .data.cpu()
                .float()
                .numpy()
            )
            # clean up
            del feats, feats0, p_len
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        return audio1

    def _retrieve_speaker_embeddings(self, feats, index, big_npy, index_rate):
        npy = feats[0].cpu().numpy()
        npy = npy.astype("float32") if self.is_half else npy
        score, ix = index.search(npy, k=8)
        weight = np.square(1 / score)
        weight /= weight.sum(axis=1, keepdims=True)
        npy = np.sum(big_npy[ix] * np.expand_dims(weight, axis=2), axis=1)
        npy = npy.astype("float16") if self.is_half else npy
        feats = (
            torch.from_numpy(npy).unsqueeze(0).to(self.device) * index_rate
            + (1 - index_rate) * feats
        )
        return feats

    def pipeline(
        self,
        model,
        net_g,
        sid,
        audio,
        pitch,
        f0_method,
        file_index,
        index_rate,
        pitch_guidance,
        filter_radius,
        volume_envelope,
        version,
        protect,
        hop_length,
        f0_autotune,
        f0_autotune_strength,
        f0_file,
    ):
        """
        The main pipeline function for performing voice conversion.

        Args:
            model: The feature extractor model.
            net_g: The generative model for synthesizing speech.
            sid: Speaker ID for the target voice.
            audio: The input audio signal.
            input_audio_path: Path to the input audio file.
            pitch: Key to adjust the pitch of the F0 contour.
            f0_method: Method to use for F0 estimation.
            file_index: Path to the FAISS index file for speaker embedding retrieval.
            index_rate: Blending rate for speaker embedding retrieval.
            pitch_guidance: Whether to use pitch guidance during voice conversion.
            filter_radius: Radius for median filtering the F0 contour.
            tgt_sr: Target sampling rate for the output audio.
            resample_sr: Resampling rate for the output audio.
            volume_envelope: Blending rate for adjusting the RMS level of the output audio.
            version: Model version.
            protect: Protection level for preserving the original pitch.
            hop_length: Hop length for F0 estimation methods.
            f0_autotune: Whether to apply autotune to the F0 contour.
            f0_file: Path to a file containing an F0 contour to use.
        """
        if file_index != "" and os.path.exists(file_index) and index_rate > 0:
            try:
                index = faiss.read_index(file_index)
                big_npy = index.reconstruct_n(0, index.ntotal)
            except Exception as error:
                print(f"An error occurred reading the FAISS index: {error}")
                index = big_npy = None
        else:
            index = big_npy = None
        audio = signal.filtfilt(bh, ah, audio)
        audio_pad = np.pad(audio, (self.window // 2, self.window // 2), mode="reflect")
        opt_ts = []
        if audio_pad.shape[0] > self.t_max:
            audio_sum = np.zeros_like(audio)
            for i in range(self.window):
                audio_sum += audio_pad[i : i - self.window]
            for t in range(self.t_center, audio.shape[0], self.t_center):
                opt_ts.append(
                    t
                    - self.t_query
                    + np.where(
                        np.abs(audio_sum[t - self.t_query : t + self.t_query])
                        == np.abs(audio_sum[t - self.t_query : t + self.t_query]).min()
                    )[0][0]
                )
        s = 0
        audio_opt = []
        t = None
        audio_pad = np.pad(audio, (self.t_pad, self.t_pad), mode="reflect")
        p_len = audio_pad.shape[0] // self.window
        inp_f0 = None
        if hasattr(f0_file, "name"):
            try:
                with open(f0_file.name, "r") as f:
                    lines = f.read().strip("\n").split("\n")
                inp_f0 = []
                for line in lines:
                    inp_f0.append([float(i) for i in line.split(",")])
                inp_f0 = np.array(inp_f0, dtype="float32")
            except Exception as error:
                print(f"An error occurred reading the F0 file: {error}")
        sid = torch.tensor(sid, device=self.device).unsqueeze(0).long()
        if pitch_guidance:
            pitch, pitchf = self.get_f0(
                "input_audio_path",  # questionable purpose of making a key for an array
                audio_pad,
                p_len,
                pitch,
                f0_method,
                filter_radius,
                hop_length,
                f0_autotune,
                f0_autotune_strength,
                inp_f0,
            )
            pitch = pitch[:p_len]
            pitchf = pitchf[:p_len]
            if self.device == "mps":
                pitchf = pitchf.astype(np.float32)
            pitch = torch.tensor(pitch, device=self.device).unsqueeze(0).long()
            pitchf = torch.tensor(pitchf, device=self.device).unsqueeze(0).float()
        for t in opt_ts:
            t = t // self.window * self.window
            if pitch_guidance:
                audio_opt.append(
                    self.voice_conversion(
                        model,
                        net_g,
                        sid,
                        audio_pad[s : t + self.t_pad2 + self.window],
                        pitch[:, s // self.window : (t + self.t_pad2) // self.window],
                        pitchf[:, s // self.window : (t + self.t_pad2) // self.window],
                        index,
                        big_npy,
                        index_rate,
                        version,
                        protect,
                    )[self.t_pad_tgt : -self.t_pad_tgt]
                )
            else:
                audio_opt.append(
                    self.voice_conversion(
                        model,
                        net_g,
                        sid,
                        audio_pad[s : t + self.t_pad2 + self.window],
                        None,
                        None,
                        index,
                        big_npy,
                        index_rate,
                        version,
                        protect,
                    )[self.t_pad_tgt : -self.t_pad_tgt]
                )
            s = t
        if pitch_guidance:
            audio_opt.append(
                self.voice_conversion(
                    model,
                    net_g,
                    sid,
                    audio_pad[t:],
                    pitch[:, t // self.window :] if t is not None else pitch,
                    pitchf[:, t // self.window :] if t is not None else pitchf,
                    index,
                    big_npy,
                    index_rate,
                    version,
                    protect,
                )[self.t_pad_tgt : -self.t_pad_tgt]
            )
        else:
            audio_opt.append(
                self.voice_conversion(
                    model,
                    net_g,
                    sid,
                    audio_pad[t:],
                    None,
                    None,
                    index,
                    big_npy,
                    index_rate,
                    version,
                    protect,
                )[self.t_pad_tgt : -self.t_pad_tgt]
            )
        audio_opt = np.concatenate(audio_opt)
        if volume_envelope != 1:
            audio_opt = AudioProcessor.change_rms(
                audio, self.sample_rate, audio_opt, self.sample_rate, volume_envelope
            )
        # if resample_sr >= self.sample_rate and tgt_sr != resample_sr:
        #    audio_opt = librosa.resample(
        #        audio_opt, orig_sr=tgt_sr, target_sr=resample_sr
        #    )
        # audio_max = np.abs(audio_opt).max() / 0.99
        # max_int16 = 32768
        # if audio_max > 1:
        #    max_int16 /= audio_max
        # audio_opt = (audio_opt * 32768).astype(np.int16)
        audio_max = np.abs(audio_opt).max() / 0.99
        if audio_max > 1:
            audio_opt /= audio_max
        if pitch_guidance:
            del pitch, pitchf
        del sid
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        return audio_opt
