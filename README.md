## RVC_CLI: Retrieval-based Voice Conversion Command Line Interface

### Installation

Ensure you have the required Python packages installed by running (Python 3.9 is recommended):

#### Windows

Execute the install.bat file to activate a Conda environment. Subsequently, launch the application using `env/python main.py` instead of the conventional `python main.py` command.

#### Linux

```bash
pip install -r requirements.txt
```

### Getting Started

For additional information and command-line options, refer to the help command:

```bash
python main.py -h
```

This will display the available modes and their corresponding parameters, helping you understand how to use the RVC CLI effectively.

### Examples

_Make sure to adjust the parameters according to your specific use case._

#### 1. Run Inference

Run the inference script with the following command:

```bash
python main.py infer f0up_key f0method "input_path" "output_path" "pth_file" "index_path"
```

- `f0up_key`: Value for f0up_key (-12 to +12)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)
- `input_path`: Input audio path (enclosed in double quotes)
- `output_path`: Output audio path (enclosed in double quotes)
- `pth_file`: Path to the .pth file (enclosed in double quotes)
- `index_path`: Path to the .index file (enclosed in double quotes)

#### 2. Preprocess Dataset

Run the preprocessing script with the following command:

```bash
python main.py preprocess "model_name" "dataset_path" sampling_rate
```

- `model_name`: Name of the model (enclosed in double quotes)
- `dataset_path`: Path to the dataset (enclosed in double quotes)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)

#### 3. Extract Features

Run the extract script with the following command:

```bash
python main.py extract "model_name" rvc_version f0method crepe_hop_length sampling_rate
```

- `model_name`: Name of the model (enclosed in double quotes)
- `rvc_version`: Version of the model (v1 or v2)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)
- `crepe_hop_length`: Value for crepe_hop_length (1 to 512)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)

#### 4. Train

Run the train script with the following command:

```bash
python main.py train "model_name" rvc_version save_every_epoch total_epoch sampling_rate batch_size
```

- `model_name`: Name of the model (enclosed in double quotes)
- `save_every_epoch`: Number of epochs after which to save the model checkpoint (1 to 50)
- `total_epoch`: Total number of training epochs (1 to 10000)
- `batch_size`: Batch size, limited by GPU VRAM
- `rvc_version`: Version of the model (v1 or v2)
- `sampling_rate`: Sampling rate of the audio data (32000, 40000, or 48000)

#### 5. Generate index file

```bash
python main.py index "model_name" rvc_version
```

- `model_name`: Name of the model (enclosed in double quotes)
- `rvc_version`: Version of the model (v1 or v2)

#### 5. Launch TensorBoard

Launch TensorBoard with the following command:

```bash
python main.py tensorboard
```

#### 6. Download models

Run the download script with the following command:

```bash
python main.py download "model_link"
```

- `model_link`: Link of the model (enclosed in double quotes; Google Drive, Hugging Face, or MediaFire)

### Credits

The RVC CLI is built on the foundations of the following projects:

- [Mangio-RVC-Fork](https://github.com/Mangio621/Mangio-RVC-Fork)
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

We acknowledge and appreciate the contributions of the respective authors and communities involved in these projects.
