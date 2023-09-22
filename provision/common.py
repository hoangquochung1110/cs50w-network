# pylint: disable=redefined-builtin
from rich import print
from rich.panel import Panel


def success(msg):
    """Print success message."""
    return print(Panel(msg, style="green bold"))


def warn(msg):
    """Print warning message."""
    return print(Panel(msg, style="yellow bold"))


def error(msg):
    """Print error message."""
    return print(Panel(msg, style="red bold"))
