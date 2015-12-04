import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()
import numpy

from math import *
from StopsDilepton.tools.helpers import getChain,getWeight,getVarValue
from StopsDilepton.tools.localInfo import *
from datetime import datetime

start = datetime.now()
print '\n','\n', "Starting code",'\n','\n'

#######################################################
#        SELECT WHAT YOU WANT TO DO HERE              #
#######################################################
reduceStat = 1 #recude the statistics, i.e. 10 is ten times less samples to look at
makedraw1D = True

btagcoeff          = 0.89
metcut             = 80.
metsignifcut       = 5.
dphicut            = 0.25
mllcut             = 20
ngoodleptons       = 2

flavour = "MuMu"

presel_met         = 'met_pt>'+str(metcut)
#presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0'
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_OS          = 'isOS'
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'

presel_flavour     = 'isMuMu&&nGoodElectrons==0&&nGoodMuons==2&&HLT_mumuIso==1&&weight>0'
if flavour=="MuMu": 
  presel_flavour     = 'isMuMu==1&&nGoodElectrons==0&&nGoodMuons==2&&HLT_mumuIso'
elif flavour=="EE": 
  presel_flavour     = 'isEE==1&&nGoodElectrons==2&&nGoodMuons==0&&HLT_ee_DZ'
elif flavour=="EMu": 
  presel_flavour     = 'isEMu==1&&nGoodElectrons==1&&nGoodMuons==1&&HLT_mue'


#preselection: MET>40, njets>=2, n_bjets>=1, n_lep>=2
#For now see here for the Sum$ syntax: https://root.cern.ch/root/html/TTree.html#TTree:Draw@2
preselection = presel_njet+'&&'+presel_OS+'&&'+presel_mll+'&&'+presel_dPhi+'&&'+presel_met+'&&'+presel_metsig+'&&'+presel_flavour

#######################################################
#                 load all the samples                #
#######################################################
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *

backgrounds = [TTJets]


#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds:
  s['chain'] = getChain(s,histname="")

mllbinning = "(50,0,150)"

plots = {\
  'nominal':{
    'dl_mass':{'title':'m_{ll} (GeV)', 'name':'Mll', 'binning': mllbinning, 'histo':{}},
    },
  'topPt':{
    'dl_mass':{'title':'m_{ll} (GeV)', 'name':'Mll', 'binning': mllbinning, 'histo':{}},
    },
  
  }


#######################################################
#            Start filling in the histograms          #
#######################################################

for s in backgrounds:
  chain = s["chain"]
  for plot in plots['nominal'].keys():
    chain.Draw(plot+">>"+plot+s["name"]+plots['nominal'][plot]['binning'],"(weight)*("+preselection+")")
    plots['nominal'][plot]['histo'][s["name"]] = ROOT.gDirectory.Get(plot+s["name"])
  for plot in plots['topPt'].keys():
    chain.Draw(plot+">>"+plot+s["name"]+"_topPt"+plots['topPt'][plot]['binning'],"(weight*reweightTopPt)*("+preselection+")")
    plots['topPt'][plot]['histo'][s["name"]] = ROOT.gDirectory.Get(plot+s["name"]+"_topPt")

  for selection in plots.keys():

    nbinsx        = plots[selection][plot]['histo'][s['name']].GetNbinsX()
    lastbin       = plots[selection][plot]['histo'][s['name']].GetBinContent(nbinsx)
    error         = plots[selection][plot]['histo'][s['name']].GetBinError(nbinsx)
    overflowbin   = plots[selection][plot]['histo'][s['name']].GetBinContent(nbinsx+1)
    overflowerror = plots[selection][plot]['histo'][s['name']].GetBinError(nbinsx+1)
    plots[selection][plot]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
    plots[selection][plot]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
    plots[selection][plot]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
    plots[selection][plot]['histo'][s['name']].SetBinError(nbinsx+1,0.)

processtime = datetime.now()
print "Time to process chains: ", processtime - start

#######################################################
#             Drawing done here                       #
#######################################################

legendtextsize = 0.032

ROOT.gStyle.SetErrorX(0.5)

if makedraw1D: 
  for i,b in enumerate(backgrounds):
    for plot in plots['nominal'].keys():

      plots['nominal'][plot]['histo'][b["name"]].SetLineColor(ROOT.kBlue)
      plots['topPt'][plot]['histo'][b["name"]].SetLineColor(ROOT.kRed)

      l=ROOT.TLegend(0.5,0.8,0.95,1.0)
      l.SetFillColor(0)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      l.SetTextSize(legendtextsize)

      c1 = ROOT.TCanvas()

      pad1 = ROOT.TPad("pad1","pad1",0,0.3,1,1.0)
      pad1.SetBottomMargin(0)
      #pad1.SetGridx()
      pad1.Draw()
      pad1.cd()

      pad1.SetLogy()
      plots['nominal'][plot]['histo'][b["name"]].Draw("HIST")
      plots['topPt'][plot]['histo'][b["name"]].Draw("HISTSAME")
      
      l.AddEntry(plots['nominal'][plot]['histo'][b["name"]],"nominal")
      l.AddEntry(plots['topPt'][plot]['histo'][b["name"]],"reweighted")
      l.Draw()

      pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
      pad2.SetTopMargin(0)
      #pad2.SetGridx()
      pad2.Draw()
      pad2.cd()

      ratio = plots['nominal'][plot]['histo'][b["name"]].Clone()
      ratio.Divide(plots['topPt'][plot]['histo'][b["name"]])
      ratio.SetLineColor(ROOT.kBlack)
      ratio.SetMinimum(0.)
      ratio.SetMaximum(3)
      #ratio.SetMarkerStyle(21)
      #ratio.Draw("ep")

      ratio.GetXaxis().SetTitle(plots['nominal'][plot]['title'])

      c1.cd()
      path = plotDir+'/test/TopPtReweight/njet_2m_isOS'+'dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'/'
      if not os.path.exists(path): os.makedirs(path)
      c1.Print(path+plot+"_"+b["name"]+".png")

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start
