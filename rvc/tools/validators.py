import argparse

def validate_sampling_rate(value):
    valid_sampling_rates = [32000, 40000, 48000]
    try:
        sampling_rate = int(value)
        if sampling_rate in valid_sampling_rates:
            return sampling_rate
        else:
            raise argparse.ArgumentTypeError(
                f"Invalid sampling rate. Please choose from {valid_sampling_rates}"
            )
    except ValueError:
        raise argparse.ArgumentTypeError("Sampling rate must be a valid integer")

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

def validate_f0method(value):
    valid_f0methods = [
        "pm",
        "dio",
        "crepe",
        "crepe-tiny",
        "mangio-crepe",
        "mangio-crepe-tiny",
        "harvest",
        "rmvpe",
    ]
    if value in valid_f0methods:
        return value
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid f0method. Please choose from {valid_f0methods}"
        )
