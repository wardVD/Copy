#!/bin/sh

python cmgPostProcessing.py --skim=dilep  --samples=TTJets_SingleLeptonFromTbar,TTJets_SingleLeptonFromTbar_ext $1
python cmgPostProcessing.py --skim=dilep  --samples=TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromT_ext $1
python cmgPostProcessing.py --skim=dilep  --samples=TTLep_pow $1
