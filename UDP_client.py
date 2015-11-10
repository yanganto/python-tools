import socket



# UDP
# sendto, recvfrom
print('{:=^30}'.format("UDP"))
target_host ="0.0.0.0"
target_port = 9999
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(b"Something", (target_host, target_port))

data, addr = client.recvfrom(4096)
print(data)
