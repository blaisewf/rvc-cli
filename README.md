## RVC_CLI: Retrieval-based Voice Conversion Command Line Interface

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/blaise-tk/rvc_cli/blob/master/RVC_CLI.ipynb)

### Todo

- Use this style for commands `python your_script.py infer --hop_length 128 --f0method rmvpe --input_path "input.wav" --output_path "output.wav" --pth_file "model.pth" --index_path "index_file.index"`
- Add Audio Split in infer

### Table of Contents

1. [Installation](#installation)
   - [Windows](#windows)
   - [Linux](#linux)
2. [Getting Started](#getting-started)
   - [Inference](#inference)
   - [Training](#training)
   - [Additional Features](#additional-features)
3. [Credits](#credits)

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

#### Run Inference

```bash
python main.py infer f0up_key filter_radius index_rate hop_length f0method "input_path" "output_path" "pth_file" "index_path"
```

- `f0up_key`: Value for f0up_key (-12 to +12)
- `filter_radius`: Value for filter_radius (0 to 10)
- `index_rate`: Value for index_rate (0.0 to 1.0)
- `hop_length`: Value for hop_length (1 to 512)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, harvest, rmvpe)
- `input_path`: Input audio path (enclosed in double quotes)
- `output_path`: Output audio path (enclosed in double quotes)
- `pth_file`: Path to the .pth file (enclosed in double quotes)
- `index_path`: Path to the .index file (enclosed in double quotes)

### Training

#### Preprocess Dataset

```bash
python main.py preprocess "model_name" "dataset_path" sampling_rate
```

- `model_name`: Name of the model (enclosed in double quotes)
- `dataset_path`: Path to the dataset (enclosed in double quotes)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000): Optional, default `40000`

#### Extract Features

```bash
python main.py extract "model_name" rvc_version f0method hop_length sampling_rate
```

- `model_name`: Name of the model (enclosed in double quotes)
- `rvc_version`: Version of the model (v1 or v2)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, harvest, rmvpe)
- `hop_length`: Value for hop_length (1 to 512)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)

#### Start Training

```bash
python main.py train "model_name" rvc_version save_every_epoch save_only_latest save_every_weights total_epoch sampling_rate batch_size gpu pitch_guidance pretrained custom_pretrained [g_pretrained] [d_pretrained]
```

- `model_name`: Name of the model (enclosed in double quotes)
- `rvc_version`: Version of the model (v1 or v2)
- `save_every_epoch`: Number of epochs after which to save the model checkpoint (1 to 50)
- `save_only_latest`: Save only the lastest final weight (True or False)
- `save_every_weights`: Save a weight every training save (True or False)
- `total_epoch`: Total number of training epochs (1 to 10000)
- `sampling_rate`: Sampling rate of the audio data (32000, 40000, or 48000): Optional, default `40000`
- `batch_size`: Batch size, limited by GPU VRAM (4 to ∞)
- `gpu`: GPU number (0 to ∞ separated by -)
- `pitch_guidance`: Train with or without pitch guidance (True or False)
- `pretrained`: Train with or without pretrained models (True or False)
- `custom_pretrained`: Use custom pretrained models; use parameters g\_/d_pretrained (True or False)
- `g_pretrained_path`: Path to pretrained file G, only if you have used custom_pretrained (enclosed in double quotes)
- `d_pretrained_path`: Path to pretrained file D, only if you have used custom_pretrained (enclosed in double quotes)

#### Generate Index File

```bash
python main.py index "model_name" rvc_version
```

- `model_name`: Name of the model (enclosed in double quotes)
- `rvc_version`: Version of the model (v1 or v2)

### Additional Features

#### Model Information

```bash
python main.py model_information "pth_path"
```

- `pth_path`: Path to the .pth file (enclosed in double quotes)

#### Model Fusion

```bash
python main.py model_fusion "model_name" "pth_path_1" "pth_path_2"
```

- `model_name`: Name of the model (enclosed in double quotes)
- `pth_path_1`: Path to the first .pth file (enclosed in double quotes)
- `pth_path_2`: Path to the second .pth file (enclosed in double quotes)

#### Launch TensorBoard

```bash
python main.py tensorboard
```

#### Download Models

Run the download script with the following command:

```bash
python main.py download "model_link"
```

- `model_link`: Link of the model (enclosed in double quotes; Google Drive or Hugging Face)

### Credits

The RVC CLI is built on the foundations of the following projects:

- [Mangio-RVC-Fork](https://github.com/Mangio621/Mangio-RVC-Fork)
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

We acknowledge and appreciate the contributions of the respective authors and communities involved in these projects.
