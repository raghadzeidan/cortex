#!/bin/bash
sudo docker run -d --network=my-test-net -p 5672:5672 rabbitmq 
sudo docker run -d --network=my-test-net -p 27017:27017 mongo 
