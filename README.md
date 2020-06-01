[![Documentation Status](https://readthedocs.org/projects/cortexx/badge/?version=latest)](https://cortexx.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.com/raghadzeidan/cortex.svg?branch=master)](https://travis-ci.com/raghadzeidan/cortex)
# Advanced System Design - Cortex Project
Welcome to the Github page of the Advanced System Design Project by Raghad Zeidan.
# Prerequisites
```
Python version 3.8.0
Docker version 19.03.6+
docker-compose version 1.17.1+
```

# Installation
Cloning github repository
```
$ git clone git@github.com:raghadzeidan/cortex.git
...
$ cd cortex/
```

Run installation script and activate virtual enviroment
```
$ .  ./scripts/install.sh
...
$ source .env/bin/activate
```

Run tests to make sure everything is working ok
```
$ pytest tests/
```

# Quickstart
Use docker-compose command to run everything together at once.
```
$ docker-compose up -d
```
# Quickstart Explanation
  The final project includes a client, which streams cognition snapshots to a server, 
  which then publishes them to a message queue, where multiple parsers read the snapshot,
  parse various parts of it, and publish the parsed results, which are then saved to a database.
  The result in the database is then reflected by an API, CLI and GUI.
  
# Basic Usage
After installing everything, run the client on a ".mind" or ".mind.giz" file that represents snapshots and run:
```
$ python -m cortex.client upload-sample /path/to/file
```
After the snapshot has been updating by the client, A Graphical User Interface (GUI) is available on http://localhost:8080, as well as a Command Line Interface (CLI) by querying like such:
```
$ python -m cortex.cli get-users
[
    {"user_id": 1, "username": "Raghd Zeidan"}
]
$ python -m cortex.cli get-user 1
{
    "user_id": 1, "username": "Raghd Zeidan", "birthday": "1997-10-13", "gender": "m"
}
```
# Full Documentation of Functions and Modules
View the full documenation of modules and functions [here](https://cortexx.readthedocs.io/en/latest/).
  
  
