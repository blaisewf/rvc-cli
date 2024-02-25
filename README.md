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
python main.py infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_path "input_path" --output_path "output_path" --pth_path "pth_path" --index_path "index_path" --split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

| Parameter Name   | Required | Default | Valid Options                                                                                                                           | Description                        |
| ---------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `f0up_key`       | No       | 0       | -24 to +24                                                                                                                              | Value for f0up_key                 |
| `filter_radius`  | No       | 3       | 0 to 10                                                                                                                                 | Value for filter_radius            |
| `index_rate`     | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Value for index_rate               |
| `hop_length`     | No       | 128     | 1 to 512                                                                                                                                | Value for hop_length               |
| `rms_mix_rate`   | No       | 1       | 0 to 1                                                                                                                                  | Value for rms_mix_rate             |
| `protect`        | No       | 0.33    | 0 to 0.5                                                                                                                                | Value for protect                  |
| `f0autotune`     | No       | False   | True or False                                                                                                                           | Value for autotune                 |
| `f0method`       | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Value for f0method                 |
| `input_path`     | Yes      |         | Full path to the input audio file                                                                                                       | Full path to the input audio file  |
| `output_path`    | Yes      |         | Full path to the output audio file                                                                                                      | Full path to the output audio file |
| `pth_path`       | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file          |
| `index_path`     | Yes      |         | Full index file path                                                                                                                    | Full index file path               |
| `split_audio`    | No       | False   | True or False                                                                                                                           | Value for split_audio              |
| `clean_audio`    | No       | False   | True or False                                                                                                                           | Value for clean_audio              |
| `clean_strength` | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Value for clean_strength           |

_Refer to `python main.py infer -h` for additional help._

#### Batch Inference

```bash
python main.py batch_infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_folder_path "input_folder_path" --output_folder_path "output_folder_path" --pth_path "pth_path" --index_path "index_path" --split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

| Parameter Name       | Required | Default | Valid Options                                                                                                                           | Description                          |
| -------------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `f0up_key`           | No       | 0       | -24 to +24                                                                                                                              | Value for f0up_key                   |
| `filter_radius`      | No       | 3       | 0 to 10                                                                                                                                 | Value for filter_radius              |
| `index_rate`         | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Value for index_rate                 |
| `hop_length`         | No       | 128     | 1 to 512                                                                                                                                | Value for hop_length                 |
| `rms_mix_rate`       | No       | 1       | 0 to 1                                                                                                                                  | Value for rms_mix_rate               |
| `protect`            | No       | 0.33    | 0 to 0.5                                                                                                                                | Value for protect                    |
| `f0autotune`         | No       | False   | True or False                                                                                                                           | Value for autotune                   |
| `f0method`           | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Value for f0method                   |
| `input_folder_path`  | Yes      |         | Full path to the input audio folder (The folder may only contain audio files)                                                           | Full path to the input audio folder  |
| `output_folder_path` | Yes      |         | Full path to the output audio folder                                                                                                    | Full path to the output audio folder |
| `pth_path`           | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file            |
| `index_path`         | Yes      |         | Full path to the index file                                                                                                             | Full path to the index file          |
| `split_audio`        | No       | False   | True or False                                                                                                                           | Value for split_audio                |
| `clean_audio`        | No       | False   | True or False                                                                                                                           | Value for clean_audio                |
| `clean_strength`     | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Value for clean_strength             |

_Refer to `python main.py batch_infer -h` for additional help._

#### TTS Inference

```bash
python main.py tts_infer --tts_text "tts_text" --tts_voice "tts_voice" --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --output_tts_path "output_tts_path" --output_rvc_path "output_rvc_path" --pth_path "pth_path" --index_path "index_path"--split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

| Parameter Name    | Required | Default | Valid Options                                                                                                                           | Description                            |
| ----------------- | -------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `tts_text`        | Yes      |         | Text for TTS synthesis                                                                                                                  | Text for TTS synthesis                 |
| `tts_voice`       | Yes      |         | Voice for TTS synthesis                                                                                                                 | Voice for TTS synthesis                |
| `f0up_key`        | No       | 0       | -24 to +24                                                                                                                              | Value for f0up_key                     |
| `filter_radius`   | No       | 3       | 0 to 10                                                                                                                                 | Value for filter_radius                |
| `index_rate`      | No       | 0.3     | 0.0 to 1.0                                                                                                                              | Value for index_rate                   |
| `hop_length`      | No       | 128     | 1 to 512                                                                                                                                | Value for hop_length                   |
| `rms_mix_rate`    | No       | 1       | 0 to 1                                                                                                                                  | Value for rms_mix_rate                 |
| `protect`         | No       | 0.33    | 0 to 0.5                                                                                                                                | Value for protect                      |
| `f0autotune`      | No       | False   | True or False                                                                                                                           | Value for autotune                     |
| `f0method`        | No       | rmvpe   | pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe] | Value for f0method                     |
| `output_tts_path` | Yes      |         | Full path to the output TTS audio file                                                                                                  | Full path to the output TTS audio file |
| `output_rvc_path` | Yes      |         | Full path to the input RVC audio file                                                                                                   | Full path to the input RVC audio file  |
| `pth_path`        | Yes      |         | Full path to the pth file                                                                                                               | Full path to the pth file              |
| `index_path`      | Yes      |         | Full path to the index file                                                                                                             | Full path to the index file            |
| `split_audio`     | No       | False   | True or False                                                                                                                           | Value for split_audio                  |
| `clean_audio`     | No       | False   | True or False                                                                                                                           | Value for clean_audio                  |
| `clean_strength`  | No       | 0.7     | 0.0 to 1.0                                                                                                                              | Value for clean_strength               |

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

| Parameter Name  | Required | Default | Valid Options                              | Description                     |
| --------------- | -------- | ------- | ------------------------------------------ | ------------------------------- |
| `model_name`    | Yes      |         | Name of the model                          | Name of the model               |
| `rvc_version`   | No       | v2      | v1 or v2                                   | Version of the model            |
| `f0method`      | No       | rmvpe   | pm, dio, crepe, crepe-tiny, harvest, rmvpe | Value for f0method              |
| `hop_length`    | No       | 128     | 1 to 512                                   | Value for hop_length            |
| `sampling_rate` | Yes      |         | 32000, 40000, or 48000                     | Sampling rate of the audio data |

#### Start Training

```bash
python main.py train --model_name "model_name" --rvc_version "rvc_version" --save_every_epoch "save_every_epoch" --save_only_latest "save_only_latest" --save_every_weights "save_every_weights" --total_epoch "total_epoch" --sampling_rate "sampling_rate" --batch_size "batch_size" --gpu "gpu" --pitch_guidance "pitch_guidance" --pretrained "pretrained" --custom_pretrained "custom_pretrained" [--g_pretrained "g_pretrained"] [--d_pretrained "d_pretrained"]
```

| Parameter Name       | Required | Default | Valid Options                                                           | Description                                               |
| -------------------- | -------- | ------- | ----------------------------------------------------------------------- | --------------------------------------------------------- |
| `model_name`         | Yes      |         | Name of the model                                                       | Name of the model                                         |
| `rvc_version`        | No       | v2      | v1 or v2                                                                | Version of the model                                      |
| `save_every_epoch`   | Yes      |         | 1 to 50                                                                 | Number of epochs after which to save the model checkpoint |
| `save_only_latest`   | No       | False   | True or False                                                           | Save only the latest final weight                         |
| `save_every_weights` | No       | True    | True or False                                                           | Save a weight every training save                         |
| `total_epoch`        | No       | 1000    | 1 to 10000                                                              | Total number of training epochs                           |
| `sampling_rate`      | Yes      |         | 32000, 40000, or 48000                                                  | Sampling rate of the audio data                           |
| `batch_size`         | No       | 8       | 1 to 50                                                                 | Batch size, limited by GPU VRAM                           |
| `gpu`                | No       | 0       | 0 to ∞ separated by -                                                   | GPU number                                                |
| `pitch_guidance`     | No       | True    | True or False                                                           | Train with or without pitch guidance                      |
| `pretrained`         | No       | True    | True or False                                                           | Train with or without pretrained models                   |
| `custom_pretrained`  | No       | False   | True or False                                                           | Use custom pretrained models                              |
| `g_pretrained`       | No       | None    | Full path to pretrained file G, only if you have used custom_pretrained | Full path to pretrained file G                            |
| `d_pretrained`       | No       | None    | Full path to pretrained file D, only if you have used custom_pretrained | Full path to pretrained file D                            |

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
python main.py model_extract --pth_path "pth_path" --model_name "model_name" --sampling_rate "sampling_rate" --pitch_guidance "pitch_guidance" --rvc_version "rvc_version"
```

| Parameter Name   | Required | Default | Valid Options          | Description                          |
| ---------------- | -------- | ------- | ---------------------- | ------------------------------------ |
| `pth_path`       | Yes      |         | Path to the pth file   | Full path to the pth file            |
| `model_name`     | Yes      |         | Name of the model      | Name of the model                    |
| `sampling_rate`  | Yes      |         | 32000, 40000, or 48000 | Sampling rate of the audio data      |
| `pitch_guidance` | Yes      |         | True or False          | Train with or without pitch guidance |
| `rvc_version`    | Yes      |         | v1 or v2               | Version of the model                 |

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
