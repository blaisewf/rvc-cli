## RVC CLI

### Usage Example

Execute the RVC CLI with the following command:

```bash
python main.py 0 rmvpe "input_path" "output_path" "model.pth" "index_file.index"
```

### Installation

Ensure you have the required Python packages installed by running:

```bash
pip install -r requirements.txt
```

### Help

For additional information and command-line options, refer to the help command:

```bash
main.py -h
```

### Explanation

The usage example illustrates the usage of the RVC CLI with the following parameters:

- `f0up_key`: Value for f0up_key (required) [-12 to +12]
- `f0method`: Value for f0method (required) [pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe]
- `input_path`: Input path (required; enclose in double quotes)
- `output_path`: Output path (required; enclose in double quotes)
- `pth_file`: Path to the .pth file (required; enclose in double quotes)
- `index_path`: Path to the .index file (required; enclose in double quotes)

_Make sure to adjust the parameters according to your specific use case._
