import re
import zlib
import cv2

from scapy.all import *

pic_dir = "/home/yanganto/pics"
faces_dir = "/home/yanganto/pics/faces"
pcap_file = "arper.pcap"

def http_assembler(pcap_file):
    caved_images = 0
    faces_detected = 0
    a = rdpcap(pcap_file)
    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        
        for packet in sessions[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:

                    # reassemble stream
                    http_payload += packet[TCP].payload
            
            except:
                pass
            headers = get_http_headers(http_payload)

            if headers is None:
                continue

            img, img_type = extract_image(headers, http_payload)

            if img is not None and img_type is not None:

                # saving image
                fname = "{}_pic_carver_{}.{}".format(pcap_file, caved_images, img_type)
                fd = open( pic_dir + '/' + fname, "wb")
                fd.write(img)
                fd.close()

                caved_images += 1

                # discover face
                try:
                    result = faces_detected( pic_dir + '/' + fname, fname)
                    
                    if result:
                        faces_detected += 1
                except:
                    pass
    return caved_images, faces_detected

print("Extracted: {} images.".format(carved_images))
print("Detected: {} faces.".format(faces_detected))

