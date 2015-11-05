#!/bin/sh
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M10to50
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_LO
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_LO

python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT100to200
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT200to400
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT400to600
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT600toInf

python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT100to200
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT200to400
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT400to600
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT600toInf

python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT100to200
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT200to400
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT400to600
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT600toInf
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT600to800
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT800to1200
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT1200to2500
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT2500toInf