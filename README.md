# Private IP Bridge

Retrive your remote machine's IP from everywhere securely.

## Philosophy

.. image:: ../design.png

## Installation

0 - Clone the repo:

`git clone git@github.com:PascalCeccaldi/private_ip_bridge.git`

1 - Remove the current git remote:

`cd private_ip_bridge && rm -rf .git`

2 - Initialize your own remote git repository in order to access it.
This steps depends on your git server's configuration.

E.g. with GitHub, create a private repository and add its remote to your local private_ip_bridge directory

## Run the App

0. If not already installed, please install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

1. Install the project's Python environment by running the following command:

`conda env create -f environment.yml -n **your_env_name** && conda activate **your_env_name**`

### Main application

You need to call the program with a name for a branch in argument.
Indeed, your IPs will be stored on a separate branch from the main code.
Also, you can create multiple branches if you want to have a specific organization for storing your IPs.

To run application for the first time, on top of the name of the branch, you need to use the **--force True** parameters in order to create the branch:

`python main.py **your_branch_name** --force True`

If the branch already exists, you can simply use:

`python main.py **your_branch_name**`

Then, you can access the visual interface by connecting to [localhost:8000](http://localhost:8000)

### Push IPs

You can manually push IPs by going on [localhost:8000/push_local_ips](http://localhost:8000/push_local_ips)

In order to launch a background job that will track the evolution of your IP, please run:

`python main.py **your_branch_name** --background True`

This command will push your IP to your repository anytime it changes.

You can specify a computer name by using the **--computer-name option** such as:

`python main.py **your_branch_name** --background True --computer-name your_computer_name`

### Read IPs

To read the IP of a given computer, stored on a given branch of your repository, please launch the app first by specifying the computer name:

`python main.py **your_branch_name** --computer-name your_computer_name`

Then, go to [localhost:8000/remote_access](http://localhost:8000/remote_access) and click on **Get remote IPs**
This will read the encrypted file on your repository and decypher it locally for you to be able to read your remote computer's IP
