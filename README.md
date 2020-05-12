# AIDA Object Detection

Source provided by Alireza Zareian

-----
To build and run the system:

```
$ CORPUS=/path/to/ldc/corpus
$ OUTPUT=/path/to/columbia_data_root/columbia_vision_shared
$ MODELS=/path/to/columbia_data_root/columbia_object_detection_models
$ GPU_ID=[a single integer index to the GPU]

$ chmod +x ./full_script.sh
$ docker build . --tag [TAG]
$ CONTAINER_ID=`docker run -itd -v ${CORPUS}:/root/corpus -v ${OUTPUT}:/root/output -v ${MODELS}:/root/models \
                -e CUDA_VISIBLE_DEVICES=${GPU_ID} --gpus=${GPU_ID} --name aida-cu-od [TAG] /bin/bash`
$ docker exec -it ${CONTAINER_ID} /bin/bash

root@7606a206e587:~/src# . ./full_script.sh 

```

If `/path/to/columbia_data_root/columbia_vision_shared/aida_output_34.pkl` (and two other files) exists, it means the system has run successfully.

Optionally, you may mount `CORPUS`, `OUTPUT`, and/or `MODELS` on different paths, in which case you should pass the new paths to `docker run` using `-e CORPUS=/new/corpus/path`, etc.


