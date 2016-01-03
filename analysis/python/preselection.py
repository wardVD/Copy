cuts=[
 ("isOS", "isOS"),
 ("njet2", "(Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id))>=2"),
 ("nbtag1", "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)>=1"),
# ("nbtag0", "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)==0"),
 ("mll20", "dl_mass>20"),
 ("met80", "met_pt>80"),
 ("metSig5", "met_pt/sqrt(Sum$(Jet_pt*(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id)))>5"),
 ("dPhiJet0-dPhiJet1", "cos(met_phi-Jet_phi[0])<cos(0.25)&&cos(met_phi-Jet_phi[1])<cos(0.25)"),
  ]

triggerMuMu   = "HLT_mumuIso"
triggerEleEle = "HLT_ee_DZ"
triggerMuEle  = "HLT_mue"
preselMuMu = "isMuMu==1&&nGoodMuons==2&&nGoodElectrons==0"
preselEE   = "isEE==1&&nGoodMuons==0&&nGoodElectrons==2"
preselEMu  = "isEMu==1&&nGoodMuons==1&&nGoodElectrons==1"

filterCut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

from StopsDilepton.tools.objectSelection import mZ
def getZCut(mode, zMassRange=15):
  zstr = "abs(dl_mass - "+str(mZ)+")"
  if mode.lower()=="onz": return zstr+"<="+str(zMassRange)
  if mode.lower()=="offz": return zstr+">"+str(zMassRange)
  return "(1)"

def preselection(dataMC, channel = "all", zWindow = "offZ", zMassRange=15, triggers=True, returnName=False):
  '''Get the preselection ROOT string. All string arguments are matched with lower case. 
dataMC: 'data' or 'MC' (default)
zWindow: onZ/offZ(default)/allZ
zMassRange: 15 GeV around mZ=91.2
triggers: True(default)/False
returnName: True/False(default) -> whether to return a prefix corresponding to the selection'''
  assert dataMC.lower() in ['data','mc'], "dataMC = Data or MC, got %r."%dataMC
  assert channel.lower() in ['all', 'ee', 'mumu', 'emu'], "channel must be one of all,ee,mumu,emu. Got %r."%channel
  assert zWindow.lower() in ['offz', 'onz', 'allz'], "zWindow must be one of onZ, offZ, allZ. Got %r"%zWindow
#basic cuts
  name   = '-'.join(c[0] for c in cuts)
  presel = "&&".join(c[1] for c in cuts)
#Z window
  name = zWindow+'_'+name
  if zWindow.lower() in ['onz', 'offz']:
     presel+="&&"+getZCut(zWindow, zMassRange)
#triggers
  if triggers:
    pMuMu = preselMuMu + "&&" + triggerMuMu
    pEE   = preselEE  + "&&" + triggerEleEle 
    pEMu  = preselEMu + "&&" + triggerMuEle
  else:
    pMuMu = preselMuMu 
    pEE   = preselEE  
    pEMu  = preselEMu 
    
  name = channel+'_'+name
  if channel.lower()=="mumu":
    presel+="&&"+pMuMu
  if channel.lower()=="ee":
    presel+="&&"+pEE
  if channel.lower()=="emu":
    presel+="&&"+pEMu
  if channel.lower()=="all":
    presel+="&&("+pMuMu+'|'+pEE+'|'+pEMu+')'

  if dataMC.lower()=='data':
    presel+="&&"+filterCut
  if returnName: return name
  return presel 
