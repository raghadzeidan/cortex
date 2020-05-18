#!/bin/bash
python -m cortex.saver run-saver  'mongodb://127.0.0.1:27017' 'rabbitmq://127.0.0.1:5672/'

