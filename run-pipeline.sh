#!/bin/bash
docker build -f deployment/feelings-running/Dockerfile -t feelings .
docker build -f deployment/pose-running/Dockerfile -t pose .
docker build -f deployment/depth-running/Dockerfile -t depth .
docker build -f deployment/color-running/Dockerfile -t color .
docker build -f deployment/saver-running/Dockerfile -t saver .
docker build -f deployment/api-running/Dockerfile -t api . 
docker build -f deployment/server-running/Dockerfile -t server . 
docker build -f deployment/gui-running/Dockerfile -t gui .

docker network create --driver bridge raghd_network
docker run -itd --network=raghd_network --name raghd_mq -p 5672:5672 rabbitmq
sleep 5
docker run -itd --network=raghd_network --name db -p 27017:27017 mongo
sleep 5
docker run -itd --network=raghd_network -v volume:/volume --name feelings feelings:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name pose pose:latest 
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name depth depth:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name color color:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name saver saver:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name api -p 5000:5000 api:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name server -p 8000:8000 server:latest
sleep 2
docker run -itd --network=raghd_network -v volume:/volume --name gui -p 8080:8080 gui:latest
