#!/bin/sh
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWTo2L2Nu $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWToLNuQQ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZTo2L2Q $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZTo2Q2Nu $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo1L3Nu $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo1L1Nu2Q $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo2L2Q $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=VVTo2L2Nu $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWZ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZZ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZZ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTWToLNu $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTWToQQ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTZToQQ $1
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTZToLLNuNu $1
