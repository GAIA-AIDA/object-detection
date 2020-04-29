FROM python:3.6.3

LABEL maintainer='Dan Napierski (ISI) <dan.napierski@toptal.com>'

# Create app directory
WORKDIR /object-detection/src/

# Install app dependencies
RUN apt-get upgrade && apt-get -y update && apt-get -y install apt-utils && apt-get -y install unzip nano tree git python-pil python-lxml python-tk
RUN pip install --upgrade pip

WORKDIR /object-detection/src/lib
RUN git clone --branch v1.12.0 https://github.com/tensorflow/models.git
RUN git clone --branch tag/v1.0.3 https://github.com/NextCenturyCorporation/AIDA-Interchange-Format.git
ENV PYTHONPATH=/usr/local/bin/python:/object-detection/src/lib/models/research:/object-detection/src/lib/models/research/slim:/object-detection/src/lib/AIDA-Interchange-Format/python:.

WORKDIR /object-detection/src/lib/models/research
RUN wget -O protobuf.zip https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
RUN unzip protobuf.zip
RUN ./bin/protoc object_detection/protos/*.proto --python_out=.

WORKDIR /object-detection/src/
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Confirm Tensorflow Object Detection API installation
RUN python /object-detection/src/lib/models/research/object_detection/builders/model_builder_test.py

# Bundle app source
COPY . .

WORKDIR /corpus/
ENV CORPUS="/corpus/"

# NOTE: ./.bigfiles/ should contain model files not in github
#WORKDIR /models/
#COPY ./.bigfiles/ .
#ENV MODELS="/models/"

WORKDIR /output/
ENV OUTPUT="/output/"

WORKDIR /object-detection/src/

LABEL name="AIDA Object Detection"
LABEL version=0
LABEL revision=1

CMD [ "/bin/bash", "" ]
