FROM ubuntu:18.04
RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y --assume-yes install python3-pip
RUN pip3 --version
RUN apt-get install -y --assume-yes python3.8-minimal
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
ADD test.py /test.py
CMD ["echo", "RAGHD_DEBUG"]
CMD python3.8 test.py
