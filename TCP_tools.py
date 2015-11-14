"""
A tool for TCP  connection

USSAGE: TCP_tools.py -t target_host -p port
    -l, --listen
        into Listening mode
    -e, --execute=file_to_run 
        execute command to response
    -c, --command
        start a shell
    -u, --upload=destination
        recieving to a file

EXAMPLE:
    TCP_tools.py -lcp 9999
    TCP_tools.py -lcp 9999 -u request.binary
    TCP_tools.py -lcp 9999 -e ls
    echo "send Some" | TCP_tools.py -t 192.168.0.1 -p 9999
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

    if not listen and target and port:
        read_in_buffer = sys.stdin.read()
        client_sender(read_in_buffer)
    if listen:
        server_loop()

def client_sender(read_in_buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if verbose:
            print("Create connection at{}:{}.".format(target, port))
        if read_in_buffer:
            client.send(read_in_buffer.encode('utf-8'))

        if verbose:
            print("Send: " + read_in_buffer)

        while True:
            recv_len = 1
            response = ""
            while recv_len:
                data = client.recv(4096).decode('utf-8')
                if verbose:
                    print("Received: " + data)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break
            print(response)

            read_in_buffer = input("")
            read_in_buffer += '\n'
            client.send(read_in_buffer.encode('utf-8'))
    except:
        if verbose:
            print("Exception:", sys.exc_info())
            print("Quit.")
        client.close()

def server_loop():
    global target
    if not target:
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        if verbose:
            print("Recived from: {}:{}".format(*addr))
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))    
        client_thread.start()
        
def client_handler(client_socket):
    global upload_destination
    global verbose

    if upload_destination: 
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        try:
            with open(upload_destination, "wb") as fout:
                fout.write(file_buffer)
            if verbose:
                print("Save to response to file {}.".format(upload_destination))
            client_socket.send(b"copied.")
        except:
            if verbose:
                print("{}: {}".format(*sys.exc_info()))
            client_socket.send(b"Fail to copy.")

    if execute:
        output = run_command(execute)
        client_socket.send(output)
        if verbose:
            print('send "{}"'.format(output))

    if command:
        while True:
            client_socket.send(b"#>")
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                receiving_data = client_socket.recv(1024)
                cmd_buffer += receiving_data
            response = run_command(cmd_buffer)
            client_socket.send(response) 

def run_command(command):
    command = command.strip()
    if verbose:
        print("Execute: {}".format(command))
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        if verbose:
            print("Output: {}".format(output))
    except:
        if verbose:
            print("{}: {}".format(*sys.exc_info()))
        output = command + " fail."
    return output



if __name__ == "__main__":
    main()
