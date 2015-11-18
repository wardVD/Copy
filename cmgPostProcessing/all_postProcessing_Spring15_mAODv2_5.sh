#!/bin/sh
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M10to50 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_LO $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_LO --lheHTCut=100 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_LO $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_LO --lheHTCut=100 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT100to200 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT200to400 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT400to600 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M50_HT600toInf $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT100to200 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT200to400 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT400to600 $1
python cmgPostProcessing.py --skim=dilep  --samples=DYJetsToLL_M5to50_HT600toInf $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT100to200 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT200to400 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT400to600 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT600toInf $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT600to800 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT800to1200 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT1200to2500 $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_HT2500toInf $1
