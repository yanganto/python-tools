import socket
import paramiko
import threading
import sys

host_key = paramiko.RSAKey(filename='test.rsa')
USERNAME = 'test'
PASSWORD = 'password'
time_out = 20

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if username == USERNAME and password == PASSWORD:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

addr_li = sys.argv[1].split(':')
ip = addr_li.pop(0)
port = int(addr_li[0]) if addr_li else 22

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((ip, port))
    sock.listen(50)
    print("listening at {}:{}".format(ip, port))
    client, addr = sock.accept()
except:
    print(sys.exc_info())
    sys.exit(1)
print("Connected!")

try:
    session = paramiko.Transport(client)
    session.add_server_key(host_key)
    server = Server()
    try:
        session.start_server(server=server)
    except paramiko.SSHException:
        print("SSH negotiation false!")
    chan = session.accept(time_out)
    if chan:
        print("Authenticated!")
    print(chan.recv(1024))
    chan.send(b"Welcom to ssh_server")
    while True:
        try:
            command = input("Enter command: ").rstrip('\n')
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024))
            else:
                chan.send('exit')
                print("Exiting..")
                session.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            session.close()
except:
    print("Exception: {}".format(sys.exc_info()))
    try:
        session.close()
    except:
        pass
    sys.exit(1)






