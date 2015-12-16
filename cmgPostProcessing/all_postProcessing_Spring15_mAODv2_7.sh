#!/bin/sh

python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WWTo2L2Nu   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WWToLNuQQ   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=ZZTo2L2Q   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=ZZTo2Q2Nu   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WZTo1L1Nu2Q   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WZTo2L2Q   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=VVTo2L2Nu   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WZTo3LNu   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=WGToLNuG   &
python cmgPostProcessing.py --skim=dilepTiny  $1 --samples=ZGTo2LG   &
