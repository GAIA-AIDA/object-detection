# AIDA Object Detection

Source provided by Alireza Zareian

-----
Pip
```
pip install -r req.txt
```

-----
Docker

```
$ docker build . --tag [TAG]
$ docker run -itd -p [HOST_PORT]:8082 --name [CONTAINER_NAME] [TAG] /bin/bash 
$ docker cp /hostmachine/clone_codes/tfobjdetect/checkpoints/faster_rcnn_inception_resnet_v2_atrous_oid/frozen_inference_graph.pb [CONTAINER_NAME]:/root/src/tfobjdetect/checkpoints/faster_rcnn_inception_resnet_v2_atrous_oid/
$ docker cp /hostmachine/clone_codes/tfobjdetect/checkpoints/faster_rcnn_nas_coco/frozen_inference_graph.pb [CONTAINER_NAME]:/root/src/tfobjdetect/checkpoints/faster_rcnn_nas_coco/
$ docker cp /hostmachine/clone_codes/wsod/snapshots/train_022/ckpt_5000 [CONTAINER_NAME]:/root/src/wsod/snapshots/train_022
$ docker exec -it [CONTAINER_NAME] /bin/bash

root@7606a206e587:/object-detection/src# . ./full_script.sh 

2020-02-20 20:15:57.217729: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
2020-02-20 20:20:06.862943: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
2020-02-20 20:26:52.627241: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
2020-02-20 20:30:53.013550: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 AVX512F FMA
0 images processed out of 10.
Linear(in_features=2048, out_features=1000, bias=True)
./dpl_034a.py:193: UserWarning: Implicit dimension choice for softmax has been deprecated. Change the call to include dim=X as an argument.
  h_x = F.softmax(outputs)#.data.squeeze()
Linear(in_features=2048, out_features=1000, bias=True)
./dpl_034b.py:188: UserWarning: Implicit dimension choice for softmax has been deprecated. Change the call to include dim=X as an argument.
  h_x = F.softmax(outputs)#.data.squeeze()
NumericalValue
NumericalValue.Number.Number
Results
Results.NumberPercentageVotes.NumberPercentageVotes
Results.TurnoutVoters.TurnoutVoters
see /object-detection/src/results/aida_output_34.pkl
```

## To manually run the system end-to-end:

```
cd /root/src/test/jpg & find '*.jpg*' > ../jpg.txt
cd /root/src/test/keyframe & find '*.png*' > ../keyframe.txt

cd /root/src/

# Run model 1 on jpg data
python tfobjdetect/script/deploy_037a.py # (needs jpg.txt and path to jpgs) (outputs det_results_jpg_oi_filtered.pkl)

# Run model 2 on jpg data
python tfobjdetect/script/deploy_037b.py # (needs jpg.txt and path to jpgs) (outputs det_results_jpg_coco_filtered.pkl)

# Run model 1 on keyframe data
python tfobjdetect/script/deploy_037c.py # (needs keyframe.txt and masterShotBoundary.msb and path to keyframes) (outputs det_results_kf_oi_filtered.pkl AND kf_id2path.pkl)

# Run model 2 on keyframe data
python tfobjdetect/script/deploy_037d.py # (needs kf_id2path.pkl) (outputs det_results_kf_coco_filtered.pkl)

# Run model 3 on jpg data
python wsod/script/dpl_034a.py # (needs jpg.txt and path to jpgs) (outputs det_results_034a.pkl)

# Run model 3 on keyframe data
python wsod/script/dpl_034b.py # (needs kf_id2path.pkl) (outputs det_results_034b.pkl)

## Get eval_jpg_voc_detn_fin_results.pkl and eval_representative_frames_voc_detn_fin_results.pkl from Arka

# Postprocess Arka's results (disabled for now)
# python model_fusion/script/import_011.py #(needs eval_representative_frames_voc_detn_fin_results.pkl) outputs (eval_representative_frames_voc_detn_fin_results_renamed.pkl)

# Integrate jpg results
python model_fusion/script/fuse_034a.py #(needs det_results_jpg_oi_1_filtered.pkl
                                           # det_results_jpg_coco_1_filtered.pkl
                                           # det_results_ws_dpl_034a.pkl
                                           # eval_jpg_voc_detn_fin_results.pkl)
                                           #(outputs det_results_merged_034a.pkl)


# Integrate keyframe results
python model_fusion/script/fuse_034b.py #(needs det_results_kf_oi_1_filtered.pkl
                                           # det_results_kf_coco_1_filtered.pkl
                                           # det_results_dpl_034b.pkl
                                           # eval_representative_frames_voc_detn_fin_results_renamed.pkl) 
                                           #(outputs det_results_merged_034b.pkl)


# Integrate all results and postprocess to prepare it for AIF
python model_fusion/script/ex_034.py #(needs det_results_merged_034a.pkl and det_results_merged_034b.pkl) (outputs aida_output_34.pkl)


## send aida_output_34.pkl to Brian's system 
```
