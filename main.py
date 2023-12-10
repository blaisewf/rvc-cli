import argparse
import subprocess


def run_infer_script(f0up_key, f0method, input_path, output_path, pth_file, index_path):
    command = [
        "python",
        "rvc/infer.py",
        f0up_key,
        f0method,
        input_path,
        output_path,
        pth_file,
        index_path,
    ]

    subprocess.run(command)


def main():
    parser = argparse.ArgumentParser(
        description="Run the infer.py script with specific parameters."
    )

    parser.add_argument("f0up_key", help="Value for f0up_key (required)")
    parser.add_argument("f0method", help="Value for f0method (required)")
    parser.add_argument(
        "input_path", help="Input path (required; enclose in double quotes)"
    )
    parser.add_argument(
        "output_path", help="Output path (required; enclose in double quotes)"
    )
    parser.add_argument(
        "pth_file", help="Path to the .pth file (required; enclose in double quotes)"
    )
    parser.add_argument(
        "index_path",
        help="Path to the .index file (required; enclose in double quotes)",
    )

    args = parser.parse_args()

    run_infer_script(
        args.f0up_key,
        args.f0method,
        args.input_path,
        args.output_path,
        args.pth_file,
        args.index_path,
    )


if __name__ == "__main__":
    main()
