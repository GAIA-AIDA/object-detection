FROM tensorflow/tensorflow:1.12.0-gpu-py3

MAINTAINER Dan Napierski (ISI) <dan.napierski@toptal.com>

# Create app directory
WORKDIR /root/src/

# Install app dependencie
RUN apt-get update && apt-get -y install wget curl apt-utils unzip git python-pil python-lxml python-tk software-properties-common libmysqlclient-dev build-essential libsm6 libxext6 libxrender-dev
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.6 python3.6-dev
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN pip3.6 install --upgrade pip

RUN mkdir lib
WORKDIR /root/src/lib
RUN git clone --branch v1.12.0 https://github.com/tensorflow/models.git
RUN git clone --branch tag/v1.0.3 https://github.com/NextCenturyCorporation/AIDA-Interchange-Format.git
ENV PYTHONPATH=/usr/local/bin/python:/root/src/lib/models/research:/root/src/lib/models/research/slim:/root/src/lib/AIDA-Interchange-Format/python:.

WORKDIR /root/src/lib/models/research
RUN wget -O protobuf.zip https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
RUN unzip protobuf.zip
RUN ./bin/protoc object_detection/protos/*.proto --python_out=.

RUN apt-get install nano tree

RUN mkdir /root/models
WORKDIR /root/models
RUN wget -O models.zip https://www.dropbox.com/sh/gn67jiie5luyvxe/AACJVYGciC8hrHP7j6gUOu_Ya?dl=1
RUN unzip models.zip -x /

WORKDIR /root/src/
COPY requirements.txt ./
RUN pip3.6 install -r requirements.txt

# Confirm Tensorflow Object Detection API installation
#RUN python3.6 /root/src/lib/models/research/object_detection/builders/model_builder_test.py

# Bundle app source
COPY . .

CMD [ "/bin/bash", "" ]
