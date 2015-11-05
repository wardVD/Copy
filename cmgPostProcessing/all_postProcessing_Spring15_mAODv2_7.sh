#!/bin/sh
python cmgPostProcessing.py --skim=dilep  --samples=WWTo2L2Nu
python cmgPostProcessing.py --skim=dilep  --samples=WWToLNuQQ

python cmgPostProcessing.py --skim=dilep  --samples=ZZTo2L2Q
python cmgPostProcessing.py --skim=dilep  --samples=ZZTo2Q2Nu

python cmgPostProcessing.py --skim=dilep  --samples=WZTo1L3Nu
python cmgPostProcessing.py --skim=dilep  --samples=WZTo1L1Nu2Q
python cmgPostProcessing.py --skim=dilep  --samples=WZTo2L2Q

python cmgPostProcessing.py --skim=dilep  --samples=VVTo2L2Nu

python cmgPostProcessing.py --skim=dilep  --samples=WWZ
python cmgPostProcessing.py --skim=dilep  --samples=WZZ
python cmgPostProcessing.py --skim=dilep  --samples=ZZZ

python cmgPostProcessing.py --skim=dilep  --samples=TTWToLNu
python cmgPostProcessing.py --skim=dilep  --samples=TTWToQQ
python cmgPostProcessing.py --skim=dilep  --samples=TTZToQQ
python cmgPostProcessing.py --skim=dilep  --samples=TTZToLLNuNu

