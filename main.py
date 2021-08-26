import argparse
from flask import Flask, render_template, request
app = Flask(__name__)

from bridge_components import ip_listener, ip_decoder, decode_computer_ips


@app.route('/get_ips', methods=['POST'])
def get_ips():
    ips = str(ip_listener(1, oneshot=True))
    return render_template('push_local_ips.html', ips=ips)

@app.route('/get_hashed_ips', methods=['POST'])
def get_hashed_ips():
    hips = str(ip_listener(1, oneshot=True, key_path=key_p))
    return render_template('push_local_ips.html', hips=hips)

@app.route('/decode_hips', methods=['POST'])
def decode_hips():
    hips = request.form['hips']
    if not len(hips):
        return render_template('index.html')
    ips = ip_decoder(hips, key_path=key_p)
    return render_template('push_local_ips.html', ips=ips)

@app.route('/hips_push', methods=['POST'])
def hips_push():
    ips = str(ip_listener(60, oneshot=True, key_path=key_p,
                          branch=your_branch, repo_path=repo_p,
                          computer_name=computer_n,
                          force=force))
    return render_template('push_local_ips.html')

@app.route('/continuous_hips_push', methods=['POST'])
def continuous_hips_push():
    ips = str(ip_listener(60, key_path=key_p, branch=your_branch,
                          repo_path=repo_p, computer_name=computer_n,
                          force=force))
    return render_template('push_local_ips.html')

@app.route('/access_ips', methods=['POST'])
def read_remote_ips(computer_name: str = 'Al'):
    ips = str(decode_computer_ips(key_path=key_p,
                                  branch=your_branch,
                                  repo_path=repo_p,
                                  computer_name=computer_n))
    return render_template('remote_access.html', ips=ips)


@app.route('/push_local_ips')
def local_access():
    return render_template('push_local_ips.html')

@app.route('/remote_access')
def remote_access():
    return render_template('remote_access.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('your_branch', type=str)
    parser.add_argument('--public-key-path', type=str,
                        default="/Users/pascalceccaldi/.ssh/id_rsa_ips.pub")
    parser.add_argument('--repository-path', type=str,
                        default='.')
    parser.add_argument('--computer-name', type=str,
                        default='Al')
    parser.add_argument('--force',type=bool,
                        default=False)
    args = parser.parse_args()
    
    your_branch = args.your_branch
    key_p = args.public_key_path
    repo_p = args.repository_path
    computer_n = args.computer_name
    force = args.force
    app.run(host='127.0.0.1', port=8000, debug=True)