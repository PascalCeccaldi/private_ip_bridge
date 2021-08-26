
import re
import git
import hmac
import time
import socket
import datetime
from git.objects import commit
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

def read_paper_list(paper_list: str):
    paper_list = paper_list.split(', ')
    new_list = []
    for item in paper_list:
        new_list.append(item.split('\'')[1])
    return new_list

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

def read_file(fname: str, key_path: str = ''):
    if not os.path.isfile(fname):
        return '{} does not exist.'.format(fname)
    with open(fname, 'r') as f: 
        stored_hips = f.read()
        hips = read_paper_list(stored_hips)
    f.close()
    if len(key_path):
        ips = ip_decoder(hips, key_path)
        return ips
    return hips

def check_updates(hips: list, fname: str):
    if hips == read_file(fname):
        return True
    return False

def auto_commit(hips: list, branch: str,
                repo_path: str, computer_name: str,
                force=False):
    fname = computer_name + '.txt'
    if check_updates(hips, fname):
        return None
    with open(fname, 'w+') as f:
        f.write(str(hips))
    f.close()
    g = git.Git(repo_path)
    if not check_branch(branch, g, force):
        return 'branch {} does not exist'.format(branch)
    repo = git.Repo(repo_path)
    for remote in repo.remotes:
        remote.fetch()
    commit_message = 'Hashed IPs updated from {}'.format(computer_name)
    g.add(fname)
    g.commit(m=commit_message)

    repo.git.push('--set-upstream', 'origin', branch)
    return commit_message

def check_branch(branch: str, g: git.Git, force: bool = False):
    all_branches = g.branch("--all").split()
    if branch not in all_branches:
        print('warning: branch {} does not exist'.format(branch))
        if not force:
            print('Last action will be ignored due to warning.')
            print('Please create your branch manually or use -f option')
            print('To force branch creation please use the following:')
            print('python main.py your_branch --force True')
            return False
        g.checkout('HEAD', b=branch) 
    g.checkout(branch)
    return True


def decode_computer_ips(key_path: str, branch: str,
                        repo_path: str, computer_name: str,
                        force: bool = False):

    g = git.Git(repo_path)
    if not check_branch(branch, g, force):
        return 'branch {} does not exist'.format(branch)
    g.pull('origin', branch)
    repo = git.Repo(repo_path)
    for remote in repo.remotes:
        remote.fetch()
    fname = computer_name + '.txt'
    return read_file(fname, key_path)


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

def ip_listener(freq: int = 60,
                oneshot: bool = False,
                key_path: str = '',
                branch: str = 'tmp',
                repo_path: str = '',
                computer_name: str = "Al",
                force: bool = False):
    
    print('Bot Listening to your ip..')
    print('To quit, press CTRL+C')
    print('...')
    
    old_ips = []
    current_ips = []
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
                    auto_commit(hashed_ips, branch,
                                repo_path, computer_name,
                                force=force)
            old_ips = current_ips
            if oneshot:
                return hashed_ips if len(key_path) else current_ips
        time.sleep(freq)
        