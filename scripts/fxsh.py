import argparse

from blt_funcx_toolkit import fxsh


parser = argparse.ArgumentParser()
parser.add_argument("endpoint_id", "ep", type=str,
					help="Endpoint to connect to")
args = parser.parse_args()

fxsh(endpoint=args.endpoint_id)