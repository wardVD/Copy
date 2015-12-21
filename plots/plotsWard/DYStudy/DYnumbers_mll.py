import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()
import numpy, os, glob

from math import *
from StopsDilepton.tools.helpers import getChain, getObjDict, getEList, getVarValue, genmatching, latexmaker_1, piemaker, getWeight, deltaPhi
from StopsDilepton.tools.objectSelection import getLeptons, looseMuID, looseEleID, getJets, getGenParts, getGoodLeptons, getGoodElectrons, getGoodMuons
from StopsDilepton.tools.localInfo import *
from StopsDilepton.tools.mt2Calculator import mt2Calculator
from StopsDilepton.tools.puReweighting import getReweightingFunction
puReweightingFunc = getReweightingFunction(era="doubleMu_onZ_isOS_1200pb_nVert_reweight_ttbar+DY")
puReweighting = lambda c:puReweightingFunc(getVarValue(c, "nVert"))

mt2Calc = mt2Calculator()


#######################################################
#        SELECT WHAT YOU WANT TO DO HERE              #
#######################################################
reduceStat         = 1 #recude the statistics, i.e. 10 is ten times less samples to look at
btagcoeff          = 0.89
metcut             = 0.
metsignifcut       = 0.
dphicut            = 0.25
mllcut             = 20
ngoodleptons       = 2
luminosity         = 1260

presel_met         = 'met_pt>'+str(metcut)
presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1'
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_ngoodlep    = '((nGoodMuons+nGoodElectrons)=='+str(ngoodleptons)+')'
presel_OS          = 'isOS'
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'

dataCut = '(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&Flag_HBHEIsoNoiseFilterReRun)&&weight>0'

#preselection: MET>40, njets>=2, n_bjets>=1, n_lep>=2
#See here for the Sum$ syntax: https://root.cern.ch/root/html/TTree.html#TTree:Draw@2
preselection = presel_met+'&&'+presel_nbjet+'&&'+presel_njet+'&&'+presel_metsig+'&&'+presel_mll+'&&'+presel_ngoodlep+'&&'+presel_OS+'&&'+presel_dPhi

#######################################################
#                 load all the samples                #
#######################################################
#from StopsDilepton.samples.cmgTuples_Spring15_25ns_postProcessed import *
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *

backgrounds = [DY_HT_LO,TTJets] 
data = [DoubleEG_Run2015D,DoubleMuon_Run2015D]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

#######################################################
#           define binning of 1D histograms           #
#######################################################
mllbinning = [15,0,300]

#######################################################
#             make plot in each sample:               #
#######################################################
plots = {\
  'mumu':{\
    'mllonZ': {'title':'M_{ll} (GeV)', 'name':'MllonZ', 'binning': mllbinning, 'histo':{}},
    'mlloffZ': {'title':'M_{ll} (GeV)', 'name':'MlloffZ', 'binning': mllbinning, 'histo':{}},
  },
  'ee':{\
    'mllonZ': {'title':'M_{ll} (GeV)', 'name':'MllonZ', 'binning': mllbinning, 'histo':{}},
    'mlloffZ': {'title':'M_{ll} (GeV)', 'name':'MlloffZ', 'binning': mllbinning, 'histo':{}},
  },
}


#######################################################
#            Start filling in the histograms          #
#######################################################
for s in backgrounds+data:
  #construct 1D histograms
  for pk in plots.keys():
    for plot in plots[pk].keys():
      plots[pk][plot]['histo'][s["name"]] = ROOT.TH1D(plots[pk][plot]['name']+"_"+s["name"]+"_"+pk, plots[pk][plot]['name']+"_"+s["name"]+"_"+pk, *plots[pk][plot]['binning'])
      plots[pk][plot]['histo'][s["name"]].Sumw2()

  chain = s["chain"]
   
  chain.SetBranchStatus("*",0)
  chain.SetBranchStatus("nVert",1)
  chain.SetBranchStatus("met_pt",1)
  chain.SetBranchStatus("met_phi",1)
  chain.SetBranchStatus("Jet_pt",1)
  chain.SetBranchStatus("Jet_eta",1)
  chain.SetBranchStatus("Jet_id",1)
  chain.SetBranchStatus("Jet_btagCSV",1)
  chain.SetBranchStatus("LepGood_pt",1)
  chain.SetBranchStatus("LepGood_eta",1)
  chain.SetBranchStatus("LepGood_phi",1)
  chain.SetBranchStatus("LepGood_charge",1)
  chain.SetBranchStatus("LepGood_dxy",1)
  chain.SetBranchStatus("LepGood_dz",1)
  chain.SetBranchStatus("LepGood_relIso03",1)
  chain.SetBranchStatus("LepGood_tightId",1)
  chain.SetBranchStatus("LepGood_pdgId",1)
  chain.SetBranchStatus("LepGood_mediumMuonId",1)
  chain.SetBranchStatus("LepGood_miniRelIso",1)
  chain.SetBranchStatus("LepGood_sip3d",1)
  chain.SetBranchStatus("LepGood_mvaIdPhys14",1)
  chain.SetBranchStatus("LepGood_convVeto",1)
  chain.SetBranchStatus("LepGood_lostHits",1)
  chain.SetBranchStatus("Jet_eta",1)
  chain.SetBranchStatus("Jet_pt",1)
  chain.SetBranchStatus("Jet_phi",1)
  chain.SetBranchStatus("Jet_btagCMVA",1)
  chain.SetBranchStatus("Jet_btagCSV",1)
  chain.SetBranchStatus("Jet_id",1)
  chain.SetBranchStatus("weight",1)
  chain.SetBranchStatus("l1_pt",1)
  chain.SetBranchStatus("l2_pt",1)
  chain.SetBranchStatus("dl_mass",1)
  chain.SetBranchStatus("dl_mt2ll",1)
  chain.SetBranchStatus("dl_mt2bb",1)
  chain.SetBranchStatus("dl_mt2blbl",1)
  chain.SetBranchStatus("dl_mass",1)
  chain.SetBranchStatus("nGoodMuons",1)
  chain.SetBranchStatus("nGoodElectrons",1)
  chain.SetBranchStatus("isOS",1)
  chain.SetBranchStatus("isEE",1)
  chain.SetBranchStatus("isEMu",1)
  chain.SetBranchStatus("isMuMu",1)
  chain.SetBranchStatus("HLT_mumuIso",1)
  chain.SetBranchStatus("HLT_ee_DZ",1)
  chain.SetBranchStatus("HLT_mue",1)
  if s in data:
    chain.SetBranchStatus("Flag_HBHENoiseFilter",1)
    chain.SetBranchStatus("Flag_goodVertices",1)
    chain.SetBranchStatus("Flag_CSCTightHaloFilter",1)
    chain.SetBranchStatus("Flag_eeBadScFilter",1)
    chain.SetBranchStatus("Flag_HBHEIsoNoiseFilterReRun",1)
  if s not in data: 
    chain.SetBranchStatus("genWeight",1)
    chain.SetBranchStatus("Jet_mcMatchFlav",1)
    chain.SetBranchStatus("xsec",1)
    chain.SetBranchStatus("Jet_partonId",1)
    chain.SetBranchStatus("puWeight",1)

  #Using Event loop
  #get EList after preselection
  print '\n', "Looping over %s" % s["name"]

  
  if s['isData'] : eList = getEList(chain, preselection+'&&'+dataCut)
  elif s == DY_LO: eList = eList = getEList(chain, preselection+'&&Sum$(Jet_pt)<150')   #stitch DY samples
  else:            eList = eList = getEList(chain, preselection)
  

  nEvents = eList.GetN()/reduceStat
  print "Found %i events in %s after preselection %s, looping over %i" % (eList.GetN(),s["name"],preselection,nEvents)
 
  for ev in range(nEvents):

    increment = 50
    if nEvents>increment and ev%(nEvents/increment)==0: 
      sys.stdout.write('\r' + "=" * (ev / (nEvents/increment)) +  " " * ((nEvents - ev)/ (nEvents/increment)) + "]" +  str(round((ev+1) / (float(nEvents)/100),2)) + "%")
      sys.stdout.flush()
      sys.stdout.write('\r')
    chain.GetEntry(eList.GetEntry(ev))
    mt2Calc.reset()
    #event weight (L= 4fb^-1)
    #weight = reduceStat*getVarValue(chain, "weight")*getVarValue(chain, "puWeight")*(luminosity/1000.) if not s['isData'] else 1

    pileupweight = puReweighting(chain) if not s['isData'] else 1.

    weight = reduceStat*getVarValue(chain, "weight")*(luminosity/1000.)*pileupweight if not s['isData'] else 1

    #MET
    met = getVarValue(chain, "met_pt")
    metPhi = getVarValue(chain, "met_phi")
    #jetpt
    leadingjetpt = getVarValue(chain, "Jet_pt",0)
    subleadingjetpt = getVarValue(chain, "Jet_pt",1)
    #leptons
    l0pt = getVarValue(chain, "l1_pt")
    l1pt = getVarValue(chain, "l2_pt")
    mll = getVarValue(chain,"dl_mass")
          
    #Leptons 
    allLeptons = getGoodLeptons(chain)
    muons = getGoodMuons(chain)
    electrons = getGoodElectrons(chain)
    nGoodElectrons = getVarValue(chain, "nGoodElectrons")
    nGoodMuons = getVarValue(chain, "nGoodMuons")

    isEE = getVarValue(chain, "isEE")
    isMuMu = getVarValue(chain, "isMuMu")
    isEMu = getVarValue(chain, "isEMu")

    #triggers
    triggerMuMu = getVarValue(chain,"HLT_mumuIso")
    triggerEleEle = getVarValue(chain,"HLT_ee_DZ")
    
    if (triggerEleEle == 1 and isEE and nGoodMuons==0 and nGoodElectrons==2):
        if abs(mll-91.2)>15: plots['ee']['mlloffZ']['histo'][s["name"]].Fill(mll, weight)
        if abs(mll-91.2)<15: plots['ee']['mllonZ']['histo'][s["name"]].Fill(mll, weight)
    if (triggerMuMu == 1 and isMuMu and  nGoodMuons==2 and nGoodElectrons==0):
        if abs(mll-91.2)>15: plots['mumu']['mlloffZ']['histo'][s["name"]].Fill(mll, weight)
        if abs(mll-91.2)<15: plots['mumu']['mllonZ']['histo'][s["name"]].Fill(mll, weight)


  #############################################
  #         Overflow to last bin              #
  #############################################
  for pk in plots.keys():
   for plot in plots[pk].keys():
     nXbins = plots[pk][plot]['histo'][s['name']].GetNbinsX()
     overflow = plots[pk][plot]['histo'][s['name']].GetBinContent(nXbins+1)
     error = plots[pk][plot]['histo'][s['name']].GetBinError(nXbins)
     overflowerror = plots[pk][plot]['histo'][s['name']].GetBinError(nXbins+1)
     plots[pk][plot]['histo'][s['name']].AddBinContent(nXbins, overflow) 
     plots[pk][plot]['histo'][s['name']].SetBinError(nXbins, sqrt(error**2+overflowerror**2))
     plots[pk][plot]['histo'][s['name']].SetBinContent(nXbins+1, 0.)
     plots[pk][plot]['histo'][s['name']].SetBinError(nXbins+1, 0.)


   # ##########################################
   #     bins with negative events to 0       #
   # ##########################################
     for i in range(nXbins):
       if plots[pk][plot]['histo'][s['name']].GetBinContent(i+1) < 0: plots[pk][plot]['histo'][s['name']].SetBinContent(i+1,0.)
  del eList

for s in backgrounds+data:
  for channel in plots.keys():
    for plot in plots[channel].keys():
      a = ROOT.Double(0)
      binning = plots[channel][plot]['binning']
      print s['name'], ",", channel, ",", plot, ": \t", plots[channel][plot]['histo'][s['name']].IntegralAndError(1,binning[0],a), "+-", a
