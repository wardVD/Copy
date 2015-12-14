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
metcut             = 0.
metsignifcut       = 0.
dphicut            = 0.25
mllcut             = 20
ngoodleptons       = 2
luminosity         = 10000/1000
mt2llcut           = 0.

presel_met         = 'met_pt>'+str(metcut)
#presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0'
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_ngoodlep    = '((nGoodMuons+nGoodElectrons)=='+str(ngoodleptons)+')'
presel_OS          = 'isOS'
presel_mt2ll       = 'dl_mt2ll>='+str(mt2llcut)
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'
presel_flavour     = 'isMuMu==1&&nGoodElectrons==0&&nGoodMuons==2&&HLT_mumuIso==1&&weight>0'


#preselection: MET>40, njets>=2, n_bjets>=1, n_lep>=2
#For now see here for the Sum$ syntax: https://root.cern.ch/root/html/TTree.html#TTree:Draw@2
preselection = presel_njet+'&&'+presel_OS+'&&'+presel_ngoodlep+'&&'+presel_mll+'&&'+presel_dPhi+'&&'+presel_met+'&&'+presel_metsig+'&&'+presel_mt2ll+'&&'+presel_flavour

#######################################################
#                 load all the samples                #
#######################################################
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *

backgrounds = [DY_HT_LO]
data = [DoubleMuon_Run2015D]#,DoubleEG_Run2015D,MuonEG_Run2015D]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

mt2llbinning = "(10,0,300)"
mllbinning = "(50,0,150)"

plots = {\
  'dl_mt2ll':{\
    '_onZ_0b': {'title':'MT2ll (GeV)', 'name':'MT2ll_onZ_b==0b',"legend":"(onZ,0 b-tag)", 'binning': mt2llbinning, 'histo':{}},
    '_offZ_0b': {'title':'MT2ll (GeV)', 'name':'MT2ll_offZ_b==0b',"legend":"(offZ,0 b-tag)",'binning': mt2llbinning, 'histo':{}},
    '_onZ_1mb': {'title':'MT2ll (GeV)', 'name':'MT2ll_onZ_b>=1', "legend":"(onZ,>0 b-tag)", 'binning': mt2llbinning, 'histo':{}},
    '_offZ_1mb': {'title':'MT2ll (GeV)', 'name':'MT2ll_offZ_b>=1', "legend":"(offZ,>0 b-tag)", 'binning': mt2llbinning, 'histo':{}},
    },
  'dl_mass':{\
    '_onZ_0b': {'title':'m_{ll} (GeV)', 'name':'Mll_onZ_b==0b', "legend":"(onZ,0 b-tag)",'binning': mllbinning, 'histo':{}},
    '_offZ_0b': {'title':'m_{ll} (GeV)', 'name':'Mll_offZ_b==0b', "legend":"(offZ,0 b-tag)", 'binning': mllbinning, 'histo':{}},
    '_onZ_1mb': {'title':'m_{ll} (GeV)', 'name':'Mll_onZ_b>=1', "legend":"(onZ,>0 b-tag)", 'binning': mllbinning, 'histo':{}},
    '_offZ_1mb': {'title':'m_{ll} (GeV)', 'name':'Mll_offZ_b>=1', "legend":"(offZ,>0 b-tag)", 'binning': mllbinning, 'histo':{}},
    },
  }


#######################################################
#            Start filling in the histograms          #
#######################################################

for s in backgrounds+data:
  chain = s["chain"]
  for plot in plots.keys():
    chain.Draw(plot+">>"+plot+"_onZ_0b"+s["name"]+plots[plot]['_onZ_0b']['binning'],preselection+'&&abs(dl_mass-90.2)<15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0')
    plots[plot]['_onZ_0b']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_onZ_0b"+s["name"])

    chain.Draw(plot+">>"+plot+"_offZ_0b"+s["name"]+plots[plot]['_offZ_0b']['binning'],preselection+'&&abs(dl_mass-90.2)>15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0')
    plots[plot]['_offZ_0b']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_offZ_0b"+s["name"])

    chain.Draw(plot+">>"+plot+"_onZ_1mb"+s["name"]+plots[plot]['_onZ_1mb']['binning'],preselection+'&&abs(dl_mass-90.2)<15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1')
    plots[plot]['_onZ_1mb']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_onZ_1mb"+s["name"])
 
    chain.Draw(plot+">>"+plot+"_offZ_1mb"+s["name"]+plots[plot]['_offZ_1mb']['binning'],preselection+'&&abs(dl_mass-90.2)>15&&Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')>=1')
    plots[plot]['_offZ_1mb']['histo'][s["name"]] = ROOT.gDirectory.Get(plot+"_offZ_1mb"+s["name"])
    

    for selection in plots[plot].keys():
      #plots[plot][selection]['histo'][s['name']].Sumw2()
      nbinsx        = plots[plot][selection]['histo'][s['name']].GetNbinsX()
      lastbin       = plots[plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
      error         = plots[plot][selection]['histo'][s['name']].GetBinError(nbinsx)
      overflowbin   = plots[plot][selection]['histo'][s['name']].GetBinContent(nbinsx+1)
      overflowerror = plots[plot][selection]['histo'][s['name']].GetBinError(nbinsx+1)
      plots[plot][selection]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
      plots[plot][selection]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
      plots[plot][selection]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
      plots[plot][selection]['histo'][s['name']].SetBinError(nbinsx+1,0.)

processtime = datetime.now()
print "Time to process chains: ", processtime - start

#######################################################
#             Drawing done here                       #
#######################################################

legendtextsize = 0.032

ROOT.gStyle.SetErrorX(0.5)

if makedraw1D: 
  for i,b in enumerate(backgrounds+data):
    for plot in plots.keys():

    #Make a stack for backgrounds
      l=ROOT.TLegend(0.5,0.8,0.95,1.0)
      l.SetFillColor(0)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      l.SetTextSize(legendtextsize)

    #Plot!
      c1 = ROOT.TCanvas()

      
      integralON0b = plots[plot]["_onZ_0b"]['histo'][b["name"]].Integral()
      integralOFF0b = plots[plot]["_offZ_0b"]['histo'][b["name"]].Integral()
      integralON1b = plots[plot]["_onZ_1mb"]['histo'][b["name"]].Integral()
      integralOFF1b = plots[plot]["_offZ_1mb"]['histo'][b["name"]].Integral()

      #plots[plot]["_onZ_0b"]['histo'][b["name"]].Scale(1./(integralON0b+integralOFF0b))
      #plots[plot]["_offZ_0b"]['histo'][b["name"]].Scale(1./(integralON0b+integralOFF0b))
      #plots[plot]["_onZ_1mb"]['histo'][b["name"]].Scale(1./(integralON1b+integralOFF1b))
      #plots[plot]["_offZ_1mb"]['histo'][b["name"]].Scale(1./(integralON1b+integralOFF1b))

      plots[plot]["_onZ_0b"]['histo'][b["name"]].Scale(1./integralON0b)
      plots[plot]["_offZ_0b"]['histo'][b["name"]].Scale(1./integralOFF0b)
      plots[plot]["_onZ_1mb"]['histo'][b["name"]].Scale(1./integralON1b)
      plots[plot]["_offZ_1mb"]['histo'][b["name"]].Scale(1./integralOFF1b)

      for j,selection in enumerate(sorted(plots[plot].keys(),key=lambda sort:plots[plot][sort]['histo'][b['name']].Integral(),reverse=True)):
        #plots[plot][selection]['histo'][b["name"]].Scale(1./integral)

        plots[plot][selection]['histo'][b["name"]].SetLineColor(j+1)
        plots[plot][selection]['histo'][b["name"]].SetLineWidth(1)
        plots[plot][selection]['histo'][b["name"]].SetMarkerColor(j+1)
        plots[plot][selection]['histo'][b["name"]].Draw("pe1same")

        if j == 0: 
          plots[plot][selection]['histo'][b["name"]].GetXaxis().SetTitle(plots[plot][selection]['title'])
          plots[plot][selection]['histo'][b["name"]].GetYaxis().SetTitle("Events (A.U.)")
          plots[plot][selection]['histo'][b["name"]].GetYaxis().SetRangeUser(0.00001,3)
        l.AddEntry(plots[plot][selection]['histo'][b["name"]],plots[plot][selection]['legend'])
      c1.SetLogy()
      l.Draw()
      path = plotDir+'/test/DYstudy/njet_2m_isOS'+'_ngoodlep_'+str(ngoodleptons)+'_mt2ll_'+str(int(mt2llcut))+'dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'/'
      if not os.path.exists(path): os.makedirs(path)
      c1.Print(path+plot+"_"+b["name"]+"_"+presel_flavour+".png")

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start
