"""
A simple python clone of netcat - a command line networking tool to
interact with raw sockets.

Intended examples:
> python3 nc.py -l 8080
> python3 nc.py 10.10.10.10 8080
> python3 nc.py -h
"""

import argparse
import socket
import sys
import threading

def fatal_error(err: str):
    sys.stderr.write("[!] " + err + "\n");
    sys.exit(-1)

def loop_sending_input_data(s: socket.socket):
    print("[*] Send data by typing and pressing enter.")

    try:
        while True:
            data = input().encode("utf-8")
            print(f"[>] Sending: {data}")
            s.send(data)
    except KeyboardInterrupt:
        pass
        

def listen(addr: str, port: int):
    """
    Sets up a server to listen on (addr, port), and then loops over sending/receiving data.
    """

    raise NotImplementedError

def connect(addr: str, port: int):
    """
    Attempts to connect to (addr, port), and then loops over sending/receiving data.
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((addr, port))

        print(f"[*] Connected to {addr}:{port}")

        thread = threading.Thread(target=loop_sending_input_data, args=(s,), daemon=True)
        thread.start()

        while True:
            data = s.recv(1024)

            if data == b'':
                break

            print(f"[<] Received: {data}")

            if not thread.is_alive():
                break

    except ConnectionRefusedError:
        fatal_error(f"Connection to {addr}:{port} refused.")
    except ConnectionAbortedError:
        fatal_error(f"Connection to {addr}:{port} aborted.")
    except ConnectionResetError:
        fatal_error(f"Connection to {addr}:{port} reset.")
    except KeyboardInterrupt:
        pass

    
    s.close()
    print(f"[*] Connection to {addr}:{port} closed.")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("address", help="The network address to interact with")
    parser.add_argument("port", help="The port to interact with", type=int)

    parser.add_argument("-l", "--listen", help="Listen on the port-address pair", action="store_true")

    args = parser.parse_args()

    #TODO: VALIDATE WITH REGEX ON ADDRESS

    if args.listen:
        listen(args.address, args.port)
    else:
        connect(args.address, args.port)

main()