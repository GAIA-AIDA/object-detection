cd /object-detection/src/test/jpg & find '*.jpg*' > ../jpg.txt
cd /object-detection/src/test/keyframe & find '*.png*' > ../keyframe.txt

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
echo see /object-detection/src/results/aida_output_34.pkl

