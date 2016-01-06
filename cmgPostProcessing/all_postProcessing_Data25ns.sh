#!/bin/sh 
########Spring15###############
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=DoubleEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=DoubleEG_Run2015D_05Oct &
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=DoubleMuon_Run2015D_Promptv4 &
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=DoubleMuon_Run2015D_05Oct &
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=MuonEG_Run2015D_Promptv4 &
python cmgPostProcessing.py --skipVariations --keepPhotons --skim=$1 $2 --samples=MuonEG_Run2015D_05Oct &
