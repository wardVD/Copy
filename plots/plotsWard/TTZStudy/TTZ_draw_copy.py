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

btagcoeff          = 0.605
metcut             = 0.
metsignifcut       = 0.
dphicut            = 0.
mllcut             = 20
mt2llcut           = 100.
njetscut           = [">=4",'4m']
nbjetscut          = [">=2",'2m']


presel_met         = 'met_pt>'+str(metcut)
presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)'+njetscut[0]
presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')'+nbjetscut[0]
presel_metsig      = 'met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>'+str(metsignifcut)
presel_mll         = 'dl_mass>'+str(mllcut)
presel_OS          = 'isOS'
presel_mt2ll       = 'dl_mt2ll>='+str(mt2llcut)
presel_dPhi        = 'cos(met_phi-Jet_phi[0])<cos('+str(dphicut)+')&&cos(met_phi-Jet_phi[1])<cos('+str(dphicut)+')'
presel_zregion     = 'abs(91.2-dl_mass)<10'
presel_nLep        = '(nGoodMuons+nGoodElectrons)>=3'
presel_SF          = '((isMuMu==1&&nGoodMuons>=2)||(isEE==1&&nGoodElectrons>=2))'

luminosity = 2500./1000

#preselection = presel_njet+'&&'+presel_nbjet+'&&'+presel_OS+'&&'+presel_flavour+'&&'+presel_zregion#+'&&'+presel_mll+'&&'+presel_met+'&&'+presel_metsig+presel_dPhi+'&&'
preselection = presel_nLep+'&&'+presel_OS+'&&'+presel_SF+'&&'+presel_zregion+'&&'+presel_njet+'&&'+presel_nbjet

#backgrounds = [DY_HT_LO,TTJets,WJetsToLNu,singleTop,QCD_Mu5,TTZ,TTW,TZQ,TTH,diBoson]
backgrounds = [TTZ,TTH,TTW,TZQ,WZ,TTJets,DY_HT_LO,WJetsToLNu,ZZ]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds:
  s['chain'] = getChain(s,histname="")

mt2llbinning = "(15,0,300)"
mllbinning = "(50,0,150)"
metbinning = "(30,0,300)"
lepbinning = "(50,0,300)"

plots = {\
    'dl_mt2ll':{'title':'MT2ll (GeV)', 'name':'MT2ll', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
    'dl_mass':{'title':'M_{ll} (GeV)', 'name':'Mll', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
    'met_pt':{'title':'MET (GeV)', 'name':'MET', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
    'LepGood_pt[1]':{'title':'l1 p_{T} (GeV)', 'name':'l1pt', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
    'LepGood_pt[2]':{'title':'l2 p_{T} (GeV)', 'name':'l2pt', 'binning': lepbinning, 'histo':{'totalbkg':0.,}},
    }


#######################################################
#            Start filling in the histograms          #
#######################################################
print preselection

for s in backgrounds:
  #construct 1D histograms

  chain = s['chain']
  for plot in plots.keys():
    chain.Draw(plot+">>"+plot+s['name']+plots[plot]['binning'],"(weight*"+str(luminosity)+")*("+preselection+')')
    plots[plot]['histo'][s['name']] = ROOT.gDirectory.Get(plot+s['name'])
    
  #overflow
  for plot in plots.keys():  
    nbinsx        = plots[plot]['histo'][s['name']].GetNbinsX()
    lastbin       = plots[plot]['histo'][s['name']].GetBinContent(nbinsx)
    error         = plots[plot]['histo'][s['name']].GetBinError(nbinsx)
    overflowbin   = plots[plot]['histo'][s['name']].GetBinContent(nbinsx+1)
    overflowerror = plots[plot]['histo'][s['name']].GetBinError(nbinsx+1)
    plots[plot]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
    plots[plot]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
    plots[plot]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
    plots[plot]['histo'][s['name']].SetBinError(nbinsx+1,0.)
        #Remove bins with negative events
    for i in range(nbinsx):
      if plots[plot]['histo'][s['name']].GetBinContent(i+1) < 0: plots[plot]['histo'][s['name']].SetBinContent(i+1,0.)
        
processtime = datetime.now()
print "Time to process chains: ", processtime - start

for b in backgrounds:
  print b['name'], ": ", plots['dl_mass']['histo'][b['name']].Integral()


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
legendpos = [0.6,0.7,1.0,1.0]
scalepos = [0.8,0.95,1.0,1.0]

if makedraw1D:
  for plot in plots.keys():
    l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
    a.append(l)
    l.SetFillColor(0)
    l.SetShadowColor(ROOT.kWhite)
    l.SetBorderSize(1)
    l.SetTextSize(legendtextsize)

    bkg_stack = ROOT.THStack("bkgs","bkgs") 
    totalbackground = plots[plot]['histo'][backgrounds[0]['name']].Clone()
    for b in backgrounds:
      if b!= backgrounds[0]:totalbackground.Add(plots[plot]['histo'][b['name']])

    for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots[plot]["histo"][sort["name"]].Integral())):
      plots[plot]['histo'][b["name"]].SetMarkerSize(0)
      plots[plot]['histo'][b["name"]].SetFillColor(b["color"])
      plots[plot]['histo'][b["name"]].SetLineWidth(1)
      bkg_stack.Add(plots[plot]['histo'][b["name"]],"h")
      l.AddEntry(plots[plot]['histo'][b["name"]],b['texName'],"f")

    c1 = ROOT.TCanvas("c1","c1",800,800)

    #c1.SetLogy()
    c1.SetTopMargin(0)
    c1.SetRightMargin(0)

    bkg_stack.Draw()
    l.Draw("same")
    #c1.SetRangeUser(0.001,1000*bkg_stack.GetMaximum())
    bkg_stack.GetXaxis().SetTitle(plots[plot]['title'])
    bkg_stack.GetYaxis().SetTitle("Events (A.U.)")

    channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
    lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
    lumitag.AddText("lumi: "+str(luminosity)+' fb^{-1}')
    channeltag.SetFillColor(ROOT.kWhite)
    channeltag.SetShadowColor(ROOT.kWhite)
    channeltag.SetBorderSize(0)
    lumitag.SetFillColor(ROOT.kWhite)
    lumitag.SetShadowColor(ROOT.kWhite)
    lumitag.SetBorderSize(0)
    channeltag.Draw()
    lumitag.Draw()
    ROOT.gPad.RedrawAxis()
    path = plotDir+'/test/TTZstudy_copy/' 
    if not os.path.exists(path): os.makedirs(path)
    c1.Print(path+plot+".png")
    c1.Clear()

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start

