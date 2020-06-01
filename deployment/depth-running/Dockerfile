FROM python:3

WORKDIR /
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD cortex/ ./cortex/

ADD scripts/depth_image_parser.sh . 

CMD [ "bash", "depth_image_parser.sh" ]
