#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --skim=dilep  --samples=DoubleEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep  --samples=DoubleMuon_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep  --samples=MuonEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep  --samples=DoubleEG_Run2015D_05Oct &
python cmgPostProcessing.py --skim=dilep  --samples=DoubleMuon_Run2015D_05Oct &
python cmgPostProcessing.py --skim=dilep  --samples=MuonEG_Run2015D_05Oct &
