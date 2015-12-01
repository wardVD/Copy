#!/bin/sh

python cmgPostProcessing.py --keepPhotons --skim=inclusive $1  --samples=GJets_HT40to100  &
python cmgPostProcessing.py --keepPhotons --skim=inclusive $1  --samples=GJets_HT100to200  &
python cmgPostProcessing.py --keepPhotons --skim=inclusive $1  --samples=GJets_HT200to400  &
python cmgPostProcessing.py --keepPhotons --skim=inclusive $1  --samples=GJets_HT400to600  &
python cmgPostProcessing.py --keepPhotons --skim=inclusive $1  --samples=GJets_HT600toInf  &

#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt15to20_Mu5 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt20to30_Mu5 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt30to50_Mu5 

#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt50to80_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt80to120_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt120to170_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt170to300_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt300to470_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt470to600_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt600to800_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt800to1000_Mu5 
#python cmgPostProcessing.py --skim=inclusive  $1 --samples=QCD_Pt1000toInf_Mu5 

#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt15to20_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt20to30_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt30to50_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt50to80_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt80to120_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt120to170_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt170to300_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt300toInf_EMEnriched 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_15to20_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_20to30_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_30to80_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_80to170_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_170to250_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=QCD_Pt_250toInf_bcToE 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=TTJets 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=TToLeptons_tch_amcatnlo,TToLeptons_tch_amcatnlo_ext 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=TToLeptons_sch_amcatnlo 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=TBar_tWch 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=T_tWch 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=DYJetsToLL_M10to50 
#python cmgPostProcessing.py --skim=inclusive $1  --samples=DYJetsToLL_M50 
