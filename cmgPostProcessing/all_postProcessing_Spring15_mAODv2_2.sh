#!/bin/sh

python cmgPostProcessing.py --skim=dilep  --samples=TTJets_SingleLeptonFromTbar,TTJets_SingleLeptonFromTbar_ext
python cmgPostProcessing.py --skim=dilep  --samples=TTJets_SingleLeptonFromT,TTJets_SingleLeptonFromT_ext
python cmgPostProcessing.py --skim=dilep  --samples=TTJets_DiLepton,TTJets_DiLepton_ext
python cmgPostProcessing.py --skim=dilep  --samples=TTLep_pow
