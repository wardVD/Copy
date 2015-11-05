#!/bin/sh
python cmgPostProcessing.py --skim=dilep  --samples=TToLeptons_tch_amcatnlo,TToLeptons_tch_amcatnlo_ext $1
python cmgPostProcessing.py --skim=dilep  --samples=TToLeptons_sch_amcatnlo $1
python cmgPostProcessing.py --skim=dilep  --samples=TBar_tWch $1
python cmgPostProcessing.py --skim=dilep  --samples=TBar_tWch_DS $1
python cmgPostProcessing.py --skim=dilep  --samples=T_tWch $1
python cmgPostProcessing.py --skim=dilep  --samples=T_tWch_DS $1
python cmgPostProcessing.py --skim=dilep  --samples=tZq_ll $1
python cmgPostProcessing.py --skim=dilep  --samples=tZq_nunu $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu $1
python cmgPostProcessing.py --skim=dilep  --samples=WJetsToLNu_LO $1
