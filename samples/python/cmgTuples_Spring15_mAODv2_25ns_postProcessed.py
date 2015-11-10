import copy, os, sys
from StopsDilepton.tools.localInfo import dataDir
dir = dataDir 

DY={\
"name" : "DY + Jets",
"bins" : [
"DYJetsToLL_M10to50",
"DYJetsToLL_M50",
],
'dir' : dir,
}

DY_LO={\
"name" : "DY (LO) + Jets",
"bins" : [
"DYJetsToLL_M5to50_LO",
"DYJetsToLL_M50_LO",
],
'dir' : dir,
}

DY_HT_LO={\
"name" : "DY (LO, HT) + Jets",
"bins" : [
"DYJetsToLL_M50_HT100to200",
"DYJetsToLL_M50_HT200to400",
"DYJetsToLL_M50_HT400to600",
"DYJetsToLL_M50_HT600toInf",
"DYJetsToLL_M5to50_HT100to200",
"DYJetsToLL_M5to50_HT200to400",
"DYJetsToLL_M5to50_HT400to600",
"DYJetsToLL_M5to50_HT600toInf",
],
'dir' : dir,
}


TTJets={
"name":"TTJets",
"bins":[
"TTJets",
],
'dir' : dir,
}
TTJets_LO={
"name":"TTJets (LO)",
"bins":[
"TTJets_LO",
],
'dir' : dir,
}

#"TTLep_pow",

TTJets_Lep={
"name":"TTJets (Lep)",
"bins":[
"TTJets_DiLepton_comb",
"TTJets_SingleLeptonFromTbar_comb",
"TTJets_SingleLeptonFromT_comb",
],
'dir' : dir,
}

TTJets_HT_LO={
"name":"TTJets (Lep)",
"bins":[
"TTJets_LO_HT600to800",
"TTJets_LO_HT800to1200",
"TTJets_LO_HT1200to2500",
"TTJets_LO_HT2500toInf",
],
'dir' : dir,
}

singleTop={
"name":"single T",
"bins":[
"TBar_tWch",
"TBar_tWch_DS",
"TToLeptons_sch",
"TToLeptons_tch_amcatnlo_comb",
"T_tWch",
"T_tWch_DS",
],
'dir' : dir,
}

TTX={\
"name" : "TTX",
"bins" : [
"TTHbb_comb",
"TTHnobb",
"TTWToLNu",
"TTWToQQ",
"TTZToLLNuNu",
"TTZToQQ",
"tZq_ll",
"tZq_nunu",
],
'dir' : dir,
}

WJetsToLNu={
"name":"WJetsToLNu",
"bins":[
"WJetsToLNu",
],
'dir':dir
}

WJetsToLNu_LO={
"name":"WJetsToLNu_LO",
"bins":[
"WJetsToLNu_LO",
],
'dir':dir
}

WJetsToLNu_HT={
"name":"WJetsToLNu_HT",
"bins":[
"WJetsToLNu_HT100to200",
"WJetsToLNu_HT200to400",
"WJetsToLNu_HT400to600",
"WJetsToLNu_HT600to800",
#"WJetsToLNu_HT600toInf",
"WJetsToLNu_HT800to1200",
"WJetsToLNu_HT1200to2500",
"WJetsToLNu_HT2500toInf",
],
'dir':dir
}

diBoson={
"name":"diBoson",
"bins":[
#"VVTo2L2Nu",
"WWTo2L2Nu",
"WWToLNuQQ",
"WZTo1L1Nu2Q",
"WZTo2L2Q",
"ZZTo2L2Q",
"ZZTo2Q2Nu",
],
'dir':dir
}
triBoson={
"name":"triBoson",
"bins":[
"WWZ",
"WZZ",
"ZZZ",
],
'dir':dir
}

QCD_HT={\
"name" : "QCD (HT binned)",
"bins" : [
"QCD_HT100to200",
"QCD_HT200to300",
"QCD_HT300to500",
"QCD_HT500to700",
"QCD_HT700to1000",
"QCD_HT1000to1500",
"QCD_HT1500to2000",
"QCD_HT2000toInf",
],
'dir' : dir,
}

QCD_Mu5={\
"name" : "QCD (Mu5)",
"bins" : [
#"QCD_Pt15to20_Mu5",#omit
"QCD_Pt20to30_Mu5",
"QCD_Pt50to80_Mu5",
"QCD_Pt80to120_Mu5",
"QCD_Pt120to170_Mu5",
"QCD_Pt170to300_Mu5",
"QCD_Pt300to470_Mu5",
"QCD_Pt470to600_Mu5",
"QCD_Pt600to800_Mu5",
"QCD_Pt800to1000_Mu5",
"QCD_Pt1000toInf_Mu5",
],
'dir' : dir,
}

QCD_EMbcToE={\
"name" : "QCD (EM+bcToE)",
"bins" : [
"QCD_Pt_15to20_bcToE",
"QCD_Pt_20to30_bcToE",
"QCD_Pt_30to80_bcToE",
"QCD_Pt_80to170_bcToE",
"QCD_Pt_170to250_bcToE",
"QCD_Pt_250toInf_bcToE",
"QCD_Pt15to20_EMEnriched",
"QCD_Pt20to30_EMEnriched",
"QCD_Pt30to50_EMEnriched",
"QCD_Pt50to80_EMEnriched",
"QCD_Pt80to120_EMEnriched",
"QCD_Pt120to170_EMEnriched",
"QCD_Pt170to300_EMEnriched",
"QCD_Pt300toInf_EMEnriched",
],
'dir' : dir,
}



QCD_Pt={\
"name" : "QCD",
"bins" : [
"QCD_Pt10to15",
"QCD_Pt15to30",
"QCD_Pt30to50",
"QCD_Pt50to80",
"QCD_Pt80to120",
"QCD_Pt120to170",
"QCD_Pt170to300",
"QCD_Pt300to470",
"QCD_Pt470to600",
"QCD_Pt600to800",
"QCD_Pt800to1000",
"QCD_Pt1000to1400",
"QCD_Pt1400to1800",
"QCD_Pt1800to2400",
"QCD_Pt2400to3200",
"QCD_Pt3200",
],
'dir' : dir,
}
