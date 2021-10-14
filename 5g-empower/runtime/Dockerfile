FROM ubuntu

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository universe
RUN apt update
RUN apt install -y python3-pip git

RUN pip3 install tornado sqlalchemy construct==2.5.5-reupload

RUN git clone https://github.com/hccresende/empower-runtime.git
RUN cd empower-runtime/; mkdir deploy; mkdir log;

WORKDIR /empower-runtime
ENTRYPOINT [ "./empower-runtime.py" ]
