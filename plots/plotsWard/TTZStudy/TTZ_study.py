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

#btagcoeff          = 0.89
btagcoeff          = 0.605
njetscut           = [">=4",'4m']
nbjetscut          = [">=2",'2m']
flavour            = "MuMu"


presel_njet        = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)'+njetscut[0]
presel_nbjet       = 'Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>'+str(btagcoeff)+')'+nbjetscut[0]
presel_nlep        = '(nGoodElectrons+nGoodMuons)>=2'

if flavour=="MuMu": 
  presel_flavour     = 'nGoodMuons>=2&&HLT_mumuIso'
  data = [DoubleMuon_Run2015D]
elif flavour=="EE": 
  presel_flavour     = 'nGoodElectrons>=2&&HLT_ee_DZ'
  data = [DoubleEG_Run2015D]

luminosity = data[0]["lumi"]

datacut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

preselection = presel_njet+'&&'+presel_nbjet+'&&'+presel_nlep+'&&'+presel_flavour

#backgrounds = [DY_HT_LO,TTJets,WJetsToLNu,singleTop,QCD_Mu5,TTZ,TTW,TZQ,TTH,diBoson]
backgrounds = [TTZ,TZQ,TTH,TTW,DY_HT_LO,TTJets,ZZ]

#######################################################
#            get the TChains for each sample          #
#######################################################
for s in backgrounds+data:
  s['chain'] = getChain(s,histname="")

mt2llbinning = [15,0,300]
mllbinning = [50,0,150]
metbinning = [30,0,300]
zptbinning = [50,0,300]

plots = {\
  '2l':{\
    #'dl_mt2ll':{'title':'MT2ll (GeV)', 'name':'MT2ll_2l', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
    'dl_mass_onZ':{'title':'M_{ll} (GeV)', 'name':'Mll_2l_onZ', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
    'dl_mass_offZ':{'title':'M_{ll} (GeV)', 'name':'Mll_2l_offZ', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
    #'met_pt':{'title':'MET (GeV)', 'name':'MET_2l', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
    'Z_pt_onZ':{'title':'p_{T} Z (GeV)', 'name':'ZpT_2l_onZ', 'binning': zptbinning, 'histo':{'totalbkg':0.,}},
    'Z_pt_offZ':{'title':'p_{T} Z (GeV)', 'name':'ZpT_2l_offZ', 'binning': zptbinning, 'histo':{'totalbkg':0.,}},
    },
  '3l':{\
    #'dl_mt2ll':{'title':'MT2ll (GeV)', 'name':'MT2ll_3l', 'binning': mt2llbinning, 'histo':{'totalbkg':0.,}},
    'dl_mass_onZ':{'title':'M_{ll} (GeV)', 'name':'Mll_3l_onZ', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
    'dl_mass_offZ':{'title':'M_{ll} (GeV)', 'name':'Mll_3l_offZ', 'binning': mllbinning, 'histo':{'totalbkg':0.,}},
    #'met_pt':{'title':'MET (GeV)', 'name':'MET_3l', 'binning': metbinning, 'histo':{'totalbkg':0.,}},
    'Z_pt_onZ':{'title':'p_{T} Z (GeV)', 'name':'ZpT_3l_onZ', 'binning': zptbinning, 'histo':{'totalbkg':0.,}},
    'Z_pt_offZ':{'title':'p_{T} Z (GeV)', 'name':'ZpT_3l_offZ', 'binning': zptbinning, 'histo':{'totalbkg':0.,}},
    },
  }


#######################################################
#            Start filling in the histograms          #
#######################################################
for s in backgrounds+data:
  #construct 1D histograms
  for lepton in plots.keys():
    for plot in plots[lepton].keys():
        plots[lepton][plot]['histo'][s["name"]] = ROOT.TH1D(plots[lepton][plot]['name']+"_"+s["name"], plots[lepton][plot]['name']+"_"+s["name"], *plots[lepton][plot]['binning'])
        plots[lepton][plot]['histo'][s["name"]].Sumw2()

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
    
    electrons = getGoodElectrons(chain)
    muons = getGoodMuons(chain)
    leptons = getGoodLeptons(chain)

    
    """
    dilep = {\
      'dl_12' : {'SF': False, 'SS': False, 'vector': l1+l2, 'lepton1': leptons[0], 'lepton2': leptons[1]},
      'dl_13' : {'SF': False, 'SS': False, 'vector': l1+l3, 'lepton1': leptons[0], 'lepton2': leptons[2]},
      'dl_23' : {'SF': False, 'SS': False, 'vector': l2+l3, 'lepton1': leptons[1], 'lepton2': leptons[2]},
      }

    for key in dilep:

      dilep[key]['SS'] = True if (dilep[key]['lepton1']['pdgId']*dilep[key]['lepton2']['pdgId'] > 0) else False
      dilep[key]['SF'] = True if (abs(dilep[key]['lepton1']['pdgId']) == abs(dilep[key]['lepton2']['pdgId'])) else False

    if dilep['dl_12']['SS'] and dilep['dl_12']['SS'] and dilep['dl_12']['SS']: #all Same Sign, no Z-boson
      continue
    if dilep['dl_12']['SF'] and dilep['dl_12']['SF'] and dilep['dl_12']['SF']: #all Same Flavour: eee, mumumu
      dl1,dl2 = [dl for dl in dilep if dilep[dl]['SS']==False ][0],[dl for dl in dilep if dilep[dl]['SS']==False ][1]
      Z = dilep[dl1]['vector'] if (abs(dilep[dl1]['vector'].Pt()-91.2) < abs(dilep[dl2]['vector'].Pt()-91.2)) else dilep[dl2]['vector']
    else: #eemu or mumue
      dl = [dl for dl in dilep if dilep[dl]['SF']==True ][0]
      if not dilep[dl]['SS']:
        Z = dilep[dl]['vector']
      else: 
        continue
    print Z.Pt()
    """

    
    mZ = 9999999.
    Z_pt = 9999999.
    for Lep1 in range(len(leptons)-1):
      l1 = ROOT.TLorentzVector()
      l1.SetPtEtaPhiM(leptons[Lep1]['pt'], leptons[Lep1]['eta'], leptons[Lep1]['phi'], 0)
      for Lep2 in range(Lep1+1,len(leptons)):
        if (leptons[Lep1]['pdgId']*leptons[Lep2]['pdgId'] < 0):
          if (abs(leptons[Lep1]['pdgId']) == abs(leptons[Lep2]['pdgId'])):
            l2 = ROOT.TLorentzVector()
            l2.SetPtEtaPhiM(leptons[Lep2]['pt'], leptons[Lep2]['eta'], leptons[Lep2]['phi'], 0)
            diLep = l1+l2
            if (abs(diLep.M()-91.2) < abs(mZ-91.2)):
              mZ = diLep.M()
              Z_pt = diLep.Pt()

    if abs(mZ - 91.2) < 15: 
      if len(leptons)==2:
        plots['2l']['dl_mass_onZ']['histo'][s["name"]].Fill(mZ,weight)
        plots['2l']['Z_pt_onZ']['histo'][s["name"]].Fill(Z_pt,weight)
      elif len(leptons)==3:
        plots['3l']['dl_mass_onZ']['histo'][s["name"]].Fill(mZ,weight)
        plots['3l']['Z_pt_onZ']['histo'][s["name"]].Fill(Z_pt,weight)
    else:
      if len(leptons)==2:
        plots['2l']['dl_mass_offZ']['histo'][s["name"]].Fill(mZ,weight)
        plots['2l']['Z_pt_offZ']['histo'][s["name"]].Fill(Z_pt,weight)
      elif len(leptons)==3:
        plots['3l']['dl_mass_offZ']['histo'][s["name"]].Fill(mZ,weight)
        plots['3l']['Z_pt_offZ']['histo'][s["name"]].Fill(Z_pt,weight)
      

  #overflow
  for lepton in plots.keys():
    for plot in plots[lepton].keys():  
      nbinsx        = plots[lepton][plot]['histo'][s['name']].GetNbinsX()
      lastbin       = plots[lepton][plot]['histo'][s['name']].GetBinContent(nbinsx)
      error         = plots[lepton][plot]['histo'][s['name']].GetBinError(nbinsx)
      overflowbin   = plots[lepton][plot]['histo'][s['name']].GetBinContent(nbinsx+1)
      overflowerror = plots[lepton][plot]['histo'][s['name']].GetBinError(nbinsx+1)
      plots[lepton][plot]['histo'][s['name']].SetBinContent(nbinsx,lastbin+overflowbin)
      plots[lepton][plot]['histo'][s['name']].SetBinError(nbinsx,sqrt(error**2+overflowerror**2))
      plots[lepton][plot]['histo'][s['name']].SetBinContent(nbinsx+1,0.)
      plots[lepton][plot]['histo'][s['name']].SetBinError(nbinsx+1,0.)
        #Remove bins with negative events
      for i in range(nbinsx):
        if plots[lepton][plot]['histo'][s['name']].GetBinContent(i+1) < 0: plots[lepton][plot]['histo'][s['name']].SetBinContent(i+1,0.)
        
processtime = datetime.now()
print "Time to process chains: ", processtime - start


for lepton in plots.keys():
  for plot in plots[lepton].keys():
    totalbkg = 0
    for b in backgrounds:
      totalbkg += plots[lepton][plot]['histo'][b["name"]].Integral()
    dataint = plots[lepton][plot]['histo'][data[0]["name"]].Integral()

    for b in backgrounds:
      if noscaling:
        plots[lepton][plot]['SF'] = 1.
      else:
        plots[lepton][plot]['histo'][b["name"]].Scale(dataint/totalbkg)
        plots[lepton][plot]['SF'] = dataint/totalbkg

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
legendpos = [0.6,0.6,1.0,0.95]
scalepos = [0.8,0.95,1.0,0.95]

if makedraw1D:
  for lepton in plots.keys():
    for plot in plots[lepton].keys():
      l=ROOT.TLegend(legendpos[0],legendpos[1],legendpos[2],legendpos[3])
      a.append(l)
      l.SetFillColor(0)
      l.SetShadowColor(ROOT.kWhite)
      l.SetBorderSize(1)
      l.SetTextSize(legendtextsize)

      bkg_stack = ROOT.THStack("bkgs","bkgs") 
      totalbackground = plots[lepton][plot]['histo'][backgrounds[0]['name']].Clone()
      for b in backgrounds:
        if b!= backgrounds[0]:totalbackground.Add(plots[lepton][plot]['histo'][b['name']])

      for j,b in enumerate(sorted(backgrounds,key=lambda sort:plots[lepton][plot]["histo"][sort["name"]].Integral())):
        plots[lepton][plot]['histo'][b["name"]].SetMarkerSize(0)
        plots[lepton][plot]['histo'][b["name"]].SetFillColor(b["color"])
        plots[lepton][plot]['histo'][b["name"]].SetLineWidth(1)
        bkg_stack.Add(plots[lepton][plot]['histo'][b["name"]],"h")
        l.AddEntry(plots[lepton][plot]['histo'][b["name"]],b['texName'],"f")

      c1 = ROOT.TCanvas("c1","c1",800,800)
      pad1 = ROOT.TPad("","",histopad[0],histopad[1],histopad[2],histopad[3])
      a.append(pad1)
      pad1.SetBottomMargin(0)
      pad1.SetTopMargin(0)
      pad1.SetRightMargin(0.05)
      pad1.Draw()
      pad1.cd()
      pad1.SetLogy()
      plots[lepton][plot]['histo'][data[0]["name"]].Draw("pe1same")
      bkg_stack.Draw("same")
      plots[lepton][plot]['histo'][data[0]["name"]].Draw("pe1same")
      bkg_stack.GetXaxis().SetLabelSize(0.)
      l.Draw()
      ROOT.gPad.RedrawAxis()

      plots[lepton][plot]['histo'][data[0]["name"]].GetXaxis().SetTitle(plots[lepton][plot]['title'])
      plots[lepton][plot]['histo'][data[0]["name"]].GetYaxis().SetTitle("Events (A.U.)")
      plots[lepton][plot]['histo'][data[0]["name"]].GetYaxis().SetRangeUser(0.005,1000000)
      l.AddEntry(plots[lepton][plot]['histo'][data[0]["name"]],data[0]['texName'])

      channeltag = ROOT.TPaveText(channeltagpos[0],channeltagpos[1],channeltagpos[2],channeltagpos[3],"NDC")
      lumitag = ROOT.TPaveText(lumitagpos[0],lumitagpos[1],lumitagpos[2],lumitagpos[3],"NDC")
      scaletag = ROOT.TPaveText(scalepos[0],scalepos[1],scalepos[2],scalepos[3],"NDC")
      channeltag.AddText(flavour)
      lumitag.AddText("lumi: "+str(data[0]['lumi'])+' pb^{-1}')
      scaletag.AddText("Scale Factor: " +str(round(plots[lepton][plot]['SF'],2)))
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
      pad2.SetRightMargin(0.05)
      pad2.Draw()
      pad2.cd()
      ratio = plots[lepton][plot]['histo'][data[0]["name"]].Clone()
      a.append(ratio)
      ratio.Divide(totalbackground)
      ratio.SetMarkerStyle(20)
      ratio.GetYaxis().SetTitle("Data/Bkg.")
      #ratio.GetYaxis().SetNdivisions(502)
      ratio.GetXaxis().SetTitle(plots[lepton][plot]['title'])
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
      path = plotDir+'/test/TTZstudy/'+lepton+'_'+flavour+'_njet_'+njetscut[1]+'_nbjet_'+nbjetscut[1]+'/'
      if not os.path.exists(path): os.makedirs(path)
      c1.Print(path+plot+".png")
      del ratio
      del pad1
      del pad2
      c1.Clear()
      

makeplotstime = datetime.now()

print '\n','\n', "Total time processing: ", makeplotstime-start

