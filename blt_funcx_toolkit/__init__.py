import logging

from blt_funcx_toolkit.execution import *
from blt_funcx_toolkit.transfer import *
from blt_funcx_toolkit.config import *

__author__ = "BLT Team"

__all__ = [
    "blt_endpoints", "BLTEndpoint", "FUNCX_SLEEP_TIME",
    "run_function_wait_result", "run_function_async", "run_console_cmd",
    "setup_ftp_conn", "ftp_upload_file_to_blt", "ftp_download_file_from_blt"
]


def set_stream_logger(name: str = 'blt_funcx_toolkit', level: int = logging.DEBUG, format_string: Optional[str] = None):
    """Add a stream log handler.
    Args:
         - name (string) : Set the logger name.
         - level (logging.LEVEL) : Set to logging.DEBUG by default.
         - format_string (string) : Set to None by default.
    Returns:
         - None
    """
    if format_string is None:
        format_string = "%(asctime)s %(name)s:%(lineno)d [%(levelname)s]  %(message)s"

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Unless we can think of a reason why not, set log level to DEBUG
set_stream_logger()