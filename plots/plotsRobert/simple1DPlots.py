from optparse import OptionParser
parser = OptionParser()
parser.add_option("--mode", dest="mode", default="doubleMu", type="string", action="store", help="doubleMu, doubleEle, muEle")
parser.add_option("--zMode", dest="zMode", default="onZ", type="string", action="store", help="onZ, offZ, allZ")
parser.add_option("--small", dest="small", default = False, action="store_true", help="small?")
parser.add_option("--addLeptonID", dest="addLeptonID", default = False, action="store_true", help="add leptonID plots?")
#parser.add_option("--OS", dest="OS", default = True, action="store_true", help="require OS?")

(opts, args) = parser.parse_args()

import ROOT
ROOT.TH1F().SetDefaultSumw2()
from array import array
from math import cos,sin,sqrt,cosh,pi
import os, copy, sys
import itertools

from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *
from StopsDilepton.tools.objectSelection import getLeptons, getMuons, getElectrons, getGoodMuons, getGoodElectrons, getGoodLeptons, mZ
from StopsDilepton.tools.helpers import getVarValue, getYieldFromChain, getChain
from StopsDilepton.tools.localInfo import plotDir
from simplePlotHelpers import plot, stack, loopAndFill, drawNMStacks
from StopsDilepton.tools.puReweighting import getReweightingFunction

puReweightingFunc = getReweightingFunction(era="doubleMu_onZ_isOS_1200pb_nVert_reweight")
puReweighting = lambda c:puReweightingFunc(getVarValue(c, "nVert"))
#puReweighting = None

cutBranches = ["weight", "leptonPt", "met*", "nVert",'run',\
               'Jet_pt', "Jet_id", "Jet_eta", "Jet_phi", "Jet_btagCSV",
               "LepGood_pdgId", "LepGood_mediumMuonId", "LepGood_miniRelIso", "LepGood_sip3d", "LepGood_dxy", "LepGood_dz", "LepGood_convVeto", "LepGood_lostHits",
               "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter", "Flag_goodVertices", "Flag_CSCTightHaloFilter", "Flag_eeBadScFilter",
               "HLT_mumuIso", "HLT_ee_DZ", "HLT_mue",
               "is*","dl_*","l1_*","l2_*", "nGoodMuons", "nGoodElectrons"
                ]
subdir = "png25ns_2l_mAODv2_PUrw"
#preprefixes = ["PUDoubleMuOnZIsOS"]
preprefixes = [] if not opts.small else ['small']
maxN = 1 if opts.small else -1

def getZCut(mode):
  zstr = "abs(dl_mass - "+str(mZ)+")"
  if mode.lower()=="onz": return zstr+"<15"
  if mode.lower()=="offz": return zstr+">15"
  return "(1)"

#filterCut = "(Flag_HBHENoiseFilter&&Flag_HBHENoiseIsoFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter)"
filterCut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"
#filterCut = "(1)"

#nMu = "Sum$(abs(LepGood_pdgId)==13&&LepGood_mediumMuonId==1&&LepGood_miniRelIso<0.1&&LepGood_sip3d<4.0&&abs(LepGood_dxy)<0.05&&abs(LepGood_dz)<0.1)"
#nEle = "Sum$(abs(LepGood_pdgId)==11&&LepGood_convVeto==1&&LepGood_miniRelIso<0.2&&LepGood_sip3d<4.0&&abs(LepGood_dxy)<0.05&&abs(LepGood_dz)<0.1&&LepGood_lostHits==0)"
triggerMuMu = "HLT_mumuIso"
triggerEleEle = "HLT_ee_DZ"
triggerMuEle = "HLT_mue"

cuts=[
 ("njet2", "(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=2"),
 ("nbtag1", "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)>=1"),
 ("mll20", "dl_mass>20"),
# ("met80", "met_pt>80"),
# ("metSig5", "met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>5"),
# ("dPhiJet0-dPhiJet1", "cos(met_phi-Jet_phi[0])<cos(0.25)&&cos(met_phi-Jet_phi[1])<cos(0.25)"),
  ]
#for i in range(len(cuts)+1):
for i in reversed(range(len(cuts)+1)):
#for i in [len(cuts)]:
  for comb in itertools.combinations(cuts,i):
#    presel = [("isOS","isOS"), ("mRelIso01", "LepGood_miniRelIso[l1_index]<0.1&&LepGood_miniRelIso[l2_index]<0.1")]
    presel = [("isOS","isOS")]
    presel.extend( comb )

    prefix = '_'.join(preprefixes+[opts.mode, opts.zMode, '-'.join([p[0] for p in presel])]) 
    preselCuts = [p[1] for p in presel]

    if opts.mode=="doubleMu":
      cutString = "&&".join(["isMuMu==1&&nGoodMuons==2&&nGoodElectrons==0", getZCut(opts.zMode)] + preselCuts)
      dataCut = "&&".join([triggerMuMu, filterCut])
      dataSample = DoubleMuon_Run2015D
      QCDSample = QCD_Mu5
    if opts.mode=="doubleEle":
      cutString = "&&".join(["isEE==1&&nGoodMuons==0&&nGoodElectrons==2", getZCut(opts.zMode)] + preselCuts)
      dataCut = "&&".join([triggerEleEle, filterCut])
      dataSample = DoubleEG_Run2015D
      QCDSample = QCD_EMbcToE
    if opts.mode=="muEle":
      cutString = "&&".join(["isEMu==1&&nGoodMuons==1&&nGoodElectrons==1", getZCut(opts.zMode)] + preselCuts)
      dataCut = "&&".join([triggerMuEle, filterCut])
      dataSample = MuonEG_Run2015D
      QCDSample = QCD_Mu5EMbcToE

    cutFunc = None
    lumiScaleFac = dataSample["lumi"]/1000.
    backgrounds = [TTJets_Lep, WJetsToLNu, DY, singleTop, QCDSample, TTX, diBoson] 
    data = getYieldFromChain(getChain(dataSample,histname="",maxN=maxN), cutString = "&&".join([cutString, dataCut]), weight='weight') 
    bkg  = 0. 
    for s in backgrounds:
      bkg+= getYieldFromChain(getChain(s,histname="", maxN=maxN), cutString, weight='weight')

    scaleFac = data/(bkg*lumiScaleFac)

    print "After lumiscale %3.3f there is bkg %7.1f and data %7.1f: re-normalizing scaleFac by %3.3f"%(lumiScaleFac, lumiScaleFac*bkg, data, scaleFac)
     
    ratioOps = {'yLabel':'Data/MC', 'numIndex':1, 'denIndex':0 ,'yRange':None, 'logY':False, 'color':ROOT.kBlack, 'yRange':(0.1, 2.1)}
    #ratioOps = None

    def getStack(labels, var, binning, cut, options={}):

      style_Data         = {'legendText':dataSample['name'],      'style':"e", 'lineThickness':0, 'errorBars':True, 'color':ROOT.kBlack, 'markerStyle':20, 'markerSize':1}
      style_WJets        = {'legendText':'W + Jets',         'style':"f", 'lineThickness':0, 'errorBars':False, 'color':42, 'markerStyle':None, 'markerSize':None}
      style_TTJets       = {'legendText':'t#bar{t} + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':7, 'markerStyle':None, 'markerSize':None}
      style_DY           = {'legendText':'DY + Jets',  'style':"f", 'linethickNess':0, 'errorBars':False,       'color':8, 'markerStyle':None, 'markerSize':None}
      style_TTX          = {'legendText':'t#bar{t} + W/Z/H',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':ROOT.kYellow+2, 'markerStyle':None, 'markerSize':None}
      style_diBoson         = {'legendText':'WW/WZ/ZZ',  'style':"f", 'linethickNess':0, 'errorBars':False, 'color':ROOT.kGreen-5, 'markerStyle':None, 'markerSize':None}
      style_QCD          = {'legendText':'QCD',  'style':"f", 'linethickNess':0, 'errorBars':False,             'color':46, 'markerStyle':None, 'markerSize':None}
      style_singleTop    = {'legendText':'single top',  'style':"f", 'linethickNess':0, 'errorBars':False,      'color':40, 'markerStyle':None, 'markerSize':None}
      
      data               = plot(var, binning, cut, sample=dataSample,       style=style_Data)
      MC_TTJets          = plot(var, binning, cut, sample=TTJets_Lep,       style=style_TTJets,    weightString="weight", weightFunc=puReweighting)
      MC_WJetsToLNu      = plot(var, binning, cut, sample=WJetsToLNu,   style=style_WJets,     weightString="weight", weightFunc=puReweighting)
      MC_DY              = plot(var, binning, cut, sample=DY,           style=style_DY,        weightString="weight", weightFunc=puReweighting)
      MC_singleTop       = plot(var, binning, cut, sample=singleTop,    style=style_singleTop, weightString="weight", weightFunc=puReweighting)
      MC_QCD             = plot(var, binning, cut, sample=QCDSample,        style=style_QCD,       weightString="weight", weightFunc=puReweighting)
      MC_TTX             = plot(var, binning, cut, sample=TTX,          style=style_TTX, weightString="weight", weightFunc=puReweighting)
      MC_diBoson         = plot(var, binning, cut, sample=diBoson,     style=style_diBoson, weightString="weight", weightFunc=puReweighting)
      #FIXME triBoson
      mcStack = [MC_TTJets, MC_DY,  MC_QCD, MC_singleTop, MC_WJetsToLNu, MC_diBoson, MC_TTX]
      for s in mcStack:
    #    print s,s.sample
        s.sample['scale'] = lumiScaleFac*scaleFac

      plotLists = [mcStack, [data]]
#      plotLists = [mcStack]

      for pL in plotLists:
        for p in pL:
          p.sample['small']=opts.small

      opt = {'small':opts.small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.11, "auto"], 'ratio':ratioOps, 'fileName':var['name']}
    #  opt = {'small':small, 'yHeadRoomFac':12, 'labels':labels, 'logX':False, 'logY':True, 'yRange':[0.11, "auto"], 'ratio':None, 'fileName':var['name']}

      if opt.has_key('ratio') and opt['ratio']:
        opt['texLines'] = [{'pos':(0.15, 0.95),'text':'CMS Preliminary', 'options':{'size':0.052}},\
                           {'pos':(0.47, 0.95), 'text':'L='+str(dataSample['lumi'])+' pb{}^{-1} (13 TeV) Scale %3.2f'%scaleFac, 'options':{'size':0.052}}]
        opt['legend'] = {'coordinates':[0.55,0.90 - len(mcStack)*0.05,.98,.93],'boxed':True}
      else:
        opt['texLines'] = [{'pos':(0.16, 0.965), 'text':'CMS Preliminary',       'options':{'size':0.038}},\
                           {'pos':(0.47, 0.965),  'text':'L='+str(dataSample['lumi'])+' pb{}^{-1} (13 TeV) Scale %3.2f'%scaleFac,'options':{'size':0.038}}]
        opt['legend'] = {'coordinates':[0.55,0.90 - len(mcStack)*0.05,.98,.95],'boxed':True}

      opt.update(options)
      res = stack(plotLists, options = opt)
      res.usedBranches = cutBranches
      return res

    allStacks=[]

    dl_mass_stack  = getStack(
        labels={'x':'m(ll) (GeV)','y':'Number of Events / 3 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_mass','leaf':"dl_mass", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[150/3,0,150]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_mass_stack)

    dl_pt_stack  = getStack(
        labels={'x':'p_{T}(ll) (GeV)','y':'Number of Events / 10 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_pt','leaf':"dl_pt", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[40,0,400]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_pt_stack)

    dl_eta_stack  = getStack(
        labels={'x':'#eta(ll) ','y':'Number of Events'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_eta','leaf':"dl_eta", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-3,3]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_eta_stack)

    dl_phi_stack  = getStack(
        labels={'x':'#phi(ll) (GeV)','y':'Number of Events'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_phi','leaf':"dl_phi", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-pi,pi]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_phi_stack)

    dl_mt2ll_stack  = getStack(
        labels={'x':'MT_{2}^{ll} (GeV)','y':'Number of Events / 20 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_mt2ll','leaf':"dl_mt2ll", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[300/20,0,300]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_mt2ll_stack)
    dl_mt2bb_stack  = getStack(
        labels={'x':'MT_{2}^{bb} (GeV)','y':'Number of Events / 20 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_mt2bb','leaf':"dl_mt2bb", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[(400-80)/20,80,400]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_mt2bb_stack)
    dl_mt2blbl_stack  = getStack(
        labels={'x':'MT_{2}^{blbl} (GeV)','y':'Number of Events / 20 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_mt2blbl','leaf':"dl_mt2blbl", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[300/20,0,300]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_mt2blbl_stack)

    dl_mtautau_stack  = getStack(
        labels={'x':'m_{#tau#tau} (GeV)','y':'Number of Events / 5 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'dl_mtautau','leaf':"dl_mtautau", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[20,0,400]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(dl_mtautau_stack)

    l1_pt_stack  = getStack(
        labels={'x':'p_{T}(l_{1}) (GeV)','y':'Number of Events / 5 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'l1_pt','leaf':"l1_pt", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[60,0,300]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l1_pt_stack)
    l1_eta_stack  = getStack(
        labels={'x':'#eta(l_{1})','y':'Number of Events'},
        var={'name':'l1_eta','leaf':"l1_eta", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[36,-3.3,3.3]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l1_eta_stack)
    l1_phi_stack  = getStack(
        labels={'x':'#phi(l_{1})','y':'Number of Events'},
        var={'name':'l1_phi','leaf':"l1_phi", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-pi,pi]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l1_phi_stack)
    l1_pdgId_stack  = getStack(
        labels={'x':'pdgId(l_{1})','y':'Number of Events'},
        var={'name':'l1_pdgId','leaf':"l1_pdgId", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[32,-16,16]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l1_pdgId_stack)
    l2_pt_stack  = getStack(
        labels={'x':'p_{T}(l_{1}) (GeV)','y':'Number of Events / 5 GeV'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'l2_pt','leaf':"l2_pt", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[60,0,300]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l2_pt_stack)
    l2_eta_stack  = getStack(
        labels={'x':'#eta(l_{1})','y':'Number of Events'},
        var={'name':'l2_eta','leaf':"l2_eta", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-3,3]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l2_eta_stack)
    l2_phi_stack  = getStack(
        labels={'x':'#phi(l_{1})','y':'Number of Events'},
        var={'name':'l2_phi','leaf':"l2_phi", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-pi,pi]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l2_phi_stack)
    l2_pdgId_stack  = getStack(
        labels={'x':'pdgId(l_{1})','y':'Number of Events'},
        var={'name':'l2_pdgId','leaf':"l2_pdgId", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[32,-16,16]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(l2_pdgId_stack)

    metZoomed_stack  = getStack(
        labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 10 GeV'},
        var={'name':'metZoomed','leaf':'met_pt', 'overFlow':'upper'},
        binning={'binning':[22,0,220]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(metZoomed_stack)

    met_stack  = getStack(
        labels={'x':'#slash{E}_{T} (GeV)','y':'Number of Events / 50 GeV'},
        var={'name':'met','leaf':'met_pt', 'overFlow':'upper'},
        binning={'binning':[1050/50,0,1050]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(met_stack)

    metSig_stack  = getStack(
        labels={'x':'#slash{E}_{T}/#sqrt(H_{T}) (GeV^{1/2})','y':'Number of Events / 100 GeV'},
    #    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
        var={'name':'metSig','TTreeFormula':'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))', 'overFlow':'upper'},
        binning={'binning':[20,0,20]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(metSig_stack)

    ht_stack  = getStack(
        labels={'x':'H_{T} (GeV)','y':'Number of Events / 100 GeV'},
    #    var={'name':'ht','leaf':'htJet40ja', 'overFlow':'upper'},
        var={'name':'ht','TTreeFormula':'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
        binning={'binning':[2600/100,0,2600]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(ht_stack)

    ht_zoomed_stack  = getStack(
        labels={'x':'H_{T} (GeV)','y':'Number of Events / 30 GeV'},
    #    var={'name':'ht_zoomed','leaf':'ht_zoomedJet40ja', 'overFlow':'upper'},
        var={'name':'ht_zoomed','TTreeFormula':'Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))', 'overFlow':'upper'},
        binning={'binning':[390/15,0,390]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(ht_zoomed_stack)

    cosMetJet0phi_stack  = getStack(
        labels={'x':'Cos(#phi(#slash{E}_{T}, Jet[0]))','y':'Number of Events'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'cosMetJet0phi','TTreeFormula':"cos(met_phi-Jet_phi[0])", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-1,1]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(cosMetJet0phi_stack)

    cosMetJet1phi_stack  = getStack(
        labels={'x':'Cos(#phi(#slash{E}_{T}, Jet[1]))','y':'Number of Events'},
    #    var={'name':'mll','func':mll, 'overFlow':'upper', 'branches':[]},
        var={'name':'cosMetJet1phi','TTreeFormula':"cos(met_phi-Jet_phi[1])", 'overFlow':'upper', 'branches':[]},
        binning={'binning':[30,-1,1]},
        cut={'string':cutString,'func':cutFunc,'dataCut':dataCut},
        )
    allStacks.append(cosMetJet1phi_stack)

    lepGood_pt0_stack  = getStack(
        labels={'x':'p_{T}(l) (GeV)','y':'Number of Events / 25 GeV'},
        var={'name':'LepGood_pt0','leaf':'LepGood_pt','ind':0, 'overFlow':'upper'},
        binning={'binning':[975/25,0,975]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(lepGood_pt0_stack)


    jet0pt_stack  = getStack(
        labels={'x':'p_{T}(leading jet) (GeV)','y':'Number of Events / 20 GeV'},
        var={'name':'jet0pt','leaf':'Jet_pt','ind':0, 'overFlow':'upper'},
        binning={'binning':[980/20,0,980]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(jet0pt_stack)
    jet1pt_stack  = getStack(
        labels={'x':'p_{T}(2^{nd.} leading jet) (GeV)','y':'Number of Events / 20 GeV'},
        var={'name':'jet1pt','leaf':'Jet_pt','ind':1, 'overFlow':'upper'},
        binning={'binning':[980/20,0,980]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(jet1pt_stack)
    jet2pt_stack  = getStack(
        labels={'x':'p_{T}(3^{rd.} leading jet) (GeV)','y':'Number of Events / 20 GeV'},
        var={'name':'jet2pt','leaf':'Jet_pt','ind':2, 'overFlow':'upper'},
        binning={'binning':[400/20,0,400]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(jet2pt_stack)
    jet3pt_stack  = getStack(
        labels={'x':'p_{T}(4^{th.} leading jet) (GeV)','y':'Number of Events / 20 GeV'},
        var={'name':'jet3pt','leaf':'Jet_pt','ind':3, 'overFlow':'upper'},
        binning={'binning':[400/20,0,400]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(jet3pt_stack)
    jet4pt_stack  = getStack(
        labels={'x':'p_{T}(5^{th.} leading jet) (GeV)','y':'Number of Events / 20 GeV'},
        var={'name':'jet4pt','leaf':'Jet_pt','ind':4, 'overFlow':'upper'},
        binning={'binning':[400/20,0,400]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(jet4pt_stack)

    nbtags_stack  = getStack(
        labels={'x':'number of b-tags (CSVM)','y':'Number of Events'},
        var={'name':'nBTags','TTreeFormula':"Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)", 'overFlow':'upper'},
        binning={'binning':[8,0,8]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(nbtags_stack)

    njets_stack  = getStack(
        labels={'x':'number of jets','y':'Number of Events'},
        var={'name':'njets','TTreeFormula':'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)', 'overFlow':'upper'},
        binning={'binning':[14,0,14]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(njets_stack)

    nVert_stack  = getStack(
        labels={'x':'vertex multiplicity','y':'Number of Events'},
        var={'name':'nVert','leaf':"nVert", 'overFlow':'upper'},
        binning={'binning':[50,0,50]},
        cut={'string':cutString,'func':cutFunc, 'dataCut':dataCut})
    allStacks.append(nVert_stack)

# OBJ: TBranch LepGood_charge  charge for Leptons after the preselection : 0 at: 0x504dc00
# OBJ: TBranch LepGood_tightId POG Tight ID (for electrons it's configured in the analyzer) for Leptons after the preselection : 0 at: 0x504e5e0
# OBJ: TBranch LepGood_eleCutIdCSA14_25ns_v1 Electron cut-based id (POG CSA14_25ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x504f030
# OBJ: TBranch LepGood_eleCutIdCSA14_50ns_v1 Electron cut-based id (POG CSA14_50ns_v1): 0=none, 1=veto, 2=loose, 3=medium, 4=tight for Leptons after the preselection : 0 at: 0x504fad0
# OBJ: TBranch LepGood_dxy d_{xy} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x5050570
# OBJ: TBranch LepGood_dz  d_{z} with respect to PV, in cm (with sign) for Leptons after the preselection : 0 at: 0x5050f70
# OBJ: TBranch LepGood_edxy  #sigma(d_{xy}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x5051970
# OBJ: TBranch LepGood_edz #sigma(d_{z}) with respect to PV, in cm for Leptons after the preselection : 0 at: 0x5052370
# OBJ: TBranch LepGood_ip3d  d_{3d} with respect to PV, in cm (absolute value) for Leptons after the preselection : 0 at: 0x5052d70
# OBJ: TBranch LepGood_sip3d S_{ip3d} with respect to PV (significance) for Leptons after the preselection : 0 at: 0x5053780
# OBJ: TBranch LepGood_convVeto  Conversion veto (always true for muons) for Leptons after the preselection : 0 at: 0x5054180
# OBJ: TBranch LepGood_lostHits  Number of lost hits on inner track for Leptons after the preselection : 0 at: 0x5054be0
# OBJ: TBranch LepGood_relIso03  PF Rel Iso, R=0.3, pile-up corrected for Leptons after the preselection : 0 at: 0x5055640
# OBJ: TBranch LepGood_relIso04  PF Rel Iso, R=0.4, pile-up corrected for Leptons after the preselection : 0 at: 0x50560a0
# OBJ: TBranch LepGood_miniRelIso  PF Rel miniRel, pile-up corrected for Leptons after the preselection : 0 at: 0x5056b00
# OBJ: TBranch LepGood_relIsoAn04  PF Activity Annulus, pile-up corrected for Leptons after the preselection : 0 at: 0x5057560
# OBJ: TBranch LepGood_tightCharge Tight charge criteria: for electrons, 2 if isGsfCtfScPixChargeConsistent, 1 if only isGsfScPixChargeConsistent, 0 otherwise; for muons, 2 if ptError/pt < 0.20, 0 otherwise  for Leptons after the preselection : 0 at: 0x5057fc0
# OBJ: TBranch LepGood_mcMatchId Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Leptons after the preselection : 0 at: 0x5058aa0
# OBJ: TBranch LepGood_mcMatchAny  Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom for Leptons after the preselection : 0 at: 0x5059560
# OBJ: TBranch LepGood_mcMatchTau  True if the leptons comes from a tau for Leptons after the preselection : 0 at: 0x505a010
# OBJ: TBranch LepGood_mcPt  p_{T} of associated gen lepton for Leptons after the preselection : 0 at: 0x505aa70
# OBJ: TBranch LepGood_mediumMuonId  Muon POG Medium id for Leptons after the preselection : 0 at: 0x505b470
# OBJ: TBranch LepGood_pdgId pdgId for Leptons after the preselection : 0 at: 0x505bec0
# OBJ: TBranch LepGood_pt  pt for Leptons after the preselection : 0 at: 0x505c8a0
# OBJ: TBranch LepGood_eta eta for Leptons after the preselection : 0 at: 0x505d280
# OBJ: TBranch LepGood_phi phi for Leptons after the preselection : 0 at: 0x505dc60
# OBJ: TBranch LepGood_mass  mass for Leptons after the preselection : 0 at: 0x505e640
# OBJ: TBranch LepGood_mvaIdPhys14 EGamma POG MVA ID for non-triggering electrons, Phys14 re-training; 1 for muons for Leptons after the preselection : 0 at: 0x505f020
# OBJ: TBranch LepGood_mvaIdSpring15 EGamma POG MVA ID for non-triggering electrons, Spring15 re-training; 1 for muons for Leptons after the preselection : 0 at: 0x505fab0
# OBJ: TBranch LepGood_mvaTTH  Lepton MVA (TTH version) for Leptons after the preselection : 0 at: 0x5060540
# OBJ: TBranch LepGood_jetPtRatiov1  pt(lepton)/pt(nearest jet) for Leptons after the preselection : 0 at: 0x5060f30
# OBJ: TBranch LepGood_jetPtRelv1  pt of the lepton transverse to the jet axis (subtracting the lepton) for Leptons after the preselection : 0 at: 0x5061980
# OBJ: TBranch LepGood_jetPtRatiov2  pt(lepton)/[rawpt(jet-PU-lep)*L2L3Res+pt(lepton)] for Leptons after the preselection : 0 at: 0x5062400
# OBJ: TBranch LepGood_jetPtRelv2  pt of the lepton transverse to the jet axis (subtracting the lepton) - v2 for Leptons after the preselection : 0 at: 0x5062e70
# OBJ: TBranch LepGood_jetBTagCSV  CSV btag of nearest jet for Leptons after the preselection : 0 at: 0x50638f0
# OBJ: TBranch LepGood_jetBTagCMVA CMA btag of nearest jet for Leptons after the preselection : 0 at: 0x5064340
# OBJ: TBranch LepGood_jetDR deltaR(lepton, nearest jet) for Leptons after the preselection : 0 at: 0x5064d90

    loopAndFill(allStacks)

    path = '/'.join([plotDir, subdir, prefix])
    print "path",path
    if not os.path.exists(path): os.makedirs(path)
    stuff=[]
    for stk in allStacks:
      stuff.append(drawNMStacks(1,1,[stk], path=path, filename=stk.options['fileName']))

    ROOT.gDirectory.GetListOfFiles().ls()

