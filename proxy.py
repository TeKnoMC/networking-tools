"""
Python command line program to forward data sent from one host on to the next

e.g. python3 proxy.py host1 host2
"""

import argparse
import re
import socket
import sys

def fatal_error(err: str):
    """
    Print out error message and exit
    """

    sys.stderr.write("[!] " + err + "\n");
    sys.exit(1)

def listen_for_connection(addr: str, port: int) -> socket.socket:
    """
    Establish a server socket and listen for a connection -> return resulting client socket.
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((addr, port))

        s.listen(0)

        (client_socket, remote_addr_pair) = s.accept()

        s.close()

        return client_socket

    except OSError as err:
        if err.errno == 99:
            fatal_error(f"Cannot assign requested address {addr}")
        elif err.errno == 98:
            fatal_error(f"Port {port} is already in use")
        else:
            fatal_error(f"OSError: {err}")
    except OverflowError:
        fatal_error(f"Port {port} is not between 0-65535")
    except KeyboardInterrupt:
        fatal_error("Keyboard interrupt")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("listen_address", help="The address to listen on")
    parser.add_argument("listen_port", help="The port to listen on", type=int)
    parser.add_argument("connect_address", help="The address to connect to")
    parser.add_argument("port_address", help="The port to connect to", type=int)

    parser.add_argument("-v", "--verbose", help="Print data sent between hosts", action="store_true")

    args = parser.parse_args()

    if not re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", args.listen_address):
        fatal_error(f"Listening address {args.listen_address} is not formatted correctly")
    if not re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", args.connect_address):
        fatal_error(f"Listening address {args.connect_address} is not formatted correctly")

    #inbound_socket = listen_for_connection(args.listen_address, args.listen_port)

main()
