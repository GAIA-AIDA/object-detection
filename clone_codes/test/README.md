Testing instructions.

Everything should be in github repo except the following .pb files which needs to copied manually.

```

./clone_codes/tfobjdetect/checkpoints/faster_rcnn_inception_resnet_v2_atrous_oid/frozen_inference_graph.pb
./clone_codes/tfobjdetect/checkpoints/faster_rcnn_nas_coco/frozen_inference_graph.pb

```

Example building and running 

```
$ docker build . --tag jan28-01
Sending build context to Docker daemon  1.042GB
Step 1/20 : FROM python:3.6.3
 ---> a8f7167de312
Step 2/20 : MAINTAINER Dan Napierski (ISI) <dan.napierski@toptal.com>
 ---> Using cache
 ---> 62306400abb0
Step 3/20 : WORKDIR /root/src/
 ---> Using cache
 ---> 8278bfb73f9e
Step 4/20 : RUN apt-get upgrade && apt-get update && apt-get -y install apt-utils unzip git python-pil python-lxml python-tk
 ---> Using cache
 ---> 1d949879333e
Step 5/20 : RUN pip install --upgrade pip
 ---> Using cache
 ---> d8a90d1f06b8
Step 6/20 : RUN mkdir tf
 ---> Using cache
 ---> 3249d82dc1b7
Step 7/20 : WORKDIR /root/src/tf
 ---> Using cache
 ---> 91cd6b613eec
Step 8/20 : RUN git clone https://github.com/tensorflow/models.git
 ---> Using cache
 ---> c2bf25cb90f0
Step 9/20 : ENV PYTHONPATH=/usr/local/bin/python:/root/src/tf/models/research:/root/src/tf/models/research/slim:.
 ---> Using cache
 ---> 590886d76136
Step 10/20 : WORKDIR /root/src/tf/models/research
 ---> Using cache
 ---> d5417e9c7880
Step 11/20 : RUN wget -O protobuf.zip https://github.com/protocolbuffers/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip
 ---> Using cache
 ---> 54dffa9c7004
Step 12/20 : RUN unzip protobuf.zip
 ---> Using cache
 ---> ae29cccef9b2
Step 13/20 : RUN ./bin/protoc object_detection/protos/*.proto --python_out=.
 ---> Using cache
 ---> 3b0c9a7ed422
Step 14/20 : RUN apt-get install nano tree
 ---> Using cache
 ---> 665128be62f6
Step 15/20 : WORKDIR /root/src/
 ---> Using cache
 ---> abd241b35b6a
Step 16/20 : COPY requirements.txt ./
 ---> Using cache
 ---> 404acebd7637
Step 17/20 : RUN pip install -r requirements.txt
 ---> Using cache
 ---> d8b93fbe2eeb
Step 18/20 : RUN python /root/src/tf/models/research/object_detection/builders/model_builder_test.py
 ---> Using cache
 ---> fcc80c4f12b8
Step 19/20 : COPY . .
 ---> f3fd30842745
Step 20/20 : CMD [ "/bin/bash", "" ]
 ---> Running in 99b5b0793f11
Removing intermediate container 99b5b0793f11
 ---> 85cdd7ad060c
Successfully built 85cdd7ad060c
Successfully tagged jan28-01:latest
[napiersk@vista23 clone_codes]$ docker run -itd --name d7 jan28-01 /bin/bash
af2149ea05e3db597cd1826db5c9f1a3dedf70ffb265bde8f0b0634289b2c870
[napiersk@vista23 clone_codes]$ docker exec -it d7 /bin/bash
root@af2149ea05e3:~/src# cd ./tfobjdetect/script/
root@af2149ea05e3:~/src/tfobjdetect/script# python ./deploy_037a.py 
2020-01-28 16:20:00.756255: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
root@af2149ea05e3:~/src/tfobjdetect/script# find /root/src/ -name 'det_results*'
/root/src/results/det_results_m18_jpg_oi_1.pkl
/root/src/results/det_results_m18_jpg_oi_1_filtered.pkl
root@af2149ea05e3:~/src/tfobjdetect/script# python ./deploy_037b.py 
2020-01-28 16:24:08.207393: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
root@af2149ea05e3:~/src/tfobjdetect/script# find /root/src/ -name 'det_results*'
/root/src/results/det_results_m18_jpg_oi_1.pkl
/root/src/results/det_results_m18_jpg_oi_1_filtered.pkl
/root/src/results/det_results_m18_jpg_coco_1.pkl
/root/src/results/det_results_m18_jpg_coco_1_filtered.pkl
root@af2149ea05e3:~/src/tfobjdetect/script# 
```
