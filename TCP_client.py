import socket


# TCP
# connect, send, recv
print('{:=^30}'.format("TCP"))
target_host ="www.google.com"
target_port = 80

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# http://yangrong.blog.51cto.com/6945369/1339593
# AF_INET for a IPv4 server
# SOCKET_STREAM means a client

client.connect((target_host, target_port))

client.send( b"GET / HTTP1.1\r\n" + 
             b"Host: google.com\r\n" +
             b"\r\n"
        )

response = client.recv(4096)

print(response)

