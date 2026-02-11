import logging
import sys


def setup_logging(log_level: int = logging.INFO) -> None:
    """
    Configure the logging system for the bot.

    :param log_level: The base logging level, e.g. ``logging.WARNING``. Defaults to ``logging.INFO``
    """
    root = logging.getLogger()
    root.setLevel(log_level)

    # stdout: DEBUG, INFO
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(lambda r: r.levelno < logging.WARNING)

    # stderr: WARNING, ERROR, CRITICAL
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    stdout_handler.setFormatter(formatter)
    stderr_handler.setFormatter(formatter)

    root.handlers.clear()
    root.addHandler(stdout_handler)
    root.addHandler(stderr_handler)

    logging.getLogger("discord").setLevel(logging.WARNING)
