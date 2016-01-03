import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()
import numpy as n

from math import *
from StopsDilepton.tools.helpers import getChain,getWeight,getVarValue, getEList
from StopsDilepton.tools.localInfo import *
from datetime import datetime
from StopsDilepton.tools.puReweighting import getReweightingFunction
from StopsDilepton.tools.objectSelection import getLeptons, looseMuID, looseEleID, getJets, getGenParts, getGoodLeptons, getGoodElectrons, getGoodMuons

#puReweightingFunc = getReweightingFunction(era="doubleMu_onZ_isOS_1500pb_nVert_reweight")
#puReweighting = lambda c:puReweightingFunc(getVarValue(c, "nVert"))


start = datetime.now()
print '\n','\n', "Starting code",'\n','\n'

#######################################################
#                 load all the samples                #
#######################################################
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *


#######################################################
#        SELECT WHAT YOU WANT TO DO HERE              #
#######################################################
makedraw1D = True
makeTexFile = True
mt2llcutscaling = False
noscaling = False

#btagcoeff          = 0.89
btagcoeff          = 0.605
metcut             = 0.
metsignifcut       = 0.
dphicut            = 0.
mllcut             = 0
mt2llcut           = 100.
njetscut           = [">=2",'2m']
nbjetscut          = [">=2",'2m']
flavour            = "MuMu"


presel_met         = 'met_pt>'+str(metcut)
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)'+njetscut[0]
presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')'+nbjetscut[0]
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_OS          = 'isOS'
presel_mt2ll       = 'dl_mt2ll>='+str(mt2llcut)
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'
presel_zregion     = 'abs(91.2-dl_mass)<10'

if flavour=="MuMu": 
  presel_flavour     = 'isMuMu==1&&nGoodMuons>=2&&HLT_mumuIso'
  data = [DoubleMuon_Run2015D]
elif flavour=="EE": 
  presel_flavour     = 'isEE==1&&nGoodElectrons>=2&&HLT_ee_DZ'
  data = [DoubleEG_Run2015D]

luminosity = data[0]["lumi"]

datacut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

preselection = presel_njet+'&&'+presel_nbjet+'&&'+presel_OS+'&&'+presel_flavour+'&&'+presel_zregion+'&&'+presel_mll+'&&'+presel_met+'&&'+presel_metsig+'&&'+presel_dPhi

backgrounds = [DY_HT_LO,TTJets,WJetsToLNu,singleTop,QCD_Mu5,TTZ,TTW,TZQ,TTH,WZ]
#backgrounds = [TTZ,TTH,TTW]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

mt2llbinning = "(15,0,300)"
mllbinning = "(50,0,150)"
metbinning = "(30,0,300)"
lepbinning = "(50,0,300)"

plots = {\
  '2l':{\
    'dl_mt2ll':{\
      '2mj': {'title':'MT2ll (GeV)', 'name':'MT2ll_2l_2mj', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'MT2ll (GeV)', 'name':'MT2ll_2l_3mj',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      '2mj': {'title':'M_{ll} (GeV)', 'name':'Mll_2l_2mj', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'M_{ll} (GeV)', 'name':'Mll_2l_3mj',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      '2mj': {'title':'MET (GeV)', 'name':'MET_2l_2mj', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'MET (GeV)', 'name':'MET_2l_6mj',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[0]':{\
      '2mj': {'title':'l1 p_{T} (GeV)', 'name':'l1pt_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l1 p_{T} (GeV)', 'name':'l1pt_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[1]':{\
      '2mj': {'title':'l2 p_{T} (GeV)', 'name':'l2pt_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l2 p_{T} (GeV)', 'name':'l2pt_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[2]':{\
      '2mj': {'title':'l3 p_{T} (GeV)', 'name':'l3pt_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l3 p_{T} (GeV)', 'name':'l3pt_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  '3l':{\
    'dl_mt2ll':{\
      '3mj': {'title':'MT2ll (GeV)', 'name':'MT2ll_3l_3mj', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'MT2ll (GeV)', 'name':'MT2ll_3l_4mj',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      '3mj': {'title':'M_{ll} (GeV)', 'name':'Mll_3l_3mj', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'M_{ll} (GeV)', 'name':'Mll_3l_4mj',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      '3mj': {'title':'MET (GeV)', 'name':'MET_3l_3mj', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'MET (GeV)', 'name':'MET_3l_4mj',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[0]':{\
      '3mj': {'title':'l1 p_{T} (GeV)', 'name':'l1pt_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l1 p_{T} (GeV)', 'name':'l1pt_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[1]':{\
      '3mj': {'title':'l2 p_{T} (GeV)', 'name':'l2pt_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l2 p_{T} (GeV)', 'name':'l2pt_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[2]':{\
      '3mj': {'title':'l3 p_{T} (GeV)', 'name':'l3pt_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l3 p_{T} (GeV)', 'name':'l3pt_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  }

plots_cut = {\
  '2l':{\
    'dl_mt2ll':{\
      '2mj': {'title':'MT2ll (GeV)', 'name':'MT2llcut_2l_2mj', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'MT2ll (GeV)', 'name':'MT2llcut_2l_3mj',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      '2mj': {'title':'M_{ll} (GeV)', 'name':'Mllcut_2l_2mj', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'M_{ll} (GeV)', 'name':'Mllcut_2l_3mj',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      '2mj': {'title':'MET (GeV)', 'name':'METcut_2l_2mj', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'MET (GeV)', 'name':'METcut_2l_6mj',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[0]':{\
      '2mj': {'title':'l1 p_{T} (GeV)', 'name':'l1ptcut_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l1 p_{T} (GeV)', 'name':'l1ptcut_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[1]':{\
      '2mj': {'title':'l2 p_{T} (GeV)', 'name':'l2ptcut_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l2 p_{T} (GeV)', 'name':'l2ptcut_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[2]':{\
      '2mj': {'title':'l3 p_{T} (GeV)', 'name':'l3ptcut_2l_2mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '6mj': {'title':'l3 p_{T} (GeV)', 'name':'l3ptcut_2l_6mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  '3l':{\
    'dl_mt2ll':{\
      '3mj': {'title':'MT2ll (GeV)', 'name':'MT2llcut_3l_3mj', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'MT2ll (GeV)', 'name':'MT2llcut_3l_4mj',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      '3mj': {'title':'M_{ll} (GeV)', 'name':'Mllcut_3l_3mj', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'M_{ll} (GeV)', 'name':'Mllcut_3l_4mj',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      '3mj': {'title':'MET (GeV)', 'name':'METcut_3l_3mj', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'MET (GeV)', 'name':'METcut_3l_4mj',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[0]':{\
      '3mj': {'title':'l1 p_{T} (GeV)', 'name':'l1ptcut_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l1 p_{T} (GeV)', 'name':'l1ptcut_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[1]':{\
      '3mj': {'title':'l2 p_{T} (GeV)', 'name':'l2ptcut_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l2 p_{T} (GeV)', 'name':'l2ptcut_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    'LepGood_pt[2]':{\
      '3mj': {'title':'l3 p_{T} (GeV)', 'name':'l3ptcut_3l_3mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      '4mj': {'title':'l3 p_{T} (GeV)', 'name':'l3ptcut_3l_4mj', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  }


#######################################################
#            Start filling in the histograms          #
#######################################################
for s in backgrounds+data:
  #construct 1D histograms

  chain = s['chain']
  for lepton in plots.keys():
    for plot in plots[lepton].keys():
      if lepton == '2l': 
        chain.Draw(plot+">>"+plot+"_"+lepton+"_2mj"+s['name']+plots[lepton][plot]['2mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2&&(nGoodMuons+nGoodElectrons)>=2)')
        plots[lepton][plot]['2mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_2mj"+s['name'])
        chain.Draw(plot+">>"+plot+"_"+lepton+"_6mj"+s['name']+plots[lepton][plot]['6mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6&&(nGoodMuons+nGoodElectrons)>=2)')
        plots[lepton][plot]['6mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_6mj"+s['name'])
        #mt2llcut
        chain.Draw(plot+">>"+plot+"_"+lepton+"_2mj_mt2llcut"+s['name']+plots_cut[lepton][plot]['2mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2&&(nGoodMuons+nGoodElectrons)>=2&&dl_mt2ll>'+str(mt2llcut)+')')
        plots_cut[lepton][plot]['2mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_2mj_mt2llcut"+s['name'])
        chain.Draw(plot+">>"+plot+"_"+lepton+"_6mj_mt2llcut"+s['name']+plots_cut[lepton][plot]['6mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=6&&(nGoodMuons+nGoodElectrons)>=2&&dl_mt2ll>'+str(mt2llcut)+')')
        plots_cut[lepton][plot]['6mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_6mj_mt2llcut"+s['name'])
      if lepton == '3l': 
        chain.Draw(plot+">>"+plot+"_"+lepton+"_3mj"+s['name']+plots[lepton][plot]['3mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=3&&(nGoodMuons+nGoodElectrons)>=3)')
        plots[lepton][plot]['3mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_3mj"+s['name'])
        chain.Draw(plot+">>"+plot+"_"+lepton+"_4mj"+s['name']+plots[lepton][plot]['4mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=4&&(nGoodMuons+nGoodElectrons)>=3)')
        plots[lepton][plot]['4mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_4mj"+s['name'])
        #mt2llcut
        chain.Draw(plot+">>"+plot+"_"+lepton+"_3mj_mt2llcut"+s['name']+plots[lepton][plot]['3mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=3&&(nGoodMuons+nGoodElectrons)>=3&&dl_mt2ll>'+str(mt2llcut)+')')
        plots_cut[lepton][plot]['3mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_3mj_mt2llcut"+s['name'])
        chain.Draw(plot+">>"+plot+"_"+lepton+"_4mj_mt2llcut"+s['name']+plots[lepton][plot]['4mj']['binning'],"(weight)*("+preselection+'&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=4&&(nGoodMuons+nGoodElectrons)>=3&&dl_mt2ll>'+str(mt2llcut)+')')
        plots_cut[lepton][plot]['4mj']['histo'][s['name']] = ROOT.gDirectory.Get(plot+"_"+lepton+"_4mj_mt2llcut"+s['name'])

  #overflow
  for lepton in plots.keys():
    for plot in plots[lepton].keys():  
      for selection in plots[lepton][plot].keys():
        nbinsx        = plots[lepton][plot][selection]['histo'][s['name']].GetNbinsX()
        lastbin       = plots[lepton][plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
        error         = plots[lepton][plot][selection]['histo'][s['name']].GetBinError(nbinsx)
        overflowbin   = plots[lepton][plot][selection]['histo'][s['name']].GetBinContent(nbinsx+1)
        overflowerror = plots[lepton][plot][selection]['histo'][s['name']].GetBinError(nbinsx+1)
        plots[lepton][plot][selection]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
        plots[lepton][plot][selection]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
        plots[lepton][plot][selection]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
        plots[lepton][plot][selection]['histo'][s['name']].SetBinError(nbinsx+1,0.)
        #Remove bins with negative events
        for i in range(nbinsx):
          if plots[lepton][plot][selection]['histo'][s['name']].GetBinContent(i+1) < 0: plots[lepton][plot][selection]['histo'][s['name']].SetBinContent(i+1,0.)
        
processtime = datetime.now()
print "Time to process chains: ", processtime - start


for lepton in plots.keys():
  for plot in plots[lepton].keys():
    for selection in plots[lepton][plot].keys():
      totalbkg = 0
      for b in backgrounds:
        totalbkg += plots[lepton][plot][selection]['histo'][b["name"]].Integral()
      dataint = plots[lepton][plot][selection]['histo'][data[0]["name"]].Integral()

      print "Scaling factor data/MC for " +lepton+" and jet selection " + selection + ": ", dataint/totalbkg
      for b in backgrounds:
        if noscaling:
          plots[lepton][plot][selection]['SF'] = 1.
          plots_cut[lepton][plot][selection]['SF'] = 1.
        else:
          plots[lepton][plot][selection]['histo'][b["name"]].Scale(dataint/totalbkg)
          plots_cut[lepton][plot][selection]['histo'][b["name"]].Scale(dataint/totalbkg)
          plots[lepton][plot][selection]['SF'] = dataint/totalbkg
          plots_cut[lepton][plot][selection]['SF'] = dataint/totalbkg

#######################################################
#             Drawing done here                       #
#######################################################

legendtextsize = 0.032
a=[]
double = n.zeros(1, dtype=float)
#ROOT.gStyle.SetErrorX(0.5)
histopad =  [0.0, 0.2, 1.0, .95]
datamcpad = [0.0, 0.0, 1.0, 0.2]
lumitagpos = [0.4,0.95,0.6,1.0]
channeltagpos = [0.45,0.8,0.6,0.85]
legendpos = [0.6,0.6,1.0,1.0]
scalepos = [0.8,0.95,1.0,1.0]

if makedraw1D:
  for lepton in plots.keys():
    for plot in plots[lepton].keys():
      for selection in plots[lepton][plot].keys():
        l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
        a.append(l)
        l.SetFillColor(0)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        l.SetTextSize(legendtextsize)

        bkg_stack = ROOT.THStack("bkgs","bkgs") 
        totalbackground = plots[lepton][plot][selection]['histo'][backgrounds[0]['name']].Clone()
        for b in backgrounds:
          if b!= backgrounds[0]:totalbackground.Add(plots[lepton][plot][selection]['histo'][b['name']])

        for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots[lepton][plot][selection]["histo"][sort["name"]].Integral())):
          plots[lepton][plot][selection]['histo'][b["name"]].SetMarkerSize(0)
          plots[lepton][plot][selection]['histo'][b["name"]].SetFillColor(b["color"])
          plots[lepton][plot][selection]['histo'][b["name"]].SetLineWidth(1)
          bkg_stack.Add(plots[lepton][plot][selection]['histo'][b["name"]],"h")
          l.AddEntry(plots[lepton][plot][selection]['histo'][b["name"]],b['texName'],"f")

        c1 = ROOT.TCanvas("c1","c1",800,800)
        pad1 = ROOT.TPad("","",histopad[0],histopad[1],histopad[2],histopad[3])
        a.append(pad1)
        pad1.SetBottomMargin(0)
        pad1.SetTopMargin(0)
        pad1.SetRightMargin(0)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy()
        plots[lepton][plot][selection]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.Draw("same")
        plots[lepton][plot][selection]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.GetXaxis().SetLabelSize(0.)
        l.Draw()
        ROOT.gPad.RedrawAxis()

        plots[lepton][plot][selection]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots[lepton][plot][selection]['title'])
        plots[lepton][plot][selection]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
        plots[lepton][plot][selection]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.005,1000000)
        l.AddEntry(plots[lepton][plot][selection]['histo'][data[0]["name"]],data[0]['texName'])

        channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
        lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
        scaletag = ROOT.TPaveText(scalepos[0],scalepos[1],scalepos[2],scalepos[3],"NDC")
        channeltag.AddText(flavour)
        lumitag.AddText("lumi: "+str(data[0]['lumi'])+' pb^{-1}')
        scaletag.AddText("Scale Factor: " +str(round(plots[lepton][plot][selection]['SF'],2)))
        channeltag.SetFillColor(ROOT.kWhite)
        channeltag.SetShadowColor(ROOT.kWhite)
        channeltag.SetBorderSize(0)
        lumitag.SetFillColor(ROOT.kWhite)
        lumitag.SetShadowColor(ROOT.kWhite)
        lumitag.SetBorderSize(0)
        scaletag.SetShadowColor(ROOT.kWhite)
        scaletag.SetFillColor(ROOT.kWhite)
        scaletag.SetBorderSize(0)
        channeltag.Draw()
        c1.cd()
        pad2 = ROOT.TPad("","",datamcpad[0],datamcpad[1],datamcpad[2],datamcpad[3])
        a.append(pad2)
        pad2.SetGrid()
        pad2.SetBottomMargin(0.4)
        pad2.SetTopMargin(0)
        pad2.SetRightMargin(0)
        pad2.Draw()
        pad2.cd()
        ratio = plots[lepton][plot][selection]['histo'][data[0]["name"]].Clone()
        a.append(ratio)
        ratio.Divide(totalbackground)
        ratio.SetMarkerStyle(20)
        ratio.GetYaxis().SetTitle("Data/Bkg.")
      #ratio.GetYaxis().SetNdivisions(502)
        ratio.GetXaxis().SetTitle(plots[lepton][plot][selection]['title'])
        ratio.GetXaxis().SetTitleSize(0.2)
        ratio.GetYaxis().SetTitleSize(0.18)
        ratio.GetYaxis().SetTitleOffset(0.29)
        ratio.GetXaxis().SetTitleOffset(0.8)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetLabelSize(0.18)
        ratio.SetMinimum(0)
        ratio.SetMaximum(3)
        ratio.Draw("pe")
        c1.cd()
        lumitag.Draw()
        scaletag.Draw()
        path = plotDir+'/test/TTZstudy/'+lepton+'_'+flavour+'_njet_'+selection+'_nbjet_'+nbjetscut[1]+'_isOS_dPhi_'+str(dphicut)+'_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'/'
        if not os.path.exists(path): os.makedirs(path)
        c1.Print(path+plot+".png")
        del ratio
        del pad1
        del pad2
        c1.Clear()

  for lepton in plots_cut.keys():
    for plot in plots_cut[lepton].keys():
      for selection in plots_cut[lepton][plot].keys():
        l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
        a.append(l)
        l.SetFillColor(0)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        l.SetTextSize(legendtextsize)
        c1 = ROOT.TCanvas()

        bkg_stack = ROOT.THStack("bkgs","bkgs") 
        totalbackground = plots_cut[lepton][plot][selection]['histo'][backgrounds[0]['name']].Clone()
        for b in backgrounds:
          if b!= backgrounds[0]:totalbackground.Add(plots_cut[lepton][plot][selection]['histo'][b['name']])

        for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots_cut[lepton][plot][selection]["histo"][sort["name"]].Integral())):
          plots_cut[lepton][plot][selection]['histo'][b["name"]].SetMarkerSize(0)
          plots_cut[lepton][plot][selection]['histo'][b["name"]].SetFillColor(b["color"])
          plots_cut[lepton][plot][selection]['histo'][b["name"]].SetLineWidth(1)
          bkg_stack.Add(plots_cut[lepton][plot][selection]['histo'][b["name"]],"h")
          l.AddEntry(plots_cut[lepton][plot][selection]['histo'][b["name"]],b['name'],"f")

        c1 = ROOT.TCanvas("c1","c1",800,800)
        pad1 = ROOT.TPad("","",histopad[0],histopad[1],histopad[2],histopad[3])
        a.append(pad1)
        pad1.SetBottomMargin(0)
        pad1.SetTopMargin(0)
        pad1.SetRightMargin(0)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy()
        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.Draw("same")
        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.GetXaxis().SetLabelSize(0.)
        l.Draw()
        ROOT.gPad.RedrawAxis()

        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots_cut[lepton][plot][selection]['title'])
        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.005,100000)
        plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].Draw("pe1same")
        l.AddEntry(plots_cut[lepton][plot][selection]['histo'][data[0]["name"]],data[0]['name'])

        channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
        lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
        scaletag = ROOT.TPaveText(scalepos[0],scalepos[1],scalepos[2],scalepos[3],"NDC")
        channeltag.AddText(flavour)
        lumitag.AddText("lumi: "+str(data[0]['lumi'])+' pb^{-1}')
        scaletag.AddText("Scale Factor: " +str(round(plots_cut[lepton][plot][selection]['SF'],2)))
        channeltag.SetFillColor(ROOT.kWhite)
        channeltag.SetShadowColor(ROOT.kWhite)
        channeltag.SetBorderSize(0)
        lumitag.SetFillColor(ROOT.kWhite)
        lumitag.SetShadowColor(ROOT.kWhite)
        lumitag.SetBorderSize(0)
        scaletag.SetShadowColor(ROOT.kWhite)
        scaletag.SetFillColor(ROOT.kWhite)
        scaletag.SetBorderSize(0)
        channeltag.Draw()
        c1.cd()
        pad2 = ROOT.TPad("","",datamcpad[0],datamcpad[1],datamcpad[2],datamcpad[3])
        a.append(pad2)
        pad2.SetGrid()
        pad2.SetBottomMargin(0.4)
        pad2.SetTopMargin(0)
        pad2.SetRightMargin(0)
        pad2.Draw()
        pad2.cd()
        ratio = plots_cut[lepton][plot][selection]['histo'][data[0]["name"]].Clone()
        a.append(ratio)
        ratio.Divide(totalbackground)
        ratio.SetMarkerStyle(20)
        ratio.GetYaxis().SetTitle("Data/Bkg.")
      #ratio.GetYaxis().SetNdivisions(502)
        ratio.GetXaxis().SetTitle(plots_cut[lepton][plot][selection]['title'])
        ratio.GetXaxis().SetTitleSize(0.2)
        ratio.GetYaxis().SetTitleSize(0.18)
        ratio.GetYaxis().SetTitleOffset(0.29)
        ratio.GetXaxis().SetTitleOffset(0.8)
        ratio.GetYaxis().SetLabelSize(0.1)
        ratio.GetXaxis().SetLabelSize(0.18)
        ratio.SetMinimum(0)
        ratio.SetMaximum(3)
        ratio.Draw("pe")
        c1.cd()
        lumitag.Draw()
        scaletag.Draw()
        path = plotDir+'/test/TTZstudy/'+lepton+"_"+flavour+'_njet_'+selection+'_nbjet_'+nbjetscut[1]+'_isOS_dPhi_'+str(dphicut)+'_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'_mt2ll_'+str(int(mt2llcut))+'/'
        if not os.path.exists(path): os.makedirs(path)
        c1.Print(path+plot+".png")
        del ratio
        del pad1
        del pad2
        c1.Clear()

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start


if makeTexFile:

  #NO MT2LLCUT
  output = open("./texfiles/TTZnumbers"+flavour+".tex",'w')
  
  output.write("\\documentclass[8pt,landscape]{article}" + '\n')
  output.write("\\usepackage[margin=0.5in]{geometry}" + '\n')
  output.write("\\usepackage{verbatim}" + '\n')
  output.write("\\usepackage{hyperref}" + '\n')
  output.write("\\usepackage{epsfig}" + '\n')
  output.write("\\usepackage{graphicx}" + '\n')
  output.write("\\usepackage{epsfig}" + '\n')
  output.write("\\usepackage{subfigure,              rotating,              rotate}" + '\n')
  output.write("\\usepackage{relsize}" + '\n')
  output.write("\\usepackage{fancyheadings}" + '\n')
  output.write("\usepackage{multirow}" + '\n')
  output.write("\\usepackage[latin1]{inputenc}" + '\n')
  output.write("\\usepackage{footnpag}" + '\n')
  output.write("\\usepackage{enumerate}" + '\n')
  output.write("\\usepackage{color}" + '\n')
  output.write("\\newcommand{\\doglobally}[1]{{\\globaldefs=1#1}}" + '\n')
  output.write("\\begin{document}" + '\n' )

  output.write("\\begin{tabular}{|c||c|c||c|c|}" + '\n')
  string = '\\multirow{2}{*}{MT2ll $\\geq$ 0}'
  string2 = ''
  string3 = ''
  string4 = ''
  string4_5 = 'Total Bkg'
  string5 = 'Scale Factor'
  output.write("\\hline" + "\n")

  for lepton in sorted(plots.keys()):
    string += "& \\multicolumn{"+str(len(plots.keys()))+"}{|c||}{" +lepton+"}" if (lepton != sorted(plots.keys())[-1]) else "& \\multicolumn{"+str(len(plots.keys()))+"}{|c|}{" +lepton+"}"
    for selection in sorted(plots[lepton]["dl_mass"].keys()):
      string2 += "& " + selection
  for s in backgrounds:
    string3 += s["name"].replace("_","\\_") + " & "
    for lepton in sorted(plots.keys()):
      for selection in sorted(plots[lepton]["dl_mass"].keys()):
        nbins    = plots[lepton][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots[lepton][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        plots[lepton][plot][selection]['histo']['totalbkg'] += integral
        error    = round(double[0],2)
        string3 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots[lepton]["dl_mass"].keys())[-1]) and (lepton == sorted(plots.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string3 += '\\\\ \\hline \n'
  for s in data:
    string4 += s["name"].replace("_","\\_") + " & "
    for lepton in sorted(plots.keys()):
      for selection in sorted(plots[lepton]["dl_mass"].keys()):
        nbins    = plots[lepton][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots[lepton][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        error    = round(double[0],2)
        string4 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots[lepton]["dl_mass"].keys())[-1]) and (lepton == sorted(plots.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string4 += '\\\\ \\hline \n'
  for lepton in sorted(plots.keys()):
    for selection in sorted(plots[lepton]["dl_mass"].keys()):
      string4_5 += " & " + str(round(plots[lepton][plot][selection]['histo']['totalbkg'],2))
      string5 += " & " + str(round(plots[lepton][plot][selection]['SF'],2))
  output.write(string + '\\\\ \\cline{2-'+str(len(plots.keys())+1)+'} \n')
  output.write(string2 + '\\\\ \\hline \\hline \n')
  output.write(string3)
  output.write(string4 + "\\hline" + '\n')
  output.write(string4_5 + " \\\\ \\hline" + '\n')
  output.write(string5 + " \\\\ \\hline" + '\n')

  output.write("\\end{tabular}" + '\n')
  output.write('\\end{document}')


  #WITH MT2LLCUT
  output = open("./texfiles/TTZnumbers"+flavour+"_MT2llcut_"+str(mt2llcut)+".tex",'w')
  

  output.write("\\documentclass[8pt,landscape]{article}" + '\n')
  output.write("\\usepackage[margin=0.5in]{geometry}" + '\n')
  output.write("\\usepackage{verbatim}" + '\n')
  output.write("\\usepackage{hyperref}" + '\n')
  output.write("\\usepackage{epsfig}" + '\n')
  output.write("\\usepackage{graphicx}" + '\n')
  output.write("\\usepackage{epsfig}" + '\n')
  output.write("\\usepackage{subfigure,              rotating,              rotate}" + '\n')
  output.write("\\usepackage{relsize}" + '\n')
  output.write("\\usepackage{fancyheadings}" + '\n')
  output.write("\usepackage{multirow}" + '\n')
  output.write("\\usepackage[latin1]{inputenc}" + '\n')
  output.write("\\usepackage{footnpag}" + '\n')
  output.write("\\usepackage{enumerate}" + '\n')
  output.write("\\usepackage{color}" + '\n')
  output.write("\\newcommand{\\doglobally}[1]{{\\globaldefs=1#1}}" + '\n')
  output.write("\\begin{document}" + '\n' )

  output.write("\\begin{tabular}{|c||c|c|c||c|c|c|}" + '\n')
  string = '\\multirow{2}{*}{MT2ll $\\geq$ '+str(mt2llcut)+'}'
  string2 = ''
  string3 = ''
  string4 = ''
  string4_5 = 'Total Bkg'
  string5 = 'Scale Factor'
  output.write("\\hline" + "\n")
  for lepton in sorted(plots_cut.keys()):
    string += "& \\multicolumn{3}{|c||}{" +lepton+"}" if (lepton != sorted(plots_cut.keys())[-1]) else "& \\multicolumn{3}{|c|}{" +lepton+"}"
    for selection in sorted(plots_cut[lepton]["dl_mass"].keys()):
      string2 += "& " + selection
  for s in backgrounds:
    string3 += s["name"].replace("_","\\_") + " & "
    for lepton in sorted(plots_cut.keys()):
      for selection in sorted(plots_cut[lepton]["dl_mass"].keys()):
        nbins    = plots_cut[lepton][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots_cut[lepton][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        plots_cut[lepton][plot][selection]['histo']['totalbkg'] += integral
        error    = round(double[0],2)
        string3 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots_cut[lepton]["dl_mass"].keys())[-1]) and (lepton == sorted(plots_cut.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string3 += '\\\\ \\hline \n'
  for s in data:
    string4 += s["name"].replace("_","\\_") + " & "
    for lepton in sorted(plots_cut.keys()):
      for selection in sorted(plots_cut[lepton]["dl_mass"].keys()):
        nbins    = plots_cut[lepton][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots_cut[lepton][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        error    = round(double[0],2)
        string4 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots_cut[lepton]["dl_mass"].keys())[-1]) and (lepton == sorted(plots_cut.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string4 += '\\\\ \\hline \n'
  for lepton in sorted(plots.keys()):
    for selection in sorted(plots[lepton]["dl_mass"].keys()):
      string4_5 += " & " + str(round(plots_cut[lepton][plot][selection]['histo']['totalbkg'],2))
      string5 += " & " + str(round(plots_cut[lepton][plot][selection]['SF'],2))
  output.write(string + '\\\\ \\cline{2-7} \n')
  output.write(string2 + '\\\\ \\hline \\hline \n')
  output.write(string3)
  output.write(string4 + "\\hline" + '\n')
  output.write(string4_5 + " \\\\ \\hline" + '\n')
  output.write(string5 + " \\\\ \\hline" + '\n')

  output.write("\\end{tabular}" + '\n')
  output.write('\\end{document}')
