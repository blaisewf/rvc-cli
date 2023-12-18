import argparse


def validate_sampling_rate(value):
    valid_sampling = [
        "32000",
        "40000",
        "48000",
    ]
    if value in valid_sampling:
        return value
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid sampling_rate. Please choose from {valid_sampling}"
        )


def validate_f0up_key(value):
    f0up_key = int(value)
    if -12 <= f0up_key <= 12:
        return f0up_key
    else:
        raise argparse.ArgumentTypeError(f"f0up_key must be in the range of -12 to +12")


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
