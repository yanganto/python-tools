import queue
import threading 
import os
import requests
import sys

threads = 5

target = "http://moodle.mcu.edu.tw/"
folder = "/tmp/web_map/moodle"
filters = [".jpg", ".png", ".gif", ".svg", ".css", ".less"]

os.chdir(folder)

web_path = queue.Queue()

for r, d, f in os.walk('.'):
    for fname in f:
        remote_path = "{}/{}".format(r, fname)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        if os.path.splitext(fname)[1] not in filters:
            web_path.put(remote_path)

def test_remote():
    s = requests.Session()
    while not web_path.empty():
        path = web_path.get()
        url = "{}/{}".format(target, path)

        try:
            response = s.get(url)

            if response.status_code != 404:
                if response.status_code >= 500:
                    print("[{}] {}".format(response.status_code, path))
                else:
                    print("     [{}] {}".format(response.status_code, path))
                #response.close()

        except:
            #print("[x] " + str(sys.exc_info()))
            pass

for i in range(threads):
    print("Spawning thread: " + str(i))
    t = threading.Thread(target=test_remote)
    t.start()


