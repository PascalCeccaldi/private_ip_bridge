
import re
import git
import hmac
import time
import socket
import datetime
import requests
import os.path

def fetch_ips(current_ips):    
    url = "https://duckduckgo.com?q=what+is+my+ip+address&ia=answer"
    response = requests.get(url, headers={'user-agent': 'my-app/0.0.1'})
    web_page = response.text
    
    re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
    global_ip = re.findall(re_ip, web_page)[0].split('.')

    local_ip = socket.gethostbyname(socket.gethostname()).split('.')
    return global_ip + local_ip


def auto_commit(hips: str, repo: git.Repo, computer_name: str = "Al"):
    with open(computer_name + '.txt', 'w') as f:
        f.write(str(hips))
    f.close()    
    

def decode_computer_ips(key_path: str, repo_path: str, computer_name: str):
    repo = git.Repo(repo_path)
    repo.remotes.origin.pull()
    fname = computer_name + '.txt'
    if not os.path.isfile(fname):
        return '{} does not exist.'.format(computer_name)
    with open(fname, 'r') as f: 
        stored_hips = f.read()
        hips = read_paper_list(stored_hips)
        ips = ip_decoder(hips, key_path)
    f.close()
    print(ips)
    return ips
    

def read_paper_list(paper_list: str):
    paper_list = paper_list.split(', ')
    new_list = []
    for item in paper_list:
        new_list.append(item.split('\'')[1])
    return new_list

def hash_ips(ips: str, key_path: str):
    hashes = []
    with open(key_path) as f:
        public_key = f.read()
        for fig in ips:
            msg = hmac.new(bytes(public_key, encoding='utf8'),
                            bytes(fig, encoding='utf8'),
                            digestmod='sha256')
            hashes.append(msg.hexdigest())
    f.close()
    print(hashes)
    return hashes


def ip_decoder(hashes, key_path):
    ips = []
    if type(hashes) is str:
        hashes = read_paper_list(hashes)
    with open(key_path) as f:
        public_key = f.read()
        for h in hashes:
            for i in range(256):
                msg = hmac.new(bytes(public_key, encoding='utf8'),
                               bytes(str(i), encoding='utf8'),
                               digestmod='sha256')
                if msg.hexdigest() == h:
                    break
            ips.append(str(i))
    f.close()
    print(ips)
    return ips
            
                

def ip_listener(freq: int = 60,
                oneshot: bool = False,
                key_path: str = '',
                repo_path: str = ''):
    
    print('Bot Listening to your ip..')
    print('To quit, press CTRL+C')
    print('...')
    
    old_ips = []
    current_ips = []
    if len(repo_path):
        repo = git.Repo(repo_path)
    while True:
        current_ips = fetch_ips(current_ips)
        if current_ips != old_ips:
            print(datetime.datetime.now())
            print("new ips: {}".format(current_ips))
            print('To quit, press CTRL+C')
            print('...')
            if len(key_path):
                hashed_ips = hash_ips(current_ips, key_path)
                if len(repo_path):
                    auto_commit(hashed_ips, repo)
            old_ips = current_ips
            if oneshot:
                return hashed_ips if len(key_path) else current_ips
        time.sleep(freq)
        