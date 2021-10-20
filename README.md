# Private IP Bridge

Retrive your remote machine's IP from everywhere securely.

## Philosophy
![alt text](https://github.com/PascalCeccaldi/private_ip_bridge/blob/master/design.jpeg)

## Installation

0 - Clone the repo:

`git clone git@github.com:PascalCeccaldi/private_ip_bridge.git`

1 - Remove the current git remote:

`cd private_ip_bridge && rm -rf .git`

2 - Initialize a new remote git repository in order to access it privately.
This steps depends on your git server's configuration.

E.g. with GitHub, create a private repository and add its remote to the private_ip_bridge directory.

## Run the App

0. If not already installed, please install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

1. Install the project's Python environment:

`conda env create -f environment.yml -n your_env_name && conda activate your_env_name`

You need to call the program with a branch name in argument, in order to store your IPs on separate branches from master.

If you run the application for the first time, you need to add the **--force True** parameters in order to create the branch:

`python main.py your_branch_name --force True`

If the branch already exists, you can simply use:

`python main.py your_branch_name`

Then, you can access the visual interface at [localhost:8000](http://localhost:8000)

## Push IPs

You can manually push IPs at [localhost:8000/push_local_ips](http://localhost:8000/push_local_ips)

Also, you can run a background job that will track the evolution of your IP:

`python main.py your_branch_name --background True`

You can identify the current computer by using **--computer-name**:

`python main.py your_branch_name --background True --computer-name your_computer_name`

Before being pushed, your IPs are locally encrypted with a passphrase, using **~/.ssh/id_rsa.pub** by default.

You can specify a passphrase by using **--public-key-path**:

`python main.py your_branch_name --public-key-path path_to_passphrase`

**IMPORTANT: this passphrase needs to be accesible on all computers from where you wish to cypher/decypher your IPs.**

## Read IPs

To read the IP of a given computer, stored on a given branch:

`python main.py your_branch_name --computer-name your_computer_name`

Then, go to [localhost:8000/remote_access](http://localhost:8000/remote_access) and click on **Get remote IPs**.

This will read the encrypted file on your repository and decypher it locally for you to be able to read your remote computer's IP.
