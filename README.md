# BashI_RL

A grey-box reinforcement learning based tool to find command injection vulnerabilities. 

## Description

A grey box security tool to find command injection vulnerabilities in web pages. The tool uses reinforcement learning to find potential injection payloads. This was my masters thesis project. 

## Getting Started

### Dependencies

* Made to be used on unix based OS's
* Requires strace permissions to view the web services syscalls. \
* Requires python3 
* Install python3 depenendencies (after cloning the repo) using the command 
```bash
pip install -r requirements.txt
```

### Installing

* Clone the repo
```bash
git clone https://github.com/aryaman31/BashI_RL.git
```

### Executing program

* Ensure web service is running. Get the PID of the webservice. 
* To run the tool for a particular web page on the service, run the command 
```bash
python3 bash_rl.py <PID OF SERVER> <Address of server> False
```

## Authors

aryaman31