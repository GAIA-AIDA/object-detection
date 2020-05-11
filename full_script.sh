echo CU Object Detection begin...

if [ -z "$CORPUS" ]; then export CORPUS=/root/corpus; fi
if [ -z "$MODELS" ]; then export MODELS=/root/models; fi
if [ -z "$OUTPUT" ]; then export OUTPUT=/root/shared; fi

cp -r ${MODELS}/faster* /object-detection/src/aida_object_detection/clone_codes/tfobjdetect/checkpoints/
cp ${MODELS}/ckpt_5000 /object-detection/src/aida_object_detection/clone_codes/wsod/snapshots/train_022/

cd /object-detection/src/tfobjdetect/script/
python3.6 ./deploy_037a.py 
python3.6 ./deploy_037b.py
python3.6 ./deploy_037c.py
python3.6 ./deploy_037d.py
cd /object-detection/src/wsod/script/
python3.6 ./dpl_034a.py 
python3.6 ./dpl_034b.py 
cd /object-detection/src/model_fusion/script/
python3.6 ./fuse_034a.py 
python3.6 ./fuse_034b.py 
python3.6 ./ex_034.py 

echo copying results to ${OUTPUT}
cp /object-detection/src/results/aida_output_34.pkl ${OUTPUT}
cp /object-detection/src/results/det_results_merged_34a.pkl ${OUTPUT}
cp /object-detection/src/results/det_results_merged_34b.pkl ${OUTPUT}
echo CU Object Detection completed.

