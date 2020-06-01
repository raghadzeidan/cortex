#!/bin/bash
python -m cortex.api run-server -h '127.0.0.1' -p 5000 -d 'mongodb://127.0.0.1:27017'
