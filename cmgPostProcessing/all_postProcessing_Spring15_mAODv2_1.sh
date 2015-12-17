#!/bin/sh
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_LO &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_DiLepton,TTJets_DiLepton_ext &

