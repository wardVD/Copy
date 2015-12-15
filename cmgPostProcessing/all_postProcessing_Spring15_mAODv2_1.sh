#!/bin/sh
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_LO $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_DiLepton,TTJets_DiLepton_ext $1

