import ROOT, pickle, os
from StopsDilepton.tools.btagEfficiency import *
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.tools.helpers import getChain

# get MC truth efficiencies for a specific sample
def getBTagMCTruthEfficiencies(c, cut="(1)"):
  mceff = {}
  for ptBin in ptBins:
    mceff[tuple(ptBin)] = {}
    for etaBin in etaBins:
      mceff[tuple(ptBin)][tuple(etaBin)] = {}
      etaCut = "abs(Jet_eta)>"+str(etaBin[0])+"&&abs(Jet_eta)<"+str(etaBin[1])
      ptCut = "abs(Jet_pt)>"+str(ptBin[0])
      if ptBin[1]>0:
        ptCut += "&&abs(Jet_pt)<"+str(ptBin[1])
      c.Draw("(Jet_btagCSV>0.890)>>hbQuark(100,-1,2)",cut+"&&Jet_id>0&&abs(Jet_mcFlavour)==5&&                     "+etaCut+"&&"+ptCut)
      c.Draw("(Jet_btagCSV>0.890)>>hcQuark(100,-1,2)",cut+"&&Jet_id>0&&abs(Jet_mcFlavour)==4&&                     "+etaCut+"&&"+ptCut)
      c.Draw("(Jet_btagCSV>0.890)>>hOther(100,-1,2)" ,cut+"&&Jet_id>0&&(abs(Jet_mcFlavour) < 4  || abs(Jet_mcFlavour) > 5)&&  "+etaCut+"&&"+ptCut)
      hbQuark = ROOT.gDirectory.Get("hbQuark")
      hcQuark = ROOT.gDirectory.Get("hcQuark")
      hOther = ROOT.gDirectory.Get("hOther")
      mceff[tuple(ptBin)][tuple(etaBin)]["b"]     = hbQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["c"]     = hcQuark.GetMean()
      mceff[tuple(ptBin)][tuple(etaBin)]["other"] = hOther.GetMean()
      print "Eta",etaBin,etaCut,"Pt",ptBin,ptCut,"Found b/c/other", mceff[tuple(ptBin)][tuple(etaBin)]["b"], mceff[tuple(ptBin)][tuple(etaBin)]["c"], mceff[tuple(ptBin)][tuple(etaBin)]["other"]
      del hbQuark, hcQuark, hOther
  return mceff

#for sample in [TTJets, TTJets_Lep]:
for sample in [ TTJets_Lep]:
  pickle.dump(\
    getBTagMCTruthEfficiencies(
      getChain(sample),  
      cut="(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=2&&(isMuMu==1||isEE==1||isEMu==1)"
    ), 
    file(os.path.expandvars('/afs/hephy.at/data/rschoefbeck01/StopsDilepton/btagEfficiencyData/'+sample['name']+'_2j_2l.pkl'), 'w')
  )
