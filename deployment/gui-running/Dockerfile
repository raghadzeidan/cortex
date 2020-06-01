FROM python:3

WORKDIR /
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ADD cortex/ ./cortex/
ADD scripts/gui.sh . 
EXPOSE 8080
CMD [ "bash", "gui.sh" ]
