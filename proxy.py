"""
Python command line program to forward data sent from one host on to the next

e.g. python3 proxy.py host1 host2
"""

import argparse
import re
import socket
import sys
import threading

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

        print(f"[*] Connection from {remote_addr_pair[0]}")

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

def open_outbound_socket(addr: str, port: int) -> socket.socket:
    """
    Connect to the given host
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((addr, port))
        return s
    except ConnectionRefusedError:
        fatal_error(f"Connection to {addr}:{port} refused")
    except ConnectionAbortedError:
        fatal_error(f"Connection to {addr}:{port} aborted")
    except ConnectionResetError:
        fatal_error(f"Connection to {addr}:{port} reset")

def loop_outbound_comms(inbound_socket: socket.socket, outbound_socket: socket.socket, verbose: bool):
    while True:
        data = inbound_socket.recv(1024)

        if verbose:
            print(f"[=>] {data}")

        outbound_socket.send(data)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("listen_address", help="The address to listen on")
    parser.add_argument("listen_port", help="The port to listen on", type=int)
    parser.add_argument("connect_address", help="The address to connect to")
    parser.add_argument("connect_port", help="The port to connect to", type=int)

    parser.add_argument("-v", "--verbose", help="Print data sent between hosts", action="store_true")

    args = parser.parse_args()

    if not re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", args.listen_address):
        fatal_error(f"Listening address {args.listen_address} is not formatted correctly")
    if not re.match(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$", args.connect_address):
        fatal_error(f"Remote address {args.connect_address} is not formatted correctly")

    inbound_socket = socket.socket()
    outbound_socket = socket.socket()

    try:
        inbound_socket = listen_for_connection(args.listen_address, args.listen_port)
        outbound_socket = open_outbound_socket(args.connect_address, args.connect_port)

        print("[*] Successfully connected to outbound address")

        thread = threading.Thread(target=loop_outbound_comms, args=(inbound_socket, outbound_socket, args.verbose), daemon=True)
        thread.start()

        while True:
            data = outbound_socket.recv(1024)

            if data == b"":
                break

            if args.verbose:
                print(f"[<=] {data}")

            inbound_socket.send(data)

    except KeyboardInterrupt:
        pass

    print("[*] Connection closed")
    inbound_socket.close()
    outbound_socket.close()

main()
