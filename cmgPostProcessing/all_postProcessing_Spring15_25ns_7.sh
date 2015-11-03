#!/bin/sh 
########Spring15###############

python cmgPostProcessing.py --skim=dilep  --samples=TTWJetsToLNu
python cmgPostProcessing.py --skim=dilep  --samples=TTZToLLNuNu
python cmgPostProcessing.py --skim=dilep  --samples=TTZToQQ
python cmgPostProcessing.py --skim=dilep  --samples=tZq_ll_4f
python cmgPostProcessing.py --skim=dilep  --samples=tZq_nunu_4f
python cmgPostProcessing.py --skim=dilep  --samples=ttHJetToNonbb
python cmgPostProcessing.py --skim=dilep  --samples=ttHJetToNonbb_ext
python cmgPostProcessing.py --skim=dilep  --samples=ttHJetTobb
python cmgPostProcessing.py --skim=dilep  --samples=ttHJetTobb_ext
python cmgPostProcessing.py --skim=dilep  --samples=ttHToNonbb_pow
