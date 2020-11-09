# AIDA Object Detection

Source provided by Alireza Zareian

-----
To build and run the system:

```
$ INPUT=/path/to/ldc/corpus
$ OUTPUT=/path/to/output/directory
$ GPU_ID=[a single integer index to the GPU]

$ chmod +x ./full_script.sh
$ docker build . --tag [TAG]
$ CONTAINER_ID=`docker run -itd -v ${INPUT}:/root/input:ro -v ${OUTPUT}:/root/output \
                -e CUDA_VISIBLE_DEVICES=${GPU_ID} --gpus=<NUMBER_OF_GPUS_ON_MACHINE> --name aida-cu-od [TAG] /bin/bash`
$ docker exec -it ${CONTAINER_ID} /bin/bash

root@7606a206e587:~/src# . ./full_script.sh 

```

If `/path/to/output/directory/columbia_vision_shared/aida_output_34.pkl` (and two other files) exists, it means the system has run successfully.

Optionally, you may mount `INPUT` and `OUTPUT` on different paths, in which case you should pass the new paths to `docker run` using `-e INPUT=/new/corpus/path`, etc.


