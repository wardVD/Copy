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
reduceStat = 1 #recude the statistics, i.e. 10 is ten times less samples to look at
makedraw1D = True
makeTexFile = True
mt2llcutscaling = False
noscaling = False

btagcoeff          = 0.89
metcut             = 80.
metsignifcut       = 5.
dphicut            = 0.25
mllcut             = 20
ngoodleptons       = 2
#luminosity         = 1549.
mt2llcut           = 100.
flavour            = "MuMu"

presel_met         = 'met_pt>'+str(metcut)
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)>=2'
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_OS          = 'isOS'
presel_mt2ll       = 'dl_mt2ll>='+str(mt2llcut)
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'

if flavour=="MuMu": 
  presel_flavour     = 'isMuMu==1&&nGoodElectrons==0&&nGoodMuons==2&&HLT_mumuIso'
  data = [DoubleMuon_Run2015D]
elif flavour=="EE": 
  presel_flavour     = 'isEE==1&&nGoodElectrons==2&&nGoodMuons==0&&HLT_ee_DZ'
  data = [DoubleEG_Run2015D]
elif flavour=="EMu": 
  presel_flavour     = 'isEMu==1&&nGoodElectrons==1&&nGoodMuons==1&&HLT_mue'
  data = [MuonEG_Run2015D]

luminosity = data[0]["lumi"]

datacut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

preselection = presel_njet+'&&'+presel_OS+'&&'+presel_mll+'&&'+presel_dPhi+'&&'+presel_met+'&&'+presel_metsig+'&&'+presel_flavour

backgrounds = [DY_HT_LO,TTJets,WJetsToLNu,singleTop,QCD_Mu5,TTX,diBoson]
#backgrounds = [DY_HT_LO,TTJets]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

mt2llbinning = [15,0,300]
mllbinning = [50,0,150]
metbinning = [30,0,300]

plots = {\
  '0b':{\
    'dl_mt2ll':{\
      'onZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_onZ_b==0b', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_offZ_b==0b',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_allZ_b==0b',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      'onZ': {'title':'M_{ll} (GeV)', 'name':'Mll_onZ_b==0b', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'M_{ll} (GeV)', 'name':'Mll_offZ_b==0b',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'M_{ll} (GeV)', 'name':'Mll_allZ_b==0b',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      'onZ': {'title':'MET (GeV)', 'name':'MET_onZ_b==0b', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MET (GeV)', 'name':'MET_offZ_b==0b',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MET (GeV)', 'name':'MET_allZ_b==0b',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  '1mb':{\
    'dl_mt2ll':{\
      'onZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_onZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_offZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MT2ll (GeV)', 'name':'MT2ll_allZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      'onZ': {'title':'M_{ll} (GeV)', 'name':'Mll_onZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'M_{ll} (GeV)', 'name':'Mll_offZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'M_{ll} (GeV)', 'name':'Mll_allZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      'onZ': {'title':'MET (GeV)', 'name':'MET_onZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MET (GeV)', 'name':'MET_offZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MET (GeV)', 'name':'MET_allZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  }

plots_cut = {\
  '0b':{\
    'dl_mt2ll':{\
      'onZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_onZ_b==0b', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_offZ_b==0b',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_allZ_b==0b',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      'onZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_onZ_b==0b', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_offZ_b==0b',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_allZ_b==0b',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      'onZ': {'title':'MET (GeV)', 'name':'METcut_onZ_b==0b', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MET (GeV)', 'name':'METcut_offZ_b==0b',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MET (GeV)', 'name':'METcut_allZ_b==0b',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      },
    },
  '1mb':{\
    'dl_mt2ll':{\
      'onZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_onZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_offZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MT2ll (GeV)', 'name':'MT2llcut_allZ_b>=1',  'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
      },
    'dl_mass':{\
      'onZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_onZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_offZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'M_{ll} (GeV)', 'name':'Mllcut_allZ_b>=1',  'binning': mllbinning, 'histo':{'totalbkg':0.,}},
      },
    'met_pt':{\
      'onZ': {'title':'MET (GeV)', 'name':'METcut_onZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'offZ': {'title':'MET (GeV)', 'name':'METcut_offZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
      'allZ': {'title':'MET (GeV)', 'name':'METcut_allZ_b>=1',  'binning': metbinning, 'histo':{'totalbkg':0.,}},
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
  for bjet in plots_cut.keys():
    for pk in plots_cut[bjet].keys():
      for plot in plots_cut[bjet][pk].keys():
        plots_cut[bjet][pk][plot]['histo'][s["name"]] = ROOT.TH1D(plots_cut[bjet][pk][plot]['name']+"_"+s["name"]+"_"+pk, plots_cut[bjet][pk][plot]['name']+"_"+s["name"]+"_"+pk, *plots_cut[bjet][pk][plot]['binning'])
        plots_cut[bjet][pk][plot]['histo'][s["name"]].Sumw2()

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

    #pileupweight = puReweighting(chain) if not s['isData'] else 1.
    
    weight = reduceStat*getVarValue(chain, "weight")*(luminosity/1000.) if not s['isData'] else 1
    
    mll = getVarValue(chain,"dl_mass")
    mt2ll = getVarValue(chain,"dl_mt2ll")
    met = getVarValue(chain,"met_pt")

    #bjet requirement
    jets  = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'], getJets(chain))
    bjets = filter(lambda j:j['btagCSV']>btagcoeff, jets)

    if len(bjets)==0:
      plots['0b']['dl_mass']["allZ"]['histo'][s["name"]].Fill(mll, weight)
      plots['0b']['dl_mt2ll']["allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      plots['0b']['met_pt']["allZ"]['histo'][s["name"]].Fill(met, weight)
      if mt2ll>=mt2llcut:
        plots_cut['0b']['dl_mass']["allZ"]['histo'][s["name"]].Fill(mll, weight)
        plots_cut['0b']['dl_mt2ll']["allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots_cut['0b']['met_pt']["allZ"]['histo'][s["name"]].Fill(met, weight)
      if abs(mll-91.2)<15:
        plots['0b']['dl_mass']["onZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['0b']['dl_mt2ll']["onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots['0b']['met_pt']["onZ"]['histo'][s["name"]].Fill(met, weight)
        if mt2ll>=mt2llcut:
          plots_cut['0b']['dl_mass']["onZ"]['histo'][s["name"]].Fill(mll, weight)
          plots_cut['0b']['dl_mt2ll']["onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
          plots_cut['0b']['met_pt']["onZ"]['histo'][s["name"]].Fill(met, weight)
      else:
        plots['0b']['dl_mass']["offZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['0b']['dl_mt2ll']["offZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots['0b']['met_pt']["offZ"]['histo'][s["name"]].Fill(met, weight)
        if mt2ll>=mt2llcut:
          plots_cut['0b']['dl_mass']["offZ"]['histo'][s["name"]].Fill(mll, weight)
          plots_cut['0b']['dl_mt2ll']["offZ"]['histo'][s["name"]].Fill(mt2ll, weight)
          plots_cut['0b']['met_pt']["offZ"]['histo'][s["name"]].Fill(met, weight)
    elif len(bjets)>=1:
      plots['1mb']['dl_mass']["allZ"]['histo'][s["name"]].Fill(mll, weight)
      plots['1mb']['dl_mt2ll']["allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
      plots['1mb']['met_pt']["allZ"]['histo'][s["name"]].Fill(met, weight)
      if mt2ll>=mt2llcut:
        plots_cut['1mb']['dl_mass']["allZ"]['histo'][s["name"]].Fill(mll, weight)
        plots_cut['1mb']['dl_mt2ll']["allZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots_cut['1mb']['met_pt']["allZ"]['histo'][s["name"]].Fill(met, weight)
      if abs(mll-91.2)<15:
        plots['1mb']['dl_mass']["onZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['1mb']['dl_mt2ll']["onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots['1mb']['met_pt']["onZ"]['histo'][s["name"]].Fill(met, weight)
        if mt2ll>=mt2llcut:
          plots_cut['1mb']['dl_mass']["onZ"]['histo'][s["name"]].Fill(mll, weight)
          plots_cut['1mb']['dl_mt2ll']["onZ"]['histo'][s["name"]].Fill(mt2ll, weight)
          plots_cut['1mb']['met_pt']["onZ"]['histo'][s["name"]].Fill(met, weight)
      else:
        plots['1mb']['dl_mass']["offZ"]['histo'][s["name"]].Fill(mll, weight)
        plots['1mb']['dl_mt2ll']["offZ"]['histo'][s["name"]].Fill(mt2ll, weight)
        plots['1mb']['met_pt']["offZ"]['histo'][s["name"]].Fill(met, weight)
        if mt2ll>=mt2llcut:
          plots_cut['1mb']['dl_mass']["offZ"]['histo'][s["name"]].Fill(mll, weight)
          plots_cut['1mb']['dl_mt2ll']["offZ"]['histo'][s["name"]].Fill(mt2ll, weight)
          plots_cut['1mb']['met_pt']["offZ"]['histo'][s["name"]].Fill(met, weight)
  #overflow
  for bjet in plots.keys():
    for plot in plots[bjet].keys():  
      for selection in plots[bjet][plot].keys():
        nbinsx        = plots[bjet][plot][selection]['histo'][s['name']].GetNbinsX()
        lastbin       = plots[bjet][plot][selection]['histo'][s['name']].GetBinContent(nbinsx)
        error         = plots[bjet][plot][selection]['histo'][s['name']].GetBinError(nbinsx)
        overflowbin   = plots[bjet][plot][selection]['histo'][s['name']].GetBinContent(nbinsx+1)
        overflowerror = plots[bjet][plot][selection]['histo'][s['name']].GetBinError(nbinsx+1)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
        plots[bjet][plot][selection]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
        plots[bjet][plot][selection]['histo'][s['name']].SetBinError(nbinsx+1,0.)
        #Remove bins with negative events
        for i in range(nbinsx):
          if plots[bjet][plot][selection]['histo'][s['name']].GetBinContent(i+1) < 0: plots[bjet][plot][selection]['histo'][s['name']].SetBinContent(i+1,0.)
        
processtime = datetime.now()
print "Time to process chains: ", processtime - start


for bjet in plots.keys():
  for plot in plots[bjet].keys():
    for zregion in plots[bjet][plot].keys():
      totalbkg = 0
      if mt2llcutscaling:
        for b in backgrounds:
          totalbkg += plots_cut[bjet][plot][zregion]['histo'][b["name"]].Integral()
        dataint = plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].Integral()
      else:
        for b in backgrounds:
          totalbkg += plots[bjet][plot][zregion]['histo'][b["name"]].Integral()
        dataint = plots[bjet][plot][zregion]['histo'][data[0]["name"]].Integral()

      print "Scaling factor data/MC for " +bjet+" and Z-region " + zregion + ": ", dataint/totalbkg
      for b in backgrounds:
        if noscaling:
          plots[bjet][plot][zregion]['SF'] = 1.
          plots_cut[bjet][plot][zregion]['SF'] = 1.
        else:
          plots[bjet][plot][zregion]['histo'][b["name"]].Scale(dataint/totalbkg)
          plots_cut[bjet][plot][zregion]['histo'][b["name"]].Scale(dataint/totalbkg)
          plots[bjet][plot][zregion]['SF'] = dataint/totalbkg
          plots_cut[bjet][plot][zregion]['SF'] = dataint/totalbkg

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
  for bjet in plots.keys():
    for plot in plots[bjet].keys():
      for zregion in plots[bjet][plot].keys():
        l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
        a.append(l)
        l.SetFillColor(0)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        l.SetTextSize(legendtextsize)

        bkg_stack = ROOT.THStack("bkgs","bkgs") 
        totalbackground = plots[bjet][plot][zregion]['histo'][backgrounds[0]['name']].Clone()
        for b in backgrounds:
          if b!= backgrounds[0]:totalbackground.Add(plots[bjet][plot][zregion]['histo'][b['name']])

        for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots[bjet][plot][zregion]["histo"][sort["name"]].Integral())):
          plots[bjet][plot][zregion]['histo'][b["name"]].SetMarkerSize(0)
          plots[bjet][plot][zregion]['histo'][b["name"]].SetFillColor(b["color"])
          plots[bjet][plot][zregion]['histo'][b["name"]].SetLineWidth(1)
          bkg_stack.Add(plots[bjet][plot][zregion]['histo'][b["name"]],"h")
          l.AddEntry(plots[bjet][plot][zregion]['histo'][b["name"]],b['texName'],"f")

        c1 = ROOT.TCanvas("c1","c1",800,800)
        pad1 = ROOT.TPad("","",histopad[0],histopad[1],histopad[2],histopad[3])
        a.append(pad1)
        pad1.SetBottomMargin(0)
        pad1.SetTopMargin(0)
        pad1.SetRightMargin(0)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy()
        plots[bjet][plot][zregion]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.Draw("same")
        plots[bjet][plot][zregion]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.GetXaxis().SetLabelSize(0.)
        l.Draw()
        ROOT.gPad.RedrawAxis()

        plots[bjet][plot][zregion]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots[bjet][plot]["allZ"]['title'])
        plots[bjet][plot][zregion]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
        plots[bjet][plot][zregion]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.01,100000)
        l.AddEntry(plots[bjet][plot][zregion]['histo'][data[0]["name"]],data[0]['texName'])

        channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
        lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
        scaletag = ROOT.TPaveText(scalepos[0],scalepos[1],scalepos[2],scalepos[3],"NDC")
        channeltag.AddText(flavour)
        lumitag.AddText("lumi: "+str(data[0]['lumi'])+' pb^{-1}')
        scaletag.AddText("Scale Factor: " +str(round(plots[bjet][plot][zregion]['SF'],2)))
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
        ratio = plots[bjet][plot][zregion]['histo'][data[0]["name"]].Clone()
        a.append(ratio)
        ratio.Divide(totalbackground)
        ratio.SetMarkerStyle(20)
        ratio.GetYaxis().SetTitle("Data/Bkg.")
      #ratio.GetYaxis().SetNdivisions(502)
        ratio.GetXaxis().SetTitle(plots[bjet][plot][zregion]['title'])
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
        if not mt2llcutscaling: path = plotDir+'/test/DYstudy/'+flavour+'_'+zregion+'_njet_2m_isOS_dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'/'
        else:            path = plotDir+'/test/DYstudy/'+flavour+'_'+zregion+'_njet_2m_isOS_dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'_mt2llscaling/'
        if not os.path.exists(path): os.makedirs(path)
        c1.Print(path+plot+"_"+bjet+".png")
        del ratio
        del pad1
        del pad2
        c1.Clear()

  for bjet in plots_cut.keys():
    for plot in plots_cut[bjet].keys():
      for zregion in plots_cut[bjet][plot].keys():
        l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
        a.append(l)
        l.SetFillColor(0)
        l.SetShadowColor(ROOT.kWhite)
        l.SetBorderSize(1)
        l.SetTextSize(legendtextsize)
        c1 = ROOT.TCanvas()

        bkg_stack = ROOT.THStack("bkgs","bkgs") 
        totalbackground = plots_cut[bjet][plot][zregion]['histo'][backgrounds[0]['name']].Clone()
        for b in backgrounds:
          if b!= backgrounds[0]:totalbackground.Add(plots_cut[bjet][plot][zregion]['histo'][b['name']])

        for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots_cut[bjet][plot][zregion]["histo"][sort["name"]].Integral())):
          plots_cut[bjet][plot][zregion]['histo'][b["name"]].SetMarkerSize(0)
          plots_cut[bjet][plot][zregion]['histo'][b["name"]].SetFillColor(b["color"])
          plots_cut[bjet][plot][zregion]['histo'][b["name"]].SetLineWidth(1)
          bkg_stack.Add(plots_cut[bjet][plot][zregion]['histo'][b["name"]],"h")
          l.AddEntry(plots_cut[bjet][plot][zregion]['histo'][b["name"]],b['name'],"f")

        c1 = ROOT.TCanvas("c1","c1",800,800)
        pad1 = ROOT.TPad("","",histopad[0],histopad[1],histopad[2],histopad[3])
        a.append(pad1)
        pad1.SetBottomMargin(0)
        pad1.SetTopMargin(0)
        pad1.SetRightMargin(0)
        pad1.Draw()
        pad1.cd()
        pad1.SetLogy()
        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.Draw("same")
        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].Draw("pe1same")
        bkg_stack.GetXaxis().SetLabelSize(0.)
        l.Draw()
        ROOT.gPad.RedrawAxis()

        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots_cut[bjet][plot]["allZ"]['title'])
        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.01,100000)
        plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].Draw("pe1same")
        l.AddEntry(plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]],data[0]['name'])

        channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
        lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
        scaletag = ROOT.TPaveText(scalepos[0],scalepos[1],scalepos[2],scalepos[3],"NDC")
        channeltag.AddText(flavour)
        lumitag.AddText("lumi: "+str(data[0]['lumi'])+' pb^{-1}')
        scaletag.AddText("Scale Factor: " +str(round(plots_cut[bjet][plot][zregion]['SF'],2)))
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
        ratio = plots_cut[bjet][plot][zregion]['histo'][data[0]["name"]].Clone()
        a.append(ratio)
        ratio.Divide(totalbackground)
        ratio.SetMarkerStyle(20)
        ratio.GetYaxis().SetTitle("Data/Bkg.")
      #ratio.GetYaxis().SetNdivisions(502)
        ratio.GetXaxis().SetTitle(plots_cut[bjet][plot][zregion]['title'])
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
        if not mt2llcutscaling: path = plotDir+'/test/DYstudy/'+flavour+'_'+zregion+'_njet_2m_isOS_dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'_mt2llcut_'+str(mt2llcut)+'/'
        else:            path = plotDir+'/test/DYstudy/'+flavour+'_'+zregion+'_njet_2m_isOS_dPhi_0.25_met_'+str(int(metcut))+'_metsig_'+str(int(metsignifcut))+'_mll_'+str(int(mllcut))+'_mt2llcut_'+str(mt2llcut)+'_mt2llscaling/'
        if not os.path.exists(path): os.makedirs(path)
        c1.Print(path+plot+"_"+bjet+".png")
        del ratio
        del pad1
        del pad2

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start


if makeTexFile:

  #NO MT2LLCUT
  if not mt2llcutscaling: output = open("./texfiles/DYnumbers"+flavour+".tex",'w')
  else:            output = open("./texfiles/DYnumbers"+flavour+"_mt2llscaling.tex",'w')

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
  string = '\\multirow{2}{*}{MT2ll $\\geq$ 0}'
  string2 = ''
  string3 = ''
  string4 = ''
  string4_5 = 'Total Bkg'
  string5 = 'Scale Factor'
  output.write("\\hline" + "\n")

  for bjet in sorted(plots.keys()):
    string += "& \\multicolumn{3}{|c||}{" +bjet+"}" if (bjet != sorted(plots.keys())[-1]) else "& \\multicolumn{3}{|c|}{" +bjet+"}"
    for selection in sorted(plots[bjet]["dl_mass"].keys()):
      string2 += "& " + selection
  for s in backgrounds:
    string3 += s["name"].replace("_","\\_") + " & "
    for bjet in sorted(plots.keys()):
      for selection in sorted(plots[bjet]["dl_mass"].keys()):
        nbins    = plots[bjet][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots[bjet][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        plots[bjet][plot][selection]['histo']['totalbkg'] += integral
        error    = round(double[0],2)
        string3 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots[bjet]["dl_mass"].keys())[-1]) and (bjet == sorted(plots.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string3 += '\\\\ \\hline \n'
  for s in data:
    string4 += s["name"].replace("_","\\_") + " & "
    for bjet in sorted(plots.keys()):
      for selection in sorted(plots[bjet]["dl_mass"].keys()):
        nbins    = plots[bjet][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots[bjet][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        error    = round(double[0],2)
        string4 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots[bjet]["dl_mass"].keys())[-1]) and (bjet == sorted(plots.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string4 += '\\\\ \\hline \n'
  for bjet in sorted(plots.keys()):
    for selection in sorted(plots[bjet]["dl_mass"].keys()):
      string4_5 += " & " + str(round(plots[bjet][plot][selection]['histo']['totalbkg'],2))
      string5 += " & " + str(round(plots[bjet][plot][selection]['SF'],2))
  output.write(string + '\\\\ \\cline{2-7} \n')
  output.write(string2 + '\\\\ \\hline \\hline \n')
  output.write(string3)
  output.write(string4 + "\\hline" + '\n')
  output.write(string4_5 + " \\\\ \\hline" + '\n')
  output.write(string5 + " \\\\ \\hline" + '\n')

  output.write("\\end{tabular}" + '\n')
  output.write('\\end{document}')


  #WITH MT2LLCUT
  if not mt2llcutscaling: output = open("./texfiles/DYnumbers"+flavour+"_MT2llcut_"+str(mt2llcut)+".tex",'w')
  else:            output = open("./texfiles/DYnumbers"+flavour+"_MT2llcut_"+str(mt2llcut)+"_mt2llscaling.tex",'w')


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
  for bjet in sorted(plots_cut.keys()):
    string += "& \\multicolumn{3}{|c||}{" +bjet+"}" if (bjet != sorted(plots_cut.keys())[-1]) else "& \\multicolumn{3}{|c|}{" +bjet+"}"
    for selection in sorted(plots_cut[bjet]["dl_mass"].keys()):
      string2 += "& " + selection
  for s in backgrounds:
    string3 += s["name"].replace("_","\\_") + " & "
    for bjet in sorted(plots_cut.keys()):
      for selection in sorted(plots_cut[bjet]["dl_mass"].keys()):
        nbins    = plots_cut[bjet][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots_cut[bjet][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        plots_cut[bjet][plot][selection]['histo']['totalbkg'] += integral
        error    = round(double[0],2)
        string3 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots_cut[bjet]["dl_mass"].keys())[-1]) and (bjet == sorted(plots_cut.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string3 += '\\\\ \\hline \n'
  for s in data:
    string4 += s["name"].replace("_","\\_") + " & "
    for bjet in sorted(plots_cut.keys()):
      for selection in sorted(plots_cut[bjet]["dl_mass"].keys()):
        nbins    = plots_cut[bjet][plot][selection]['histo'][s["name"]].GetNbinsX()
        integral = round(plots_cut[bjet][plot][selection]['histo'][s["name"]].IntegralAndError(1,nbins,double),2)
        error    = round(double[0],2)
        string4 += str(integral) + " $\\pm$ " +str(error) if ((selection == sorted(plots_cut[bjet]["dl_mass"].keys())[-1]) and (bjet == sorted(plots_cut.keys())[-1])) else str(integral) + " $\\pm$ " +str(error) + " & "
    string4 += '\\\\ \\hline \n'
  for bjet in sorted(plots.keys()):
    for selection in sorted(plots[bjet]["dl_mass"].keys()):
      string4_5 += " & " + str(round(plots_cut[bjet][plot][selection]['histo']['totalbkg'],2))
      string5 += " & " + str(round(plots_cut[bjet][plot][selection]['SF'],2))
  output.write(string + '\\\\ \\cline{2-7} \n')
  output.write(string2 + '\\\\ \\hline \\hline \n')
  output.write(string3)
  output.write(string4 + "\\hline" + '\n')
  output.write(string4_5 + " \\\\ \\hline" + '\n')
  output.write(string5 + " \\\\ \\hline" + '\n')

  output.write("\\end{tabular}" + '\n')
  output.write('\\end{document}')
