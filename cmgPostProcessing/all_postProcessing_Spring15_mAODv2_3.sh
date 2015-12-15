#!/bin/sh

python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_LO_HT600to800 $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_LO_HT800to1200 $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_LO_HT1200to2500 $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTJets_LO_HT2500toInf $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTHnobb $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTHnobb_pow $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTHnobb_mWCutfix_ch0 $1
python cmgPostProcessing.py --skim=dilepTiny  --samples=TTHbb,TTHbb_ext1,TTHbb_ext2,TTHbb_ext3 $1
