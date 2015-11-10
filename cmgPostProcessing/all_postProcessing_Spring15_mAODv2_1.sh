#!/bin/sh
python cmgPostProcessing.py --skim=dilep $1  --samples=TTJets
python cmgPostProcessing.py --skim=dilep $1  --samples=TTJets_LO

