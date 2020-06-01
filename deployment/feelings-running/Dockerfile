FROM python:3

WORKDIR /
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD cortex/ ./cortex/

ADD scripts/feelings_parser.sh . 

CMD [ "bash", "feelings_parser.sh" ]
