"""
A simple python clone of NetCat - a command line networking tool to
interact with raw sockets.

Intended examples:
> python3 nc.py -l 8080
> python3 nc.py 10.10.10.10 8080
> python3 nc.py -h
"""

import argparse
import socket

def listen(addr, port, verbosity):
    """
    Sets up a server to listen on (addr, port), and then loops over sending/recieving data.
    """

    raise NotImplementedError

def connect(addr, port, verbosity):
    """
    Attempts to connect to (addr, port), and then loops over sending/recieving data.
    """

    raise NotImplementedError

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("address", help="The network address to interact with")
    parser.add_argument("port", help="The port to interact with", type=int)

    parser.add_argument("-l", "--listen", help="Listen on the port-address pair", action="store_true")
    parser.add_argument("-v", "--verbosity", help="More detailed logging", action="count", default=0)

    args = parser.parse_args()

    if args.listen:
        listen(args.address, args.port, args.verbosity)
    else:
        connect(args.address, args.port, args.verbosity)

main()