FROM ubuntu

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository universe
RUN apt update
RUN apt install -y python3-pip git

RUN pip3 install netaddr eventlet==0.30.2 oslo_config routes tinyrpc webob websocket-client

RUN git clone https://github.com/hccresende/empower-ryu.git

WORKDIR /empower-ryu
ENV PYTHONPATH "${PYTHONPATH}:./"
CMD ["python3", "./bin/ryu-manager", "--observe-links", "ryu.app.intent"]
