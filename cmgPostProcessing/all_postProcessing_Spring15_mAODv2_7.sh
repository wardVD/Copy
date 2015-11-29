#!/bin/sh

python cmgPostProcessing.py --skim=dilep  $1 --samples=WWTo2L2Nu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWToLNuQQ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZTo2L2Q 
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZTo2Q2Nu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo1L1Nu2Q 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo2L2Q 
python cmgPostProcessing.py --skim=dilep  $1 --samples=VVTo2L2Nu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZTo3LNu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WGToLNuG 
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZGTo2LG 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWDouble 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WpWpJJ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WWZ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=WZZ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=ZZZ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTWToLNu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTWToQQ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTZToQQ 
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTZToLLNuNu 
python cmgPostProcessing.py --skim=dilep  $1 --samples=TTGJets 
