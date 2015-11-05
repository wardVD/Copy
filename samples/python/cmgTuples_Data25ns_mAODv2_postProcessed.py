import copy, os, sys
from StopsDilepton.tools.localInfo import dataDir
dir = dataDir 

DoubleEG_Run2015D = { "name" :"DoubleEG_Run2015D", 
"bins":[
"DoubleEG_Run2015D_05Oct",
"DoubleEG_Run2015D_v4"
],
"lumi":550.17+711.13,
}
MuonEG_Run2015D = { "name" :"MuonEG_Run2015D", 
"bins":[
"MuonEG_Run2015D_05Oct",
"MuonEG_Run2015D_v4"
],
"lumi":528.85+703.21,
}
DoubleMuon_Run2015D = { "name" : "DoubleMuon_Run2015D", 
"bins":[
"DoubleMuon_Run2015D_05Oct",
"DoubleMuon_Run2015D_v4"
],
"lumi":552.59+711.13
}

allSamples_Data25ns = [DoubleEG_Run2015D, MuonEG_Run2015D, DoubleMuon_Run2015D]
import ROOT 
for s in allSamples_Data25ns:
  s.update({ 
    'dir' : dir,
    'color':ROOT.kBlack,
    'isData':True
  })

