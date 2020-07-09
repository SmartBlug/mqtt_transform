FROM python:3

RUN pip3 install paho-mqtt

COPY *.py /var/prog/
COPY tag /var/prog/
COPY conf/* /var/prog/conf/

WORKDIR /var/prog

CMD [ "python", "main.py" ]