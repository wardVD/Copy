#!/bin/sh
python cmgPostProcessing.py --skim=dilep $1  --samples=TTJets
python cmgPostProcessing.py --skim=dilep $1  --samples=TTJets_LO
python cmgPostProcessing.py --skim=dilep  --samples=TTJets_DiLepton,TTJets_DiLepton_ext $1

