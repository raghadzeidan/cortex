FROM python:3

WORKDIR /
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD cortex/ ./cortex/

ADD scripts/pose_parser.sh . 

CMD [ "bash", "pose_parser.sh"]
