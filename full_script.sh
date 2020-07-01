echo CU Object Detection begin...

if [ -z "$INPUT" ]; then export INPUT=/root/input; fi
if [ -z "$OUTPUT" ]; then export OUTPUT=/root/output; fi
if [ -z "$OBJDET_OUTPUT" ]; then export OBJDET_OUTPUT=$OUTPUT/WORKING/columbia_vision_shared/cu_objdet_results; fi
if [ -z "$MODELS" ]; then export MODELS=/root/models; fi

export CORPUS=$INPUT

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

echo copying results to ${OBJDET_OUTPUT}
mkdir -p $OBJDET_OUTPUT
cp /root/src/results/aida_output_34.pkl ${OBJDET_OUTPUT}
cp /root/src/results/det_results_merged_34a.pkl ${OBJDET_OUTPUT}
cp /root/src/results/det_results_merged_34b.pkl ${OBJDET_OUTPUT}
echo CU Object Detection completed.

