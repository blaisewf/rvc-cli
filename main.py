import os
import sys
import wget
import argparse
import subprocess
from rvc.configs.config import Config

config = Config()
logs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")

# Download models
if not os.path.exists("./hubert_base.pt"):
    wget.download(
        "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt",
        out="./hubert_base.pt",
    )

if not os.path.exists("./rmvpe.pt"):
    wget.download(
        "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt",
        out="./rmvpe.pt",
    )

if sys.platform == "win32":
    if not os.path.exists("./ffmpeg.exe"):
        wget.download(
            "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/ffmpeg.exe",
            out="./ffmpeg.exe",
        )
if sys.platform == "win32":
    if not os.path.exists("./ffprobe.exe"):
        wget.download(
            "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/ffprobe.exe",
            out="./ffprobe.exe",
        )


# Infer
def validate_f0up_key(value):
    try:
        f0up_key = int(value)
        if -12 <= f0up_key <= 12:
            return f0up_key
        else:
            raise argparse.ArgumentTypeError(
                f"f0up_key must be in the range of -12 to +12"
            )
    except ValueError:
        raise argparse.ArgumentTypeError("f0up_key must be a valid integer")


def run_infer_script(f0up_key, f0method, input_path, output_path, pth_file, index_path):
    command = [
        "python",
        "rvc/infer/infer.py",
        str(f0up_key),
        f0method,
        input_path,
        output_path,
        pth_file,
        index_path,
    ]
    subprocess.run(command)


# Train
def run_preprocess_script(model_name, dataset_path, sampling_rate, cpu_processes):
    per = 3.0 if config.is_half else 3.7
    command = [
        "python",
        "rvc/train/preprocess/preprocess.py",
        logs_path + "\\" + str(model_name),
        dataset_path,
        str(sampling_rate),
        str(cpu_processes),
        str(per),
    ]

    os.mkdir(logs_path + "\\" + str(model_name))
    subprocess.run(command)


def run_extract_script(
    model_name, rvc_version, cpu_processes, f0method, crepe_hop_length
):
    command_1 = [
        "python",
        "rvc/train/extract/extract_f0_print.py",
        logs_path + "\\" + str(model_name),
        cpu_processes,
        f0method,
        crepe_hop_length,
    ]
    command_2 = [
        "python",
        "rvc/train/extract/extract_feature_print.py",
        config.device,
        "1",
        "0",
        "0",
        logs_path + "\\" + str(model_name),
        rvc_version,
        "True",
    ]
    subprocess.run(command_1)
    subprocess.run(command_2)


def run_tensorboard_script():
    command = [
        "python",
        "rvc/tools/launch_tensorboard.py",
    ]
    subprocess.run(command)


def run_download_script(model_link):
    command = [
        "python",
        "rvc/tools/model_download.py",
        model_link,
    ]
    subprocess.run(command)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the main.py script with specific parameters."
    )

    subparsers = parser.add_subparsers(
        title="subcommands", dest="mode", help="Choose a mode"
    )

    # Parser for 'infer' mode
    infer_parser = subparsers.add_parser("infer", help="Run inference")
    infer_parser.add_argument(
        "f0up_key", type=validate_f0up_key, help="Value for f0up_key (-12 to +12)"
    )
    infer_parser.add_argument(
        "f0method",
        type=str,
        help="Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)",
    )
    infer_parser.add_argument(
        "input_path", type=str, help="Input path (enclose in double quotes)"
    )
    infer_parser.add_argument(
        "output_path", type=str, help="Output path (enclose in double quotes)"
    )
    infer_parser.add_argument(
        "pth_file", type=str, help="Path to the .pth file (enclose in double quotes)"
    )
    infer_parser.add_argument(
        "index_path",
        type=str,
        help="Path to the .index file (enclose in double quotes)",
    )

    # Parser for 'preprocess' mode
    preprocess_parser = subparsers.add_parser("preprocess", help="Run preprocessing")
    preprocess_parser.add_argument(
        "model_name", type=str, help="Name of the model (enclose in double quotes)"
    )
    preprocess_parser.add_argument(
        "dataset_path",
        type=str,
        help="Path to the dataset (enclose in double quotes)",
    )
    preprocess_parser.add_argument(
        "sampling_rate", type=int, help="Sampling rate (32000, 40000 or 48000)"
    )
    preprocess_parser.add_argument(
        "cpu_processes", type=int, help="Number of CPU processes"
    )

    # Parser for 'extract' mode
    extract_parser = subparsers.add_parser("extract", help="Run extract")
    extract_parser.add_argument(
        "model_name",
        type=str,
        help="Name of the model (enclose in double quotes)",
    )
    extract_parser.add_argument(
        "rvc_version",
        type=str,
        help="Version of the model (v1 or v2)",
    )
    extract_parser.add_argument(
        "cpu_processes", type=str, help="Number of CPU processes"
    )
    extract_parser.add_argument(
        "f0method",
        type=str,
        help="Value for f0method (pm, dio, crepe, crepe-tiny, mangio-crepe, mangio-crepe-tiny, harvest, rmvpe)",
    )
    extract_parser.add_argument(
        "crepe_hop_length", type=str, help="Value for crepe_hop_length (1 to 512)"
    )

    # Parser for 'tensorboard' mode
    subparsers.add_parser("tensorboard", help="Run tensorboard")

    # Parser for 'download' mode
    download_parser = subparsers.add_parser("download", help="Download models")
    download_parser.add_argument(
        "model_link",
        type=str,
        help="Link of the model (enclose in double quotes)",
    )

    return parser.parse_args()


def main():
    if len(sys.argv) == 1:
        print("Please run the script with '-h' for more information.")
        sys.exit(1)

    args = parse_arguments()

    try:
        if args.mode == "infer":
            run_infer_script(
                args.f0up_key,
                args.f0method,
                args.input_path,
                args.output_path,
                args.pth_file,
                args.index_path,
            )
        elif args.mode == "preprocess":
            run_preprocess_script(
                args.model_name,
                args.dataset_path,
                str(args.sampling_rate),
                str(args.cpu_processes),
            )

        elif args.mode == "extract":
            run_extract_script(
                args.model_name,
                args.rvc_version,
                args.cpu_processes,
                args.f0method,
                args.crepe_hop_length,
            )
        elif args.mode == "tensorboard":
            run_tensorboard_script()
        elif args.mode == "download":
            run_download_script(
                args.model_link,
            )
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
