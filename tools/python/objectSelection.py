from StopsDilepton.tools.helpers import getVarValue, getObjDict
from math import *

mZ=91.2

jetVars = ['eta','pt','phi','btagCSV', 'id']

def getJets(c, jetVars=jetVars):
  return [getObjDict(c, 'Jet_', jetVars, i) for i in range(int(getVarValue(c, 'nJet')))]

def jetId(j, ptCut=30, absEtaCut=2.4, ptVar='pt'):
 return j[ptVar]>ptCut and abs(j['eta'])<absEtaCut and j['id']

def getGoodJets(c, ptCut=30, absEtaCut=2.4, jetVars=jetVars):
  return filter(lambda j:jetId(j, ptCut=ptCut, absEtaCut=absEtaCut), getJets(c, jetVars))

def isBJet(j):
  return j['btagCSV']>0.890

def getGoodBJets(c):
  return filter(lambda j:isBJet(j), getGoodJets(c))

def getGenLeps(c):
  return [getObjDict(c, 'genLep_', ['eta','pt','phi','charge', 'pdgId', 'sourceId'], i) for i in range(int(getVarValue(c, 'ngenLep')))]

def getGenParts(c):
  return [getObjDict(c, 'GenPart_', ['eta','pt','phi','charge', 'pdgId', 'motherId', 'grandmotherId'], i) for i in range(int(getVarValue(c, 'nGenPart')))]

def getGenPartsAll(c):
  return [getObjDict(c, 'genPartAll_', ['eta','pt','phi','charge', 'status', 'pdgId', 'motherId', 'grandmotherId','daughterIndex1','daughterIndex2'], i) for i in range(int(getVarValue(c, 'ngenPartAll')))]

Muon_mediumMuonId = 1
Muon_miniRelIso = 0.2
Muon_sip3d = 4.0
Muon_dxy = 0.05
Muon_dz = 0.1

def looseMuID(l, ptCut=20, absEtaCut=2.4):
  return \
    l["pt"]>=ptCut\
    and abs(l["pdgId"])==13\
    and abs(l["eta"])<absEtaCut\
    and l["mediumMuonId"]==Muon_mediumMuonId \
    and l["miniRelIso"]<Muon_miniRelIso \
    and l["sip3d"]<Muon_sip3d\
    and abs(l["dxy"])<Muon_dxy\
    and abs(l["dz"])<Muon_dz\

def looseMuIDString(ptCut=20, absEtaCut=2.4):
  string = []
  LepString = "LepGood_"
  string.append(LepString+"pt>="+str(ptCut))
  string.append("abs("+LepString+"pdgId)=="+str(Muon_pdgId))
  string.append("abs("+LepString+"eta)<"+str(absEtaCut))
  string.append(LepString+"mediumMuonId=="+str(Muon_mediumMuonId))
  string.append(LepString+"miniRelIso<"+str(Muon_miniRelIso))
  string.append(LepString+"sip3d<"+str(Muon_sip3d))
  string.append("abs("+LepString+"dxy)<"+str(Muon_dxy))
  string.append("abs("+LepString+"dz)<"+str(Muon_dz))
  string = 'Sum$('+'&&'.join(string)+')'
  return string

def cmgMVAEleID(l,mva_cuts):
  aeta = abs(l["eta"])
  for abs_e, mva in mva_cuts.iteritems():
    if aeta>=abs_e[0] and aeta<abs_e[1] and l["mvaIdSpring15"] >mva: return True
  return False

def cmgMVAEleIDString(mva_cuts):
  aeta = "abs(LepGood_eta)"
  string = []
  for abs_e, mva in mva_cuts.iteritems():
    string.append("("+aeta+">="+str(abs_e[0])+"&&"+aeta+"<"+str(abs_e[1])+"&&LepGood_mvaIdSpring15>"+str(mva)+")")
  string = "("+'||'.join(string)+')'
  return string
  
ele_MVAID_cuts_vloose = {(0,0.8):-0.16 , (0.8, 1.479):-0.65, (1.57, 999): -0.74}
#ele_MVAID_cuts_loose = {(0,0.8):0.35 , (0.8, 1.479):0.20, (1.57, 999): -0.52}
ele_MVAID_cuts_tight = {(0,0.8):0.87 , (0.8, 1.479):0.60, (1.57, 999):  0.17}

Ele_miniRelIso = 0.2
Ele_lostHits = 0
Ele_sip3d = 4.0
Ele_dxy = 0.05
Ele_dz = 0.1

def looseEleID(l, ptCut=20, absEtaCut=2.4):
  return \
    l["pt"]>=ptCut\
    and abs(l["eta"])<absEtaCut\
    and abs(l["pdgId"])==11\
    and cmgMVAEleID(l, ele_MVAID_cuts_tight)\
    and l["miniRelIso"]<Ele_miniRelIso\
    and l["convVeto"]\
    and l["lostHits"]==Ele_lostHits\
    and l["sip3d"] < Ele_sip3d\
    and abs(l["dxy"]) < Ele_dxy\
    and abs(l["dz"]) < Ele_dz\

def looseEleIDString(ptCut=20, absEtaCut=2.4):
  string = []
  LepString = "LepGood_"
  string.append(LepString+"pt>="+str(ptCut))
  string.append("abs("+LepString+"eta)<"+str(absEtaCut))
  string.append("abs("+LepString+"pdgId)=="+str(Ele_pdgId))
  string.append(cmgMVAEleIDString(ele_MVAID_cuts_tight))
  string.append(LepString+"miniRelIso<"+str(Ele_miniRelIso))
  string.append(LepString+"convVeto")
  string.append(LepString+"lostHits=="+str(Ele_lostHits))
  string.append(LepString+"sip3d<"+str(Ele_sip3d))
  string.append("abs("+LepString+"dxy)<"+str(Ele_dxy))
  string.append("abs("+LepString+"dz)<"+str(Ele_dz))
  string = 'Sum$('+'&&'.join(string)+')'
  return string

#leptonVars=['eta','pt','phi','mass','charge', 'dxy', 'dz', 'relIso03','tightId', 'pdgId', 'mediumMuonId', 'miniRelIso', 'sip3d', 'mvaIdSpring15', 'convVeto', 'lostHits']
leptonVars=['eta','pt','phi','dxy', 'dz','tightId', 'pdgId', 'mediumMuonId', 'miniRelIso', 'sip3d', 'mvaIdSpring15', 'convVeto', 'lostHits']

def getLeptons(c, collVars=leptonVars):
  return [getObjDict(c, 'LepGood_', collVars, i) for i in range(int(getVarValue(c, 'nLepGood')))]
def getMuons(c, collVars=leptonVars):
  return [getObjDict(c, 'LepGood_', collVars, i) for i in range(int(getVarValue(c, 'nLepGood'))) if abs(getVarValue(c,"LepGood_pdgId",i))==13]
def getElectrons(c, collVars=leptonVars):
  return [getObjDict(c, 'LepGood_', collVars, i) for i in range(int(getVarValue(c, 'nLepGood'))) if abs(getVarValue(c,"LepGood_pdgId",i))==11]
def getGoodMuons(c, collVars=leptonVars):
  return [l for l in getMuons(c, collVars) if looseMuID(l)]
def getGoodElectrons(c, collVars=leptonVars):
  return [l for l in getElectrons(c, collVars) if looseEleID(l)]
def getGoodLeptons(c, ptCut=20, collVars=leptonVars):
  return [l for l in getLeptons(c, collVars) if (abs(l["pdgId"])==11 and looseEleID(l, ptCut)) or (abs(l["pdgId"])==13 and looseMuID(l, ptCut))]
def m_ll(l1,l2):
  return sqrt(2.*l1['pt']*l2['pt']*(cosh(l1['eta']-l2['eta']) - cos(l1['phi']-l2['phi'])))
def pt_ll(l1,l2):
  return sqrt((l1['pt']*cos(l1['phi']) + l2['pt']*cos(l2['phi']))**2 + (l1['pt']*sin(l1['phi']) + l2['pt']*sin(l2['phi']))**2)


tauVars=['eta','pt','phi','pdgId','charge', 'dxy', 'dz', 'idDecayModeNewDMs', 'idCI3hit', 'idAntiMu','idAntiE','mcMatchId']

def getTaus(c, collVars=tauVars):
  return [getObjDict(c, 'TauGood_', collVars, i) for i in range(int(getVarValue(c, 'nTauGood')))]
def looseTauID(l, ptCut=20, absEtaCut=2.4):
  return \
    l["pt"]>=ptCut\
    and abs(l["eta"])<absEtaCut\
    and l["idDecayModeNewDMs"]>=1\
    and l["idCI3hit"]>=1\
    and l["idAntiMu"]>=1\
    and l["idAntiE"]>=1\

def getGoodTaus(c, collVars=tauVars):
  return [l for l in getTaus(c,collVars=collVars) if looseTauID(l)]
