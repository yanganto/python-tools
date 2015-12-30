import threading
import queue
from urllib.parse import quote
import requests
import sys

threads = 50
target_url = "http://testphp.vulnweb.com"

# get from SVNdigger or get from DirBuster
word_list = "/tmp/all.txt"
resume = None

# act as Edge browser
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246" 


def build_word_list(wordlist_file):

    found_resume = False
    words = queue.Queue()

    with open(word_list, "r") as f:
        for line in f:
            words.put(line.strip())
    return words

def dir_bruter(word_queue, extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []

        # if file extension exist, check the file, else check the folder
        if "." not in attempt:
            attempt_list.append("/{}/".format(attempt))
        else:
            attempt_list.append("/" + attempt)

        # force check the file with extension
        if extensions:
            for extension in extensions:
                attempt_list.append("/" + attempt + extension)

        # try
        for brute in attempt_list:
            url = target_url + quote(brute)
            s = requests.Session()
            s.headers.update({'User-Agent': user_agent}) 
            try:
                #print('-> ' + url)
                response = s.get(url) 
                if response.status_code != 404:
                    if response.status_code >= 500:
                        print("[{}] {}".format(response.status_code, url))
                    else:
                        print("     [{}] {}".format(response.status_code, url))

            except:
                #print("[x] " + str(sys.exc_info()))
                pass

word_queue = build_word_list(word_list)
extensions = ['', '.php', '.bak', '.orig', 'inc']

for i in range(threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extensions))
    t.start()
