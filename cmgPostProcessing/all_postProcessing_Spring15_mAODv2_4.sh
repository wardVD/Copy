#!/bin/sh
python cmgPostProcessing.py --skim=dilepTiny  --samples=TToLeptons_tch_amcatnlo,TToLeptons_tch_amcatnlo_ext $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TToLeptons_sch_amcatnlo $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TBar_tWch $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TBar_tWch_DS $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=T_tWch $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=T_tWch_DS $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=tZq_ll $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=tZq_nunu $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=WJetsToLNu $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=WJetsToLNu_LO $1
