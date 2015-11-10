#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --skim=dilep $1  --samples=DoubleEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep $1  --samples=DoubleEG_Run2015D_05Oct &
python cmgPostProcessing.py --skim=dilep $1  --samples=DoubleMuon_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep $1  --samples=DoubleMuon_Run2015D_05Oct &
python cmgPostProcessing.py --skim=dilep $1  --samples=MuonEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skim=dilep $1  --samples=MuonEG_Run2015D_05Oct &
