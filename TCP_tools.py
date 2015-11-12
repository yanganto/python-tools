"""
doc
"""
import sys
import socket
import getopt
import threading
import subprocess


verbose = False
listen = False
command = False
execute = ""
target = ""
upload_destination = ""
port = 0

def main():
    global listen
    global command
    global execute
    global target
    global upload_destination
    global port
    global verbose
    if not sys.argv[1:]:
        print(__doc__)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vhle:t:p:cu:",
                ["verbose", "help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as e:
        print(e)
        print(__doc__)
        sys.exit(-1)

    for o, a in opts:
        if o in ('-h', '--help'):
            print(__doc__)
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-c', '--command'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-v', '--verbose'):
            verbose = True
        else:
            assert False, "Unhandle options"

    if verbose:
        print('''
listen: {}
command: {}
execute: {}
target: {}
upload_destination: {}
port: {}
'''.format(listen, command, execute, target, upload_destination, port))

    if not listen and len(target) and port:
        read_in_buffer = sys.stdin.read()
        client_sender(read_in_buffer)
    if listen:
        server_loop()

def client_sender(read_in_buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if verbose:
            print("Create connection.")
        if read_in_buffer:
            client.send(read_in_buffer.encode('utf-8'))

        if verbose:
            print("Send: " + read_in_buffer)

        while True:
            recv_len = 1
            response = b""
            while recv_len:
                data = client.recv(4096)
                if verbose:
                    print("Received: " + data.decode('utf-8'))
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response.decode('utf-8'))

            read_in_buffer= input("")
            read_in_buffer += '\n'
            client.send(read_in_buffer.encode('utf-8'))
    except:
        if verbose:
            print("Exception:", sys.exc_info())
            print("Quit.")
        client.close()


if __name__ == "__main__":
    main()
