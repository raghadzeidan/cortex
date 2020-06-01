FROM python:3

WORKDIR /
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD cortex/ ./cortex/

ADD scripts/saver.sh . 

CMD [ "bash", "saver.sh" ]
