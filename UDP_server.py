import socket
import threading


bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((bind_ip, bind_port))

print('Listening at {0}:{1}'.format(bind_ip,bind_port))


while True:
    data, addr = server.recvfrom(1024)

    print("Received connection from {}:{}".format(*addr))
    print("Received {}".format(data))

