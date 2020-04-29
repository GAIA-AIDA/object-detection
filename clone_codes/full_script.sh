echo CU Object Detection begin...
cd /object-detection/src/test/jpg
find . -name '*.jpg*' > /object-detection/src/test/jpg.txt
cd /object-detection/src/test/keyframe
find . -name '*.jpg*' > /object-detection/src/test/keyframe.txt
cd /object-detection/src/tfobjdetect/script/
python ./deploy_037a.py 
python ./deploy_037b.py
python ./deploy_037c.py
python ./deploy_037d.py
cd /object-detection/src/wsod/script/
python ./dpl_034a.py 
python ./dpl_034b.py 
cd /object-detection/src/model_fusion/script/
python ./fuse_034a.py 
python ./fuse_034b.py 
python ./ex_034.py 

echo copying results to ${OUTPUT}
cp /object-detection/src/results/aida_output_34.pkl ${OUTPUT}
cp /object-detection/src/results/det_results_merged_34a.pkl ${OUTPUT}
cp /object-detection/src/results/det_results_merged_34b.pkl ${OUTPUT}
echo CU Object Detection completed.

#echo Which of these is the three?
#./results/det_results_m18_jpg_oi_1.pkl
#./results/det_results_m18_jpg_oi_1_filtered.pkl
#./results/det_results_m18_jpg_coco_1.pkl
#./results/det_results_m18_jpg_coco_1_filtered.pkl
#./results/det_results_m18_kf_oi_1.pkl
#./results/det_results_m18_kf_oi_1_filtered.pkl
#./results/det_results_m18_kf_coco_1.pkl
#./results/det_results_m18_kf_coco_1_filtered.pkl
#./results/det_results_ws_jpg_dpl_034a.pkl
#./results/det_results_ws_kf_dpl_034b.pkl
#./results/det_results_concat_34a.pkl
#./results/det_results_merged_34a.pkl
#./results/det_results_concat_34b.pkl
#./results/det_results_merged_34b.pkl
#./results/aida_output_34.pkl
