import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()
import numpy

from math import *
from StopsDilepton.tools.helpers import getChain,getWeight,getVarValue, getEList
from StopsDilepton.tools.localInfo import *
from datetime import datetime
from StopsDilepton.tools.puReweighting import getReweightingFunction
from StopsDilepton.tools.objectSelection import getLeptons, looseMuID, looseEleID, getJets, getGenParts, getGoodLeptons, getGoodElectrons, getGoodMuons

puReweightingFunc = getReweightingFunction(era="doubleMu_onZ_isOS_1500pb_nVert_reweight")
puReweighting = lambda c:puReweightingFunc(getVarValue(c, "nVert"))


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
luminosity         = 1549.
mt2llcut           = 0.

presel_met         = 'met_pt>'+str(metcut)
#presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')==0'
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_OS          = 'isOS'
presel_mt2ll       = 'dl_mt2ll>='+str(mt2llcut)
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'
presel_flavour     = 'isMuMu==1&&nGoodElectrons==0&&nGoodMuons==2&&HLT_mumuIso'

datacut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

#preselection: MET>40, njets>=2, n_bjets>=1, n_lep>=2
#For now see here for the Sum$ syntax: https://root.cern.ch/root/html/TTree.html#TTree:Draw@2
preselection = presel_njet+'&&'+presel_OS+'&&'+presel_mll+'&&'+presel_dPhi+'&&'+presel_met+'&&'+presel_metsig+'&&'+presel_mt2ll+'&&'+presel_flavour

#######################################################
#                 load all the samples                #
#######################################################
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *

backgrounds = [DY,TTJets]
data = [DoubleMuon_Run2015D]#,DoubleEG_Run2015D,MuonEG_Run2015D]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

mt2llbinning = [15,0,300]
mllbinning = [50,0,150]

plots = {\
  '0b':{\
    'dl_mt2ll':{\
      '_onZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_onZ_b==0b', 'binning': mt2llbinning, 'histo':{}},
      '_offZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_offZ_b==0b',  'binning': mt2llbinning, 'histo':{}},
      '_allZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_allZ_b==0b',  'binning': mt2llbinning, 'histo':{}},
      },
    'dl_mass':{\
      '_onZ': {'title':'M_{ll} (GeV)', 'name':'Mll_onZ_b==0b', 'binning': mllbinning, 'histo':{}},
      '_offZ': {'title':'M_{ll} (GeV)', 'name':'Mll_offZ_b==0b',  'binning': mllbinning, 'histo':{}},
      '_allZ': {'title':'M_{ll} (GeV)', 'name':'Mll_allZ_b==0b',  'binning': mllbinning, 'histo':{}},\
      },
    },
  '1mb':{\
    'dl_mt2ll':{\
      '_onZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_onZ_b>=1',  'binning': mt2llbinning, 'histo':{}},
      '_offZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_offZ_b>=1',  'binning': mt2llbinning, 'histo':{}},
      '_allZ': {'title':'M^{2}_{T}(ll) (GeV)', 'name':'MT2ll_allZ_b>=1',  'binning': mt2llbinning, 'histo':{}},
      },
    'dl_mass':{\
      '_onZ': {'title':'M_{ll} (GeV)', 'name':'Mll_onZ_b>=1',  'binning': mllbinning, 'histo':{}},
      '_offZ': {'title':'M_{ll} (GeV)', 'name':'Mll_offZ_b>=1',  'binning': mllbinning, 'histo':{}},
      '_allZ': {'title':'M_{ll} (GeV)', 'name':'Mll_allZ_b>=1',  'binning': mllbinning, 'histo':{}},
      },
    },
  }


#######################################################
#            Start filling in the histograms          #
#######################################################
for s in backgrounds+data:
  #construct 1D histograms
  for bjet in plots.keys():
    for pk in plots[bjet].keys():
      for plot in plots[bjet][pk].keys():
        plots[bjet][pk][plot]['histo'][s["name"]] = ROOT.TH1D(plots[bjet][pk][plot]['name']+"_"+s["name"]+"_"+pk, plots[bjet][pk][plot]['name']+"_"+s["name"]+"_"+pk, *plots[bjet][pk][plot]['binning'])
        plots[bjet][pk][plot]['histo'][s["name"]].Sumw2()

  chain = s["chain"]

  eList = getEList(chain, preselection) if not s['isData'] else getEList(chain, preselection+'&&'+datacut)
  
  nEvents = eList.GetN()/reduceStat
  print "Found %i events in %s after preselection %s, looping over %i" % (eList.GetN(),s["name"],preselection,nEvents)
 
  for ev in range(nEvents):

    increment = 50
    if nEvents>increment and ev%(nEvents/increment)==0: 
      sys.stdout.write('\r' + "=" * (ev / (nEvents/increment)) +  " " * ((nEvents - ev)/ (nEvents/increment)) + "]" +  str(round((ev+1) / (float(nEvents)/100),2)) + "%")
      sys.stdout.flush()
      sys.stdout.write('\r')
    chain.GetEntry(eList.GetEntry(ev))

    pileupweight = puReweighting(chain) if not s['isData'] else 1.
    
    weight = reduceStat*getVarValue(chain, "weight")*(luminosity/1000.)*pileupweight if not s['isData'] else 1
    
    mll = getVarValue(chain,"dl_mass")
    mt2ll = getVarValue(chain,"dl_mt2ll")

    #bjet requirement
    jets  = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'], getJets(chain))
    bjets = filter(lambda j:j['btagCSV']>btagcoeff, jets)

    if len(bjets)==0:
      plots['0b']['dl_mass']["_allZ"]['histo'][s["name"]].Fill(mll, weight)
      plots['0b']['dl_mt2ll']["_allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      if abs(mll-90.2)<15:
        plots['0b']['dl_mass']["_onZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['0b']['dl_mt2ll']["_onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      else:
        plots['0b']['dl_mass']["_offZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['0b']['dl_mt2ll']["_offZ"]['histo'][s["name"]].Fill(mt2ll, weight)
    elif len(bjets)>=1:
      plots['1mb']['dl_mass']["_allZ"]['histo'][s["name"]].Fill(mll, weight)
      plots['1mb']['dl_mt2ll']["_allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      if abs(mll-90.2)<15:
        plots['1mb']['dl_mass']["_onZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['1mb']['dl_mt2ll']["_onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      else:
        plots['1mb']['dl_mass']["_offZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['1mb']['dl_mt2ll']["_offZ"]['histo'][s["name"]].Fill(mt2ll, weight)

  for bjet in plots.keys():
    for plot in plots[bjet].keys():  
      for selection in plots[bjet][plot].keys():
      #plots[plot][selection]['histo'][s['name']].Sumw2()
        nbinsx        = plots[bjet][plot][selection]['histo'][s['name']].GetNbinsX()
        lastbin       = plots[bjet][plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
        error         = plots[bjet][plot][selection]['histo'][s['name']].GetBinError(nbinsx)
        overflowbin   = plots[bjet][plot][selection]['histo'][s['name']].GetBinContent(nbinsx+1)
        overflowerror = plots[bjet][plot][selection]['histo'][s['name']].GetBinError(nbinsx+1)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
        plots[bjet][plot][selection]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinError(nbinsx+1,0.)
        
processtime = datetime.now()
print "Time to process chains: ", processtime - start

#######################################################
#             Drawing done here                       #
#######################################################

legendtextsize = 0.032
a=[]
#ROOT.gStyle.SetErrorX(0.5)

if makedraw1D:
  for bjet in plots.keys():
    for plot in plots[bjet].keys():

    #Make a stack for backgrounds
      l=ROOT.TLegend(0.5,0.8,0.95,1.0)
      l.SetFillColor(0)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      l.SetTextSize(legendtextsize)

    #Plot!
      c1 = ROOT.TCanvas()

    #for j,selection in enumerate(sorted(plots[plot].keys(),key=lambda sort:plots[plot][sort]['histo'][b['name']].Integral(),reverse=True)):
      totalbkg = 0
      for b in backgrounds:
        totalbkg += plots[bjet][plot]["_allZ"]['histo'][b["name"]].Integral()
      dataint = plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].Integral()

      print "Scaling factor data/MC: ", dataint/totalbkg

      bkg_stack = ROOT.THStack("bkgs","bkgs") 
      for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots[bjet][plot]["_allZ"]["histo"][sort["name"]].Integral())):
        plots[bjet][plot]["_allZ"]['histo'][b["name"]].Scale(dataint/totalbkg)
        plots[bjet][plot]["_allZ"]['histo'][b["name"]].SetMarkerSize(0)
        plots[bjet][plot]["_allZ"]['histo'][b["name"]].SetFillColor(b["color"])
        plots[bjet][plot]["_allZ"]['histo'][b["name"]].SetLineWidth(1)
        bkg_stack.Add(plots[bjet][plot]["_allZ"]['histo'][b["name"]],"h")
        l.AddEntry(plots[bjet][plot]["_allZ"]['histo'][b["name"]],b['name'])
        for selection in plots[bjet][plot].keys():
          print b["texName"], plot, selection , bjet, '\t \t',plots[bjet][plot][selection]['histo'][b["name"]].Integral()
      for selection in plots[bjet][plot].keys():
        print data[0]["texName"], plot, selection, bjet, '\t \t', plots[bjet][plot][selection]['histo'][data[0]["name"]].Integral()
      
      plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots[bjet][plot]["_allZ"]['title'])
      plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
      plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.01,100000)
      plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].Draw("pe1same")
      bkg_stack.Draw("same")
      plots[bjet][plot]["_allZ"]['histo'][data[0]["name"]].Draw("pe1same")

      c1.SetLogy()
      ROOT.gPad.RedrawAxis()
      l.Draw()
      path = plotDir+'/test/DYstudy/njet_2m_isOS'+'_mt2ll_'+str(int(mt2llcut))+'dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'/'
      if not os.path.exists(path): os.makedirs(path)
      c1.Print(path+plot+"_"+bjet+".png")

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start
