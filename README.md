## RVC_CLI: Retrieval-based Voice Conversion Command Line Interface

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blaise-tk/rvc_cli/blob/master/RVC_CLI.ipynb)

### Todo

- [ ] Improve the efficiency of prerequisite download to avoid running it every time `main.py` is executed.
- [ ] Resolve issues with Google Colab (missing some updates)

### Table of Contents

1. [Installation](#installation)
   - [Windows](#windows)
   - [Linux](#linux)
2. [Getting Started](#getting-started)
   - [Inference](#inference)
   - [Training](#training)
   - [Additional Features](#additional-features)
3. [API](#api)
4. [Credits](#credits)

### Installation

Ensure that you have the necessary Python packages installed by following these steps (Python 3.9 is recommended):

#### Windows

Execute the [install.bat](./install.bat) file to activate a Conda environment. Afterward, launch the application using `env/python main.py` instead of the conventional `python main.py` command.

#### Linux

```bash
chmod +x install.sh
./install.sh
```

### Getting Started

For detailed information and command-line options, refer to the help command:

```bash
python main.py -h
```

This command provides a clear overview of the available modes and their corresponding parameters, facilitating effective utilization of the RVC CLI.

### Inference

#### Single Inference

```bash
python main.py infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_path "input_path" --output_path "output_path" --pth_path "pth_path" --index_path "index_path" --split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength" --export_format "export_format"
```

| Parameter Name   | Required | Default | Valid Options                                                                                                                           | Description                                                                                                                                                                                                                                                                                                           |
| ---------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `f0up_key`       | No       | 0       | -24 to +24                                                                                                                              | Set the pitch of the audio, the higher the value, thehigher the pitch.                                                                                                                                                                                                                                                |
| `filter_radius`  | No       | 3       | 0 to 10                                                                                                                                 | If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.                                                                                                                                                                  |
| `index_rate`     | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.                                                                                                                                              |
| `hop_length`     | No       | 128     | 1 to 512                                                                                                                                | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.                                                                                                                                |
| `rms_mix_rate`   | No       | 1       | 0 to 1                                                                                                                                  | Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.                                                                                                                                                                                   |
| `protect`        | No       | 0.33    | 0 to 0.5                                                                                                                                | Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect. |
| `f0autotune`     | No       | False   | True or False                                                                                                                           | Apply a soft autotune to your inferences, recommended for singing conversions.                                                                                                                                                                                                                                        |
| `f0method`       | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                                                                                                                                                      |
| `input_path`     | Yes      |         | Full path to the input audio file                                                                                                       | Full path to the input audio file                                                                                                                                                                                                                                                                                     |
| `output_path`    | Yes      |         | Full path to the output audio file                                                                                                      | Full path to the output audio file                                                                                                                                                                                                                                                                                    |
| `pth_path`       | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file                                                                                                                                                                                                                                                                                             |
| `index_path`     | Yes      |         | Full index file path                                                                                                                    | Full index file path                                                                                                                                                                                                                                                                                                  |
| `split_audio`    | No       | False   | True or False                                                                                                                           | Split the audio into chunks for inference to obtain better results in some cases.                                                                                                                                                                                                                                     |
| `clean_audio`    | No       | False   | True or False                                                                                                                           | Clean your audio output using noise detection algorithms, recommended for speaking audios.                                                                                                                                                                                                                            |
| `clean_strength` | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.                                                                                                                                                          |
| `export_format`  | No       | WAV     | WAV, MP3, FLAC, OGG, M4A                                                                                                                | File audio format                                                                                                                                                                                                                                                                                                     |

_Refer to `python main.py infer -h` for additional help._

#### Batch Inference

```bash
python main.py batch_infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_folder_path "input_folder_path" --output_folder_path "output_folder_path" --pth_path "pth_path" --index_path "index_path" --split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength" --export_format "export_format"
```

| Parameter Name       | Required | Default | Valid Options                                                                                                                           | Description                                                                                                                                                                                                                                                                                                           |
| -------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `f0up_key`           | No       | 0       | -24 to +24                                                                                                                              | Set the pitch of the audio, the higher the value, thehigher the pitch.                                                                                                                                                                                                                                                |
| `filter_radius`      | No       | 3       | 0 to 10                                                                                                                                 | If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.                                                                                                                                                                  |
| `index_rate`         | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.                                                                                                                                              |
| `hop_length`         | No       | 128     | 1 to 512                                                                                                                                | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.                                                                                                                                |
| `rms_mix_rate`       | No       | 1       | 0 to 1                                                                                                                                  | Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.                                                                                                                                                                                   |
| `protect`            | No       | 0.33    | 0 to 0.5                                                                                                                                | Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect. |
| `f0autotune`         | No       | False   | True or False                                                                                                                           | Apply a soft autotune to your inferences, recommended for singing conversions.                                                                                                                                                                                                                                        |
| `f0method`           | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                                                                                                                                                      |
| `input_folder_path`  | Yes      |         | Full path to the input audio folder (The folder may only contain audio files)                                                           | Full path to the input audio folder                                                                                                                                                                                                                                                                                   |
| `output_folder_path` | Yes      |         | Full path to the output audio folder                                                                                                    | Full path to the output audio folder                                                                                                                                                                                                                                                                                  |
| `pth_path`           | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file                                                                                                                                                                                                                                                                                             |
| `index_path`         | Yes      |         | Full path to the index file                                                                                                             | Full path to the index file                                                                                                                                                                                                                                                                                           |
| `split_audio`        | No       | False   | True or False                                                                                                                           | Split the audio into chunks for inference to obtain better results in some cases.                                                                                                                                                                                                                                     |
| `clean_audio`        | No       | False   | True or False                                                                                                                           | Clean your audio output using noise detection algorithms, recommended for speaking audios.                                                                                                                                                                                                                            |
| `clean_strength`     | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.                                                                                                                                                          |
| `export_format`      | No       | WAV     | WAV, MP3, FLAC, OGG, M4A                                                                                                                | File audio format                                                                                                                                                                                                                                                                                                     |

_Refer to `python main.py batch_infer -h` for additional help._

#### TTS Inference

```bash
python main.py tts_infer --tts_text "tts_text" --tts_voice "tts_voice" --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --output_tts_path "output_tts_path" --output_rvc_path "output_rvc_path" --pth_path "pth_path" --index_path "index_path"--split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength" --export_format "export_format"
```

| Parameter Name    | Required | Default | Valid Options                                                                                                                           | Description                                                                                                                                                                                                                                                                                                           |
| ----------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `tts_text`        | Yes      |         | Text for TTS synthesis                                                                                                                  | Text for TTS synthesis                                                                                                                                                                                                                                                                                                |
| `tts_voice`       | Yes      |         | Voice for TTS synthesis                                                                                                                 | Voice for TTS synthesis                                                                                                                                                                                                                                                                                               |
| `f0up_key`        | No       | 0       | -24 to +24                                                                                                                              | Set the pitch of the audio, the higher the value, thehigher the pitch.                                                                                                                                                                                                                                                |
| `filter_radius`   | No       | 3       | 0 to 10                                                                                                                                 | If the number is greater than or equal to three, employing median filtering on the collected tone results has the potential to decrease respiration.                                                                                                                                                                  |
| `index_rate`      | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Influence exerted by the index file; a higher value corresponds to greater influence. However, opting for lower values can help mitigate artifacts present in the audio.                                                                                                                                              |
| `hop_length`      | No       | 128     | 1 to 512                                                                                                                                | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy.                                                                                                                                |
| `rms_mix_rate`    | No       | 1       | 0 to 1                                                                                                                                  | Substitute or blend with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is employed.                                                                                                                                                                                   |
| `protect`         | No       | 0.33    | 0 to 0.5                                                                                                                                | Safeguard distinct consonants and breathing sounds to prevent electro-acoustic tearing and other artifacts. Pulling the parameter to its maximum value of 0.5 offers comprehensive protection. However, reducing this value might decrease the extent of protection while potentially mitigating the indexing effect. |
| `f0autotune`      | No       | False   | True or False                                                                                                                           | Apply a soft autotune to your inferences, recommended for singing conversions.                                                                                                                                                                                                                                        |
| `f0method`        | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                                                                                                                                                      |
| `output_tts_path` | Yes      |         | Full path to the output TTS audio file                                                                                                  | Full path to the output TTS audio file                                                                                                                                                                                                                                                                                |
| `output_rvc_path` | Yes      |         | Full path to the input RVC audio file                                                                                                   | Full path to the input RVC audio file                                                                                                                                                                                                                                                                                 |
| `pth_path`        | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file                                                                                                                                                                                                                                                                                             |
| `index_path`      | Yes      |         | Full path to the index file                                                                                                             | Full path to the index file                                                                                                                                                                                                                                                                                           |
| `split_audio`     | No       | False   | True or False                                                                                                                           | Split the audio into chunks for inference to obtain better results in some cases.                                                                                                                                                                                                                                     |
| `clean_audio`     | No       | False   | True or False                                                                                                                           | Clean your audio output using noise detection algorithms, recommended for speaking audios.                                                                                                                                                                                                                            |
| `clean_strength`  | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Set the clean-up level to the audio you want, the more you increase it the more it will clean up, but it is possible that the audio will be more compressed.                                                                                                                                                          |
| `export_format`   | No       | WAV     | WAV, MP3, FLAC, OGG, M4A                                                                                                                | File audio format                                                                                                                                                                                                                                                                                                     |

_Refer to `python main.py tts_infer -h` for additional help._

### Training

#### Preprocess Dataset

```bash
python main.py preprocess --model_name "model_name" --dataset_path "dataset_path" --sampling_rate "sampling_rate"
```

| Parameter Name  | Required | Default | Valid Options                                                             | Description                     |
| --------------- | -------- | ------- | ------------------------------------------------------------------------- | ------------------------------- |
| `model_name`    | Yes      |         | Name of the model                                                         | Name of the model               |
| `dataset_path`  | Yes      |         | Full path to the dataset folder (The folder may only contain audio files) | Full path to the dataset folder |
| `sampling_rate` | Yes      |         | 32000, 40000, or 48000                                                    | Sampling rate of the audio data |

_Refer to `python main.py preprocess -h` for additional help._

#### Extract Features

```bash
python main.py extract --model_name "model_name" --rvc_version "rvc_version" --f0method "f0method" --hop_length "hop_length" --sampling_rate "sampling_rate"
```

| Parameter Name  | Required | Default | Valid Options                              | Description                                                                                                                                                                            |
| --------------- | -------- | ------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_name`    | Yes      |         | Name of the model                          | Name of the model                                                                                                                                                                      |
| `rvc_version`   | No       | v2      | v1 or v2                                   | Version of the model                                                                                                                                                                   |
| `f0method`      | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe | Pitch extraction algorithm to use for the audio conversion. The default algorithm is rmvpe, which is recommended for most cases.                                                       |
| `hop_length`    | No       | 128     | 1 to 512                                   | Denotes the duration it takes for the system to transition to a significant pitch change. Smaller hop lengths require more time for inference but tend to yield higher pitch accuracy. |
| `sampling_rate` | Yes      |         | 32000, 40000, or 48000                     | Sampling rate of the audio data                                                                                                                                                        |

#### Start Training

```bash
python main.py train --model_name "model_name" --rvc_version "rvc_version" --save_every_epoch "save_every_epoch" --save_only_latest "save_only_latest" --save_every_weights "save_every_weights" --total_epoch "total_epoch" --sampling_rate "sampling_rate" --batch_size "batch_size" --gpu "gpu" --pitch_guidance "pitch_guidance" --pretrained "pretrained" --custom_pretrained "custom_pretrained" [--g_pretrained "g_pretrained"] [--d_pretrained "d_pretrained"]
```

| Parameter Name       | Required | Default | Valid Options                                                           | Description                                                                                                                                                                                                                                                     |
| -------------------- | -------- | ------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_name`         | Yes      |         | Name of the model                                                       | Name of the model                                                                                                                                                                                                                                               |
| `rvc_version`        | No       | v2      | v1 or v2                                                                | Version of the model                                                                                                                                                                                                                                            |
| `save_every_epoch`   | Yes      |         | 1 to 50                                                                 | Determine at how many epochs the model will saved at.                                                                                                                                                                                                           |
| checkpoint           |
| `save_only_latest`   | No       | False   | True or False                                                           | Enabling this setting will result in the G and D files saving only their most recent versions, effectively conserving storage space.                                                                                                                            |
|                      |
| `save_every_weights` | No       | True    | True or False                                                           | This setting enables you to save the weights of the model at the conclusion of each epoch.                                                                                                                                                                      |
|                      |
| `total_epoch`        | No       | 1000    | 1 to 10000                                                              | Specifies the overall quantity of epochs for the model training process.                                                                                                                                                                                        |
|                      |
| `sampling_rate`      | Yes      |         | 32000, 40000, or 48000                                                  | Sampling rate of the audio data                                                                                                                                                                                                                                 |
| `batch_size`         | No       | 8       | 1 to 50                                                                 | It's advisable to align it with the available VRAM of your GPU. A setting of 4 offers improved accuracy but slower processing, while 8 provides faster and standard results.                                                                                    |
| `gpu`                | No       | 0       | 0 to ∞ separated by -                                                   | Specify the number of GPUs you wish to utilize for training by entering them separated by hyphens (-).                                                                                                                                                          |
|                      |
| `pitch_guidance`     | No       | True    | True or False                                                           | By employing pitch guidance, it becomes feasible to mirror the intonation of the original voice, including its pitch. This feature is particularly valuable for singing and other scenarios where preserving the original melody or pitch pattern is essential. |
|                      |
| `pretrained`         | No       | True    | True or False                                                           | Utilize pretrained models when training your own. This approach reduces training duration and enhances overall quality.                                                                                                                                         |
|                      |
| `custom_pretrained`  | No       | False   | True or False                                                           | Utilizing custom pretrained models can lead to superior results, as selecting the most suitable pretrained models tailored to the specific use case can significantly enhance performance.                                                                      |
| models               |
| `g_pretrained`       | No       | None    | Full path to pretrained file G, only if you have used custom_pretrained | Full path to pretrained file G                                                                                                                                                                                                                                  |
| `d_pretrained`       | No       | None    | Full path to pretrained file D, only if you have used custom_pretrained | Full path to pretrained file D                                                                                                                                                                                                                                  |

_Refer to `python main.py train -h` for additional help._

#### Generate Index File

```bash
python main.py index --model_name "model_name" --rvc_version "rvc_version"
```

| Parameter Name | Required | Default | Valid Options     | Description          |
| -------------- | -------- | ------- | ----------------- | -------------------- |
| `model_name`   | Yes      |         | Name of the model | Name of the model    |
| `rvc_version`  | Yes      |         | v1 or v2          | Version of the model |

_Refer to `python main.py index -h` for additional help._

### Additional Features

#### Model Extract

```bash
python main.py model_extract --pth_path "pth_path" --model_name "model_name" --sampling_rate "sampling_rate" --pitch_guidance "pitch_guidance" --rvc_version "rvc_version" --epoch "epoch" --step "step"
```

| Parameter Name   | Required | Default | Valid Options          | Description                                                                                                                                                                                                                                                     |
| ---------------- | -------- | ------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pth_path`       | Yes      |         | Path to the pth file   | Full path to the pth file                                                                                                                                                                                                                                       |
| `model_name`     | Yes      |         | Name of the model      | Name of the model                                                                                                                                                                                                                                               |
| `sampling_rate`  | Yes      |         | 32000, 40000, or 48000 | Sampling rate of the audio data                                                                                                                                                                                                                                 |
| `pitch_guidance` | Yes      |         | True or False          | By employing pitch guidance, it becomes feasible to mirror the intonation of the original voice, including its pitch. This feature is particularly valuable for singing and other scenarios where preserving the original melody or pitch pattern is essential. |
| `rvc_version`    | Yes      |         | v1 or v2               | Version of the model                                                                                                                                                                                                                                            |
| `epoch`          | Yes      |         | 1 to 10000             | Specifies the overall quantity of epochs for the model training process.                                                                                                                                                                                        |
| `step`           | Yes      |         | 1 to ∞                 | Specifies the overall quantity of steps for the model training process.                                                                                                                                                                                         |

#### Model Information

```bash
python main.py model_information --pth_path "pth_path"
```

| Parameter Name | Required | Default | Valid Options        | Description               |
| -------------- | -------- | ------- | -------------------- | ------------------------- |
| `pth_path`     | Yes      |         | Path to the pth file | Full path to the pth file |

#### Model Blender

```bash
python main.py model_blender --model_name "model_name" --pth_path_1 "pth_path_1" --pth_path_2 "pth_path_2" --ratio "ratio"
```

| Parameter Name | Required | Default | Valid Options               | Description                      |
| -------------- | -------- | ------- | --------------------------- | -------------------------------- |
| `model_name`   | Yes      |         | Name of the model           | Name of the model                |
| `pth_path_1`   | Yes      |         | Path to the first pth file  | Full path to the first pth file  |
| `pth_path_2`   | Yes      |         | Path to the second pth file | Full path to the second pth file |
| `ratio`        | No       | 0.5     | 0.0 to 1                    | Value for blender ratio          |

#### Launch TensorBoard

```bash
python main.py tensorboard
```

#### Download Models

Run the download script with the following command:

```bash
python main.py download --model_link "model_link"
```

| Parameter Name | Required | Default | Valid Options                                                               | Description       |
| -------------- | -------- | ------- | --------------------------------------------------------------------------- | ----------------- |
| `model_link`   | Yes      |         | Link of the model (enclosed in double quotes; Google Drive or Hugging Face) | Link of the model |

_Refer to `python main.py download -h` for additional help._

### API

```bash
python main.py api --host "host" --port "port"
```

| Parameter Name | Required | Default   | Valid Options         | Description           |
| -------------- | -------- | --------- | --------------------- | --------------------- |
| `host`         | No       | 127.0.0.1 | Value for host IP     | Value for host IP     |
| `port`         | No       | 8000      | Value for port number | Value for port number |

To use the RVC CLI via the API, utilize the provided script. Make API requests to the following endpoints:

- **Docs**: `/docs`
- **Ping**: `/ping`
- **Infer**: `/infer`
- **Batch Infer**: `/batch_infer`
- **TTS**: `/tts`
- **Preprocess**: `/preprocess`
- **Extract**: `/extract`
- **Train**: `/train`
- **Index**: `/index`
- **Model Information**: `/model_information`
- **Model Fusion**: `/model_fusion`
- **Download**: `/download`

Make POST requests to these endpoints with the same required parameters as in CLI mode.

### Credits

The RVC CLI builds upon the foundations of the following projects:

- [ContentVec](https://github.com/auspicious3000/contentvec/) by auspicious3000
- [HIFIGAN](https://github.com/jik876/hifi-gan) by jik876
- [Gradio](https://github.com/gradio-app/gradio) by gradio-app
- [FFmpeg](https://github.com/FFmpeg/FFmpeg) by FFmpeg
- [audio-slicer](https://github.com/openvpi/audio-slicer) by openvpi
- [VITS](https://github.com/jaywalnut310/vits) by jaywalnut310
- [RMVPE](https://github.com/Dream-High/RMVPE) by Dream-High
- [FCPE](https://github.com/CNChTu/FCPE) by CNChTu
- [So-Vits-SVC](https://github.com/svc-develop-team/so-vits-svc) by svc-develop-team
- [Harmonify](https://huggingface.co/Eempostor/Harmonify) by Eempostor
- [RVC_CLI](https://github.com/blaise-tk/RVC_CLI) by blaise-tk
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) by RVC-Project
- [Mangio-RVC-Fork](https://github.com/Mangio621/Mangio-RVC-Fork) by Mangio621

We acknowledge and appreciate the contributions of the respective authors and communities involved in these projects.
