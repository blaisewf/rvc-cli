## RVC_CLI: Retrieval-based Voice Conversion Command Line Interface

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blaise-tk/rvc_cli/blob/master/RVC_CLI.ipynb)

### Todo

- [ ] Optimize the download of prerequisites so as not to run it every time main.py is executed.
- [ ] Fix Google Colab (missing some updates)

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

Ensure you have the required Python packages installed by running (Python 3.9 is recommended):

#### Windows

Execute the [install.bat](./install.bat) file to activate a Conda environment. Subsequently, launch the application using `env/python main.py` instead of the conventional `python main.py` command.

#### Linux

```bash
chmod +x install.sh
./install.sh
```

### Getting Started

For additional information and command-line options, refer to the help command:

```bash
python main.py -h
```

This command displays the available modes and their corresponding parameters, providing clarity on how to effectively use the RVC CLI.

### Inference

#### Single Inference

```bash
python main.py infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_path "input_path" --output_path "output_path" --pth_path "pth_path" --index_path "index_path" --split_audio "split_audio" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

- `f0up_key`: Value for f0up_key (-24 to +24)
- `filter_radius`: Value for filter_radius (0 to 10)
- `index_rate`: Value for index_rate (0.0 to 1.0)
- `hop_length`: Value for hop_length (1 to 512)
- `rms_mix_rate`: Value for rms_mix_rate (0 to 1)
- `protect`: Value for protect (0 to 0.5)
- `f0autotune`: Value for autotune (True or False)
- `f0method`: Value for f0method (pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe])
- `input_path`: Full path to the input audio file
- `output_path`: Full path to the output audio file
- `pth_path`: Full path to the pth file
- `index_path`: Full index file path
- `split_audio`: Value for split_audio (True or False)
- `clean_audio`: Value for clean_audio (True or False)
- `clean_strength`: Value for clean_strength (0.0 to 1.0)

_If you need more help, check `python main.py infer -h`_

#### Batch Inference

```bash
python main.py batch_infer --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --input_folder_path "input_folder_path" --output_folder_path "output_folder_path" --pth_path "pth_path" --index_path "index_path" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

- `f0up_key`: Value for f0up_key (-24 to +24)
- `filter_radius`: Value for filter_radius (0 to 10)
- `index_rate`: Value for index_rate (0.0 to 1.0)
- `hop_length`: Value for hop_length (1 to 512)
- `rms_mix_rate`: Value for rms_mix_rate (0 to 1)
- `protect`: Value for protect (0 to 0.5)
- `f0autotune`: Value for autotune (True or False)
- `f0method`: Value for f0method (pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe])
- `input_folder_path`: Full path to the input audio folder (The folder may only contain audio files)
- `output_folder_path`: Full path to the output audio folder
- `pth_path`: Full path to the pth file
- `index_path`: Full path to the index file
- `clean_audio`: Value for clean_audio (True or False)
- `clean_strength`: Value for clean_strength (0.0 to 1.0)

_If you need more help, check `python main.py batch_infer -h`_

#### TTS Inference

```bash
python main.py tts_infer --tts_text "tts_text" --tts_voice "tts_voice" --f0up_key "f0up_key" --filter_radius "filter_radius" --index_rate "index_rate" --hop_length "hop_length" --rms_mix_rate "rms_mix_rate" --protect "protect" --f0autotune "f0autotune" --f0method "f0method" --output_tts_path "output_tts_path" --output_rvc_path "output_rvc_path" --pth_path "pth_path" --index_path "index_path" --clean_audio "clean_audio" --clean_strength "clean_strength"
```

- `tts_text`: Text for TTS synthesis
- `tts_voice`: Voice for TTS synthesis
- `f0up_key`: Value for f0up_key (-24 to +24)
- `filter_radius`: Value for filter_radius (0 to 10)
- `index_rate`: Value for index_rate (0.0 to 1.0)
- `hop_length`: Value for hop_length (1 to 512)
- `rms_mix_rate`: Value for rms_mix_rate (0 to 1)
- `protect`: Value for protect (0 to 0.5)
- `f0autotune`: Value for autotune (True or False)
- `f0method`: Value for f0method (pm, harvest, dio, crepe, crepe-tiny, rmvpe, fcpe, hybrid[crepe+rmvpe], hybrid[crepe+fcpe], hybrid[rmvpe+fcpe], hybrid[crepe+rmvpe+fcpe])
- `output_tts_path`: Full path to the output TTS audio file
- `output_rvc_path`: Full path to the input RVC audio file
- `pth_path`: Full path to the pth file
- `index_path`: Full path to the index file
- `clean_audio`: Value for clean_audio (True or False)
- `clean_strength`: Value for clean_strength (0.0 to 1.0)

_If you need more help, check `python main.py tts_infer -h`_

### Training

#### Preprocess Dataset

```bash
python main.py preprocess --model_name "model_name" --dataset_path "dataset_path" --sampling_rate "sampling_rate"
```

- `model_name`: Name of the model
- `dataset_path`: Full path to the dataset folder (The folder may only contain audio files)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)

_If you need more help, check `python main.py preprocess -h`_

#### Extract Features

```bash
python main.py extract --model_name "model_name" --rvc_version "rvc_version" --f0method "f0method" --hop_length "hop_length" --sampling_rate "sampling_rate"
```

- `model_name`: Name of the model
- `rvc_version`: Version of the model (v1 or v2)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, harvest, rmvpe)
- `hop_length`: Value for hop_length (1 to 512)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)

#### Start Training

```bash
python main.py train --model_name "model_name" --rvc_version "rvc_version" --save_every_epoch "save_every_epoch" --save_only_latest "save_only_latest" --save_every_weights "save_every_weights" --total_epoch "total_epoch" --sampling_rate "sampling_rate" --batch_size "batch_size" --gpu "gpu" --pitch_guidance "pitch_guidance" --pretrained "pretrained" --custom_pretrained "custom_pretrained" [--g_pretrained "g_pretrained"] [--d_pretrained "d_pretrained"]
```

- `model_name`: Name of the model
- `rvc_version`: Version of the model (v1 or v2)
- `save_every_epoch`: Number of epochs after which to save the model checkpoint (1 to 50)
- `save_only_latest`: Save only the lastest final weight (True or False)
- `save_every_weights`: Save a weight every training save (True or False)
- `total_epoch`: Total number of training epochs (1 to 1000)
- `sampling_rate`: Sampling rate of the audio data (32000, 40000, or 48000)
- `batch_size`: Batch size, limited by GPU VRAM (1 to 50)
- `gpu`: GPU number (0 to ∞ separated by -)
- `pitch_guidance`: Train with or without pitch guidance (True or False)
- `pretrained`: Train with or without pretrained models (True or False)
- `custom_pretrained`: Use custom pretrained models; use parameters g\_/d_pretrained (True or False)
- `g_pretrained_path`: Path to pretrained file G, only if you have used custom_pretrained
- `d_pretrained_path`: Path to pretrained file D, only if you have used custom_pretrained

_If you need more help, check `python main.py train -h`_

#### Generate Index File

```bash
python main.py index --model_name "model_name" --rvc_version "rvc_version"
```

- `model_name`: Name of the model
- `rvc_version`: Version of the model (v1 or v2)

_If you need more help, check `python main.py index -h`_

### Additional Features

#### Model Information

```bash
python main.py model_information --pth_path "pth_path"
```

- `pth_path`: Path to the .pth file

_If you need more help, check `python main.py model_information -h`_

#### Model Fusion (Not working)

```bash
python main.py model_fusion --model_name "model_name" --pth_path_1 "pth_path_1" --pth_path_2 "pth_path_2"
```

- `model_name`: Name of the model
- `pth_path_1`: Path to the first .pth file
- `pth_path_2`: Path to the second .pth file

_If you need more help, check `python main.py model_fusion -h`_

#### Launch TensorBoard

```bash
python main.py tensorboard
```

#### Download Models

Run the download script with the following command:

```bash
python main.py download --model_link "model_link"
```

- `model_link`: Link of the model (enclosed in double quotes; Google Drive or Hugging Face)
  _If you need more help, check `python main.py download -h`_

### API

```bash
python main.py api
```

To use the RVC CLI via the API, you can utilize the provided script. Make API requests to the following endpoints:

- **Infer**: `/infer`
- **Batch Infer**: `/batch_infer`
- **TTS**: `/tts`
- **Preprocess**: `/preprocess`
- **Extract**: `/extract`
- **Train**: `/train`
- **Index**: `/index`
- **Model Information**: `/model_information`
- **Model Fusion**: `/model_fusion`
- **Tensorboard**: `/tensorboard`
- **Download**: `/download`

You can make POST requests to these endpoints with the same required parameters as in CLI mode.

### Credits

The RVC CLI is built on the foundations of the following projects:

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
