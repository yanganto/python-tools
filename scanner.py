import threading
import ipaddress
import time
import socket
import os 
import struct
import ctypes
import sys

host = "192.168.2.101"

subnet = "192.168.2.0/24"

# magic string check in ICMP
magic_message = b"PYTHONRULES!"


# UDP datagram
def udp_sender(subnet, magic_string):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in ipaddress.ip_network(subnet):
        try:
            sender.sendto(magic_string, (str(ip), 65212))
        except:
            print("sending {} fail: {}".format(ip, sys.exc_info()))


# 64-bit machine
class IP(ctypes.Structure):
    _fields_ =[
        ('ihl', ctypes.c_uint8, 4),
        ('version', ctypes.c_uint8, 4),
        ('tos', ctypes.c_uint8),
        ('len', ctypes.c_uint16),
        ('id', ctypes.c_uint16),
        ('offset', ctypes.c_uint16),
        ('ttl', ctypes.c_uint8),
        ('protocol_num', ctypes.c_uint8),
        ('sum', ctypes.c_uint16),
        ('src', ctypes.c_uint32),
        ('dst', ctypes.c_uint32)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = { 1: 'ICMP', 6: 'TCP', 17: 'UDP'}

        self.src_addr = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_addr = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

class ICMP(ctypes.Structure):
    _fields_=[
        ('type', ctypes.c_uint8),
        ('code', ctypes.c_uint8),
        ('checksum', ctypes.c_uint16),
        ('unused', ctypes.c_uint16),
        ('next_hup_mtu', ctypes.c_uint16)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

#get header
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

t = threading.Thread(target=udp_sender, args=(subnet, magic_message))
t.start()

try:
    while True:
        raw_buffer = sniffer.recvfrom(65565)[0]

        ip_header = IP(raw_buffer[0:32])
        #print("Protocol: {} {} -> {}".format(ip_header.protocol, ip_header.src_addr, ip_header.dst_addr))

        if ip_header.protocol == 'ICMP':
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + ctypes.sizeof(ICMP)]
            icmp_header = ICMP(buf)
            #print("ICMP -> type: {}, Code: {}".format(icmp_header.type, icmp_header.code))

        # Check up type=3 and code=3
        if icmp_header.code == 3 and icmp_header.type == 3:

            # Check the response is in subnet
            if ipaddress.ip_address(ip_header.src_addr) in ipaddress.ip_network(subnet):
                print("Host Up: {}".format(ip_header.src_addr))
                if raw_buffer[ len(raw_buffer) - len(magic_message):] == magic_message:
                    print("Host Up: {}".format(ip_header.src_addr))

except KeyboardInterrupt:

    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

