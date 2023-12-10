import argparse
import subprocess


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
        "rvc/infer.py",
        str(f0up_key),
        f0method,
        input_path,
        output_path,
        pth_file,
        index_path,
    ]

    subprocess.run(command)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Run the main.py script with specific parameters."
    )
    parser.add_argument("f0up_key", type=validate_f0up_key, help="Value for f0up_key")
    parser.add_argument("f0method", type=str, help="Value for f0method")
    parser.add_argument(
        "input_path", type=str, help="Input path (enclose in double quotes)"
    )
    parser.add_argument(
        "output_path", type=str, help="Output path (enclose in double quotes)"
    )
    parser.add_argument(
        "pth_file", type=str, help="Path to the .pth file (enclose in double quotes)"
    )
    parser.add_argument(
        "index_path",
        type=str,
        help="Path to the .index file (enclose in double quotes)",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    try:
        run_infer_script(
            args.f0up_key,
            args.f0method,
            args.input_path,
            args.output_path,
            args.pth_file,
            args.index_path,
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
