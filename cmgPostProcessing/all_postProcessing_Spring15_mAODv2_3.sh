#!/bin/sh

python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_LO_HT600to800 &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_LO_HT800to1200 &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_LO_HT1200to2500 &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTJets_LO_HT2500toInf &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTHnobb &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTHnobb_pow &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTHnobb_mWCutfix_ch0 &
python cmgPostProcessing.py --skim=$1 $2  --samples=TTHbb,TTHbb_ext1,TTHbb_ext2,TTHbb_ext3 &
