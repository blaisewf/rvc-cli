## RVC CLI

### Installation

> [!NOTE]  
> The training section is currently under development

Ensure you have the required Python packages installed by running:

```bash
pip install -r requirements.txt
```

Make sure to have Python installed on your system.

### Help

For additional information and command-line options, refer to the help command:

```bash
python main.py -h
```

This will display the available modes and their corresponding parameters, helping you understand how to use the RVC CLI effectively.

_Make sure to adjust the parameters according to your specific use case._

### Help Command Example

```bash
python main.py -h
```

### Examples

#### 1. Run Inference

Run the inference script with the following command:

```bash
python main.py infer 0 crepe "input.wav" "output.wav" "model_file.pth" "index_file.index"
```

- `f0up_key`: Value for f0up_key (-12 to +12)
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)
- `input_path`: Input path (enclose in double quotes)
- `output_path`: Output path (enclose in double quotes)
- `pth_file`: Path to the .pth file (enclose in double quotes)
- `index_path`: Path to the .index file (enclose in double quotes)

#### 2. Preprocess Dataset

Run the preprocessing script with the following command:

```bash
python main.py preprocess "dataset_path" 32000 4 "model_name"
```

- `dataset_path`: Path to the dataset (enclose in double quotes)
- `sampling_rate`: Sampling rate (32000, 40000, or 48000)
- `cpu_processes`: Number of CPU processes
- `model_name`: Name of the model (enclose in double quotes)

#### 3. Extract Features

Run the extract script with the following command:

```bash
python main.py extract "model_name" v1 4 crepe 512
```

- `model_name`: Name of the model (enclose in double quotes)
- `rvc_version`: Version of the model (v1 or v2)
- `cpu_processes`: Number of CPU processes
- `f0method`: Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)
- `crepe_hop_length`: Value for crepe_hop_length (1 to 512)

#### 4. Launch TensorBoard

Launch TensorBoard with the following command:

```bash
python main.py tensorboard
```

### Credits

The RVC CLI is built on the foundations of the following projects:

- [Mangio-RVC-Fork](https://github.com/Mangio621/Mangio-RVC-Fork)
- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

We acknowledge and appreciate the contributions of the respective authors and communities involved in these projects.
