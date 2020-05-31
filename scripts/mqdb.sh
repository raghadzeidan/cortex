#!/bin/bash
sudo docker run -ti -p 5672:5672 rabbitmq --net=bridge
sudo docker run -d -p 27017:27017 mongo --net=bridge
