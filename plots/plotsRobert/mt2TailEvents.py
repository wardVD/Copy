import ROOT
ROOT.gROOT.LoadMacro("$CMSSW_BASE/src/StopsDilepton/tools/scripts/tdrstyle.C")
ROOT.setTDRStyle()

from math import *
import array, operator
from StopsDilepton.tools.localInfo import plotDir
from StopsDilepton.tools.helpers import getChain, getObjDict, getEList, getVarValue, deltaR
from StopsDilepton.tools.objectSelection import getGenPartsAll, getGoodLeptons, getLeptons, looseMuID, looseEleID, getJets, leptonVars, jetVars 
from StopsDilepton.tools.mt2Calculator import mt2Calculator
mt2Calc = mt2Calculator()
from StopsDilepton.tools.localInfo import *

reduceStat = 1
lumiScale = 10.
lepPdgs = [11,13,15]
muPdgs = [12,14,16]

#load all the samples
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_postProcessed import *
small=False
maxN=3 if small else -1
ttjets = TTJets_Lep
ttjets['name']="TTLep_1l2l"
ttjets['chain'] = getChain(ttjets,histname="", maxN=maxN)
prefix="mAODv2"
#others={'name':'ST/VV/TTX', 'chain':getChain([WJetsToLNu,DY,singleTop,TTX,diBoson], histname="")}

samples=[TTJets_Lep]

cuts=[
 ("lepVeto", "nGoodMuons+nGoodElectrons==2"),
 ("njet2", "(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=2"), 
 ("nbtag1", "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)>=1"), 
 ("mll20", "dl_mass>20"), 
 ("met80", "met_pt>80"), 
 ("metSig5", "met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>5"), 
 ("dPhiJet0-dPhiJet1", "cos(met_phi-Jet_phi[0])<cos(0.25)&&cos(met_phi-Jet_phi[1])<cos(0.25)"), 
 ("isOS","isOS==1"),
 ("SFZVeto","( (isMuMu==1||isEE==1)&&abs(dl_mass-90.2)>=15 || isEMu==1 )"), 
# ("mRelIso01", "LepGood_miniRelIso[l1_index]<0.1&&LepGood_miniRelIso[l2_index]<0.1")
  ]
preselection = "&&".join([c[1] for c in cuts])

#ttjets['chain'].Scan('Sum$(abs(genPartAll_pdgId)==11&&abs(genPartAll_motherId)==24):Sum$(abs(genPartAll_pdgId)==13&&abs(genPartAll_motherId)==24):Sum$(abs(genPartAll_pdgId)==15&&abs(genPartAll_motherId)==24)', 'isEMu==1&&dl_mt2ll>140&&'+preselection)
#ttjets['chain'].Scan('genPartAll_pdgId:genPartAll_motherId:genPartAll_pt:genPartAll_phi:genPartAll_eta:LepGood_pt:LepGood_eta:LepGood_phi', 'abs(genPartAll_pdgId)==13&&isMuMu==1&&dl_mt2ll>140&&'+preselection)

def descendTauDecay(tau_, genParts):
  daughters = [p for p in genParts[tau_['daughterIndex1']:tau_['daughterIndex2']+1] ]
  taus_ = filter(lambda p:abs(p['pdgId'])==15, daughters)
  assert len(taus_)<=1, "Found more than one tau in decay chain -> impossible." 
  if len(taus_)>0:
#    print "Found further tau -> descending"
    return descendTauDecay(taus_[0], genParts)

  lf= filter(lambda p:abs(p['pdgId']) in [11,13], daughters)
  assert len(lf)<=1, "Found more than one ele/mu in decay chain -> impossible." 
  if len(lf)==1: 
    return lf[0]['pdgId']
  else:
     return 0

def dRMatch(coll, dR=0.4):
  def match(l):
    for o in coll:
      if deltaR(l,o)<dR: return True
    return False
  return match


 
for s in samples:
#  for pk in plots.keys():
#    plots[pk]['histo'][s['name']] = ROOT.TH1F("met_"+s["name"], "met_"+s["name"], *(plots[pk]['binning']))

  chain = s["chain"]
  print "Looping over %s" % s["name"]
  eList = getEList(chain, preselection+"&&dl_mt2ll>140") 
  nEvents = eList.GetN()/reduceStat
  print "Found %i events in %s after preselection %s, looping over %i" % (eList.GetN(),s["name"],preselection,nEvents)
  ntot=0
  counterReco={}
  counterRecoGen={}
  counterRecoGen_muMatched={}
  counterRecoGen_eleMatched={}
  counterRecoGen_allMatched={}
  counterRecoGen_oneMuMatchedToB={}
  counterRecoGen_oneEleMatchedToB={}
  counterRecoGen_oneMuMatchedToTau={}
  counterRecoGen_oneEleMatchedToTau={}
  for mode in ["isMuMu", "isEE", "isEMu"]:
    counterReco[mode]=0
    counterRecoGen[mode]={}
    counterRecoGen_muMatched[mode]={}
    counterRecoGen_eleMatched[mode]={}
    counterRecoGen_allMatched[mode]={}
    counterRecoGen_oneMuMatchedToB[mode]={}
    counterRecoGen_oneEleMatchedToB[mode]={}
    counterRecoGen_oneMuMatchedToTau[mode]={}
    counterRecoGen_oneEleMatchedToTau[mode]={}
  for ev in range(nEvents):
    ntot+=1
    if ev%10000==0:print "At %i/%i"%(ev,nEvents)
    chain.GetEntry(eList.GetEntry(ev))
    mt2Calc.reset()
    weight = reduceStat*getVarValue(chain, "weight")*lumiScale if not s['isData'] else 1
    met = getVarValue(chain, "met_pt")
    metPhi = getVarValue(chain, "met_phi")
    jets = filter(lambda j:j['pt']>30 and abs(j['eta'])<2.4 and j['id'], getJets(chain))

    leptons = filter(lambda l: looseMuID(l) or looseEleID(l), getLeptons(chain, collVars=leptonVars+['mcMatchId','mcMatchAny','mcMatchTau','mcPt']))
#LepGood_mcMatchId Match to source from hard scatter (pdgId of heaviest particle in chain, 25 for H, 6 for t, 23/24 for W/Z), zero if non-prompt or fake for Leptons after the preselection 
#LepGood_mcMatchAny  Match to any final state leptons: 0 if unmatched, 1 if light flavour (including prompt), 4 if charm, 5 if bottom for Leptons after the preselection
#LepGood_mcMatchTau True if the leptons comes from a tau for Leptons after the preselection

#    for l in leptons:
#      if (l['mcMatchAny']==0 and (not (l['mcMatchId']==0))) or ( (not l['mcMatchAny']==0) and (l['mcMatchId']==0)):
#        print "Match?",l

#RECO
    mu      = filter(lambda l: abs(l['pdgId'])==13, leptons)
    ele     = filter(lambda l: abs(l['pdgId'])==11, leptons)

#RECO mathes
    muMatched   = filter(lambda l: abs(l['mcMatchAny'])==1, mu)
    eleMatched  = filter(lambda l: abs(l['mcMatchAny'])==1, ele)
#GEN    
    genParts = getGenPartsAll(chain)
    genLeptons          =   filter(lambda p: abs(p['motherId']) in [24] and abs(p['pdgId']) in lepPdgs, genParts)
    genLeptonsFromTau   =   filter(lambda p: abs(p['motherId']) in [15] and abs(p['pdgId']) in lepPdgs, genParts)
    genNeutrinos        =   filter(lambda p: abs(p['motherId']) ==24 and abs(p['pdgId']) in muPdgs, genParts)
    genNeutrinosFromTau =   filter(lambda p: abs(p['motherId']) ==15 and abs(p['pdgId']) in muPdgs, genParts)
    genEle =       filter(lambda p: abs(p['motherId']) in [24] and abs(p['pdgId'])==11 , genParts)
    genMu=         filter(lambda p: abs(p['motherId']) in [24] and abs(p['pdgId'])==13 , genParts)
    genEleFromTau= filter(lambda p: abs(p['motherId']) in [15] and abs(p['pdgId'])==11 , genParts)
    genMuFromTau=  filter(lambda p: abs(p['motherId']) in [15] and abs(p['pdgId'])==13 , genParts)
    genTau=        filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==15 , genParts)
    genTauToE=     filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==15 and abs(descendTauDecay(p, genParts))==11, genParts)
    genTauToMu=    filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==15 and abs(descendTauDecay(p, genParts))==13, genParts)
    genTauToHad=   filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==15 and abs(descendTauDecay(p, genParts))==0, genParts)
    genNuE =         filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==12 , genParts)
    genNuMu=         filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==14 , genParts)
    genNuTau=        filter(lambda p: abs(p['motherId'])==24 and abs(p['pdgId'])==16 , genParts)
    genNuEFromTau =  filter(lambda p: abs(p['motherId'])==15 and abs(p['pdgId'])==12 , genParts)
    genNuMuFromTau=  filter(lambda p: abs(p['motherId'])==15 and abs(p['pdgId'])==14 , genParts)
    genNuTauFromTau= filter(lambda p: abs(p['motherId'])==15 and abs(p['pdgId'])==16 , genParts)
    genB   =         filter(lambda p: abs(p['motherId'])==6 and abs(p['pdgId'])==5 , genParts)

#Matched    
#    muMatchedToB     = filter(lambda l: abs(l['mcMatchAny'])==5 and l['mcMatchId']==0, mu)
#    eleMatchedToB    = filter(lambda l: abs(l['mcMatchAny'])==5 and l['mcMatchId']==0, ele)
#    muMatchedToTau   = filter(lambda l: l['mcMatchTau']>0, mu)
#    eleMatchedToTau  = filter(lambda l: l['mcMatchTau']>0, ele)
    muMatchedToB     = filter(lambda l: dRMatch(genB, dR=0.4)(l), mu)
    eleMatchedToB    = filter(lambda l: dRMatch(genB, dR=0.4)(l), ele)
    muMatchedToTau   = filter(lambda l: dRMatch(genMuFromTau, dR=0.4)(l), mu)
    eleMatchedToTau  = filter(lambda l: dRMatch(genEleFromTau, dR=0.4)(l), ele)
 
     
#    for gt in genTau:
#      print "Descending tau..."
#      res = descendTauDecay(gt, genParts)
#      if res:
#        print "Found lepton %i"%res['pdgId']
#      else:
#        print "Hadronic decay"
#      print "Check genNuE %i genNuMu %i genNuTau %i"%(len(genNuE), len(genNuMu), len(genNuTau))
#      print "  genTau decay:",[p['pdgId'] for p in genParts[gt['daughterIndex1']:gt['daughterIndex2']+1] ]
    for v in ['isMuMu','isEE','isEMu']:
      exec(v+'=getVarValue(chain, "'+v+'")')
    for mode in ["isMuMu", "isEE", "isEMu"]:
      if eval(mode):
        counterReco[mode]+=1 

        gMode="other"   
#        print len(genEle),len(genMu),len(genTau),len(genLeptons)
        if    len(genMu)==2 and len(genLeptons)==2: gMode="2Mu"
        elif  len(genMu)==1 and len(genLeptons)==1: gMode="1Mu"
        elif  len(genEle)==2 and len(genLeptons)==2: gMode="2Ele"
        elif  len(genEle)==1 and len(genLeptons)==1: gMode="1Ele"
        elif  len(genMu)==1 and len(genEle)==1 and len(genLeptons)==2: gMode="Ele+Mu"
#        elif  len(genMu)==1 and len(genTau)==1 and len(genLeptons)==2: gMode="Mu+Tau"
#        elif  len(genEle)==1 and len(genTau)==1 and len(genLeptons)==2: gMode="Ele+Tau"
        elif  len(genMu)==1 and len(genTauToE)==1 and len(genLeptons)==2: gMode="Mu+TauToE"
        elif  len(genMu)==1 and len(genTauToMu)==1 and len(genLeptons)==2: gMode="Mu+TauToMu"
        elif  len(genMu)==1 and len(genTauToHad)==1 and len(genLeptons)==2: gMode="Mu+TauToHad"
        elif  len(genEle)==1 and len(genTauToE)==1 and len(genLeptons)==2: gMode="Ele+TauToE"
        elif  len(genEle)==1 and len(genTauToMu)==1 and len(genLeptons)==2: gMode="Ele+TauToMu"
        elif  len(genEle)==1 and len(genTauToHad)==1 and len(genLeptons)==2: gMode="Ele+TauToHad"

        elif  len(genTau)==2 and len(genLeptons)==2: gMode="2Tau"
        
        if gMode=='other':
          print len(genLeptons), len(genNeutrinos), len(genNuE), len(genNuMu), len(genNuTau) 
        if not counterRecoGen[mode].has_key(gMode):
          counterRecoGen[mode][gMode]=0 
          counterRecoGen_muMatched[mode][gMode]=0
          counterRecoGen_eleMatched[mode][gMode]=0
          counterRecoGen_allMatched[mode][gMode]=0
          counterRecoGen_oneMuMatchedToB[mode][gMode]=0
          counterRecoGen_oneEleMatchedToB[mode][gMode]=0
          counterRecoGen_oneMuMatchedToTau[mode][gMode]=0
          counterRecoGen_oneEleMatchedToTau[mode][gMode]=0
        counterRecoGen[mode][gMode]+=1
        if len(mu)==len(muMatched):counterRecoGen_muMatched[mode][gMode]+=1
        if len(ele)==len(eleMatched):counterRecoGen_eleMatched[mode][gMode]+=1
        if len(mu)==len(muMatched) and len(ele)==len(eleMatched):counterRecoGen_allMatched[mode][gMode]+=1
        if len(muMatchedToB)>0:  counterRecoGen_oneMuMatchedToB[mode][gMode]+=1
        if len(eleMatchedToB)>0:  counterRecoGen_oneEleMatchedToB[mode][gMode]+=1
        if len(muMatchedToTau)>0:   counterRecoGen_oneMuMatchedToTau[mode][gMode]+=1
        if len(eleMatchedToTau)>0:   counterRecoGen_oneEleMatchedToTau[mode][gMode]+=1


        print "mode %s genLeps %i genNus %i (%i %i %i) gen/recoLeps/matched Ele:%i/%i/%i Mu:%i/%i/%i Tau:%i"%(mode, len(genLeptons), len(genNeutrinos), len(genNuE), len(genNuMu), len(genNuTau), len(genEle), len(ele), len(eleMatched), len(genMu), len(mu),len(muMatched), len(genTau))
        if len(eleMatchedToB+muMatchedToB)>0:print "  fromB (tot.: %i) Ele:%i Mu:%i"%(len(eleMatchedToB+muMatchedToB), len(eleMatchedToB), len(muMatchedToB))#, eleMatchedToB, muMatchedToB
        if len(eleMatchedToTau+muMatchedToTau)>0:print "  fromTau (tot.: %i) Ele:%i Mu:%i"%(len(eleMatchedToTau+muMatchedToTau), len(eleMatchedToTau), len(muMatchedToTau))#,eleMatchedToTau,muMatchedToTau

  print
  for mode in ["isMuMu", "isEE", "isEMu"]:

    print "Reconstructed as %s (%i)"%(mode, counterReco[mode])
    sortedRes = sorted(counterRecoGen[mode].items(), key=operator.itemgetter(1)) 
    sortedRes.reverse()
    for gMode,n in sortedRes: 
      print "  Generated as %s: %i " %(gMode, n)
      print "    all eleMatched: %i"       %counterRecoGen_eleMatched[mode][gMode]
      print "    all muMatched: %i"        %counterRecoGen_muMatched[mode][gMode]
      print "    all lep matched: %i"      %counterRecoGen_allMatched[mode][gMode]
      print "    >=1 match Ele/B: %i"      %counterRecoGen_oneEleMatchedToB[mode][gMode]
      print "    >=1 match Mu/B: %i"       %counterRecoGen_oneMuMatchedToB[mode][gMode]
      print "    >=1 match Ele/Tau: %i"    %counterRecoGen_oneEleMatchedToTau[mode][gMode]
      print "    >=1 match Mu/Tau: %i"     %counterRecoGen_oneMuMatchedToTau[mode][gMode]
    print 
    print 
