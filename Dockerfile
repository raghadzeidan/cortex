FROM python:3
RUN which python
RUN python --version
RUN pip install --upgrade pip
RUN pip --version
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV DISPLAY mymachine.com:0.0
ADD cortex /cortex
CMD python -m cortex.parsers run-parser color_image rabbitmq://my_rabbitmq:5672/
