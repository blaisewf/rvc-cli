import ffmpeg
import numpy as np


def load_audio(file, sr, do_formant=False, quefrency=1.0, timbre=1.0):
    try:
        file = file.strip(" ").strip('"').strip("\n").strip('"').strip(" ")
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="f32le", acodec="pcm_f32le", ac=1, ar=sr)
            .run(cmd=["ffmpeg", "-nostdin"], capture_stdout=True, capture_stderr=True)
        )
    except Exception as error:
        raise RuntimeError(f"Failed to load audio: {error}")

    return np.frombuffer(out, np.float32).flatten()
