"""Special marker strings used in generated result files."""

OUTPUT_BLOCKED = "<OUTPUT_BLOCKED>"
OUTPUT_ERROR = "<ERROR>"


def is_blocked_output(value: str) -> bool:
    return value == OUTPUT_BLOCKED


def is_error_output(value: str) -> bool:
    return value == OUTPUT_ERROR
