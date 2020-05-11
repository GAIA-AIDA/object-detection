echo CU Object Detection begin...

if [ -z "$CORPUS" ]; then export CORPUS=/root/corpus; fi
if [ -z "$MODELS" ]; then export MODELS=/root/models; fi
if [ -z "$OUTPUT" ]; then export OUTPUT=/root/shared; fi

cd /root/src/tfobjdetect/script/
python3.6 ./deploy_037a.py 
python3.6 ./deploy_037b.py
python3.6 ./deploy_037c.py
python3.6 ./deploy_037d.py
cd /root/src/wsod/script/
python3.6 ./dpl_034a.py 
python3.6 ./dpl_034b.py 
cd /root/src/model_fusion/script/
python3.6 ./fuse_034a.py 
python3.6 ./fuse_034b.py 
python3.6 ./ex_034.py 

echo copying results to ${OUTPUT}
cp /root/src/results/aida_output_34.pkl ${OUTPUT}
cp /root/src/results/det_results_merged_34a.pkl ${OUTPUT}
cp /root/src/results/det_results_merged_34b.pkl ${OUTPUT}
echo CU Object Detection completed.

