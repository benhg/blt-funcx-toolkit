"""
FuncX Shell - `fxsh`

Use FuncX to open a virtual
    interactive session on a FuncX endpoint.

Any commands input will be forwarded to the
    endpoint using `subprocess.check_output`

Has only been tested with Linux-based endponits
"""

import argparse

from blt_funcx_toolkit.execution import fxsh
from blt_funcx_toolkit.config import blt_endpoints

def cli_run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint-name",
                        "-ep",
                        type=str,
                        help="Endpoint to open interactive session on",
                        default="blt_small",
                        choices=list(blt_endpoints.keys()))
    parser.add_argument("--verbose",
                        "-v",
                        action="store_true",
                        help="Enable verbose output",
                        default=False)
    args = parser.parse_args()
    args = parser.parse_args()

    fxsh(endpoint_name=args.endpoint_name, print_wait=args.verbose)
if __name__ == '__main__':
    cli_run()