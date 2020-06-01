#!/bin/bash
python -m cortex.server run-server -h '0.0.0.0' 'rabbitmq://raghd_mq:5672/' 
