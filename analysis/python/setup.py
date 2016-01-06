import copy
#Numerical constants
zMassRange=15

#define samples
from StopsDilepton.samples.cmgTuples_Data25ns_mAODv2_postProcessed import *
from StopsDilepton.samples.cmgTuples_Spring15_mAODv2_25ns_1l_postProcessed import *
DYSample      = DY #NLO M10t050 + M50
#DYSample      = DY_HT_LO #LO, HT binned including a low HT bin starting from zero from the inclusive sample
TTJetsSample  = TTJets #NLO
#TTJetsSample  = TTJets_Lep #LO, very large dilep + single lep samples
TTZSample     = TTZ 
QCDSample     = QCD_HT #FIXME: Need MuMu, EE, EMu samples here

from Systematics import jmeVariations
def getCuts(selectionModifier=None):
  if selectionModifier: assert selectionModifier in jmeVariations, "Don't know about systematic variation %r preselection(), take one of %s"%(selectionModifier, ",".join(jmeVariations))
  sysStr="" if not selectionModifier else "_"+selectionModifier
  nbstr = "nBTags" if not selectionModifier else "nbJets" #Correct stupid naming convention I already fixed in the postprocessing...
  return [
 ("isOS", "isOS"),
 ("njet2", "nGoodJets"+sysStr+">=2"),
 ("nbtag1", nbstr+sysStr+">=1"),
# ("nbtag0", "Sum$(Jet_pt>30&&abs(Jet_eta)<2.4&&Jet_id&&Jet_btagCSV>0.890)==0"),
 ("mll20", "dl_mass>20"),
 ("met80", "met_pt"+sysStr+">80"),
 ("metSig5", "met_pt"+sysStr+"/sqrt(ht"+sysStr+")>5"),
 ("dPhiJet0-dPhiJet1", "cos(met_phi"+sysStr+"-Jet_phi[0])<cos(0.25)&&cos(met_phi"+sysStr+"-Jet_phi[1])<cos(0.25)"),
  ]

from StopsDilepton.analysis.setupHelpers import getZCut, loadChain
class setup:
  def __init__(self):
    self.channel='all'
    self.zWindow='offZ'
    self.zMassRange=zMassRange
    self.useTriggers=True
    self.lumi         =  10000 #10/fb
    self.sys          = {'weight':'weightPU', 'reweight':None, 'selectionModifier':None}
    self.prefix = '-'.join(c[0] for c in getCuts())
    self.prefix = self.zWindow+'_'+self.prefix
    self.prefix = self.channel+'_'+self.prefix

    self.DYSample     = DYSample
    self.TTJetsSample = TTJetsSample
    self.TTZSample    = TTZSample
    self.QCDSample    = QCDSample
    for s in [self.DYSample, self.TTJetsSample, self.TTZSample, self.QCDSample]:
      loadChain(s)

  #Clone the setup and optinally modify the systematic variation
  def sysClone(self, sys=None):
    '''Clone setup and change systematic if provided'''
    res     = copy.copy(self)
    res.sys = copy.deepcopy(self.sys)
#    assert sys==None or all([k in sys.keys() for k in self.sys.keys()]), "Argument sys has too few keys: %r. Should look like %r."%(sys, self.sys) #Assure that all default sys keys are provided
    if sys:
      for k in sys.keys():
        res.sys[k]=sys[k] if sys[k] else res.sys[k]
    return res

  def preselection(self, dataMC):
    '''Get preselection  cutstring.
Arguments: dataMC: 'Data' or 'MC'
sys: Systematic variation, default is None. '''

    triggerMuMu   = "HLT_mumuIso"
    triggerEleEle = "HLT_ee_DZ"
    triggerMuEle  = "HLT_mue"
    preselMuMu = "isMuMu==1&&nGoodMuons==2&&nGoodElectrons==0"
    preselEE   = "isEE==1&&nGoodMuons==0&&nGoodElectrons==2"
    preselEMu  = "isEMu==1&&nGoodMuons==1&&nGoodElectrons==1"
    filterCut = "(Flag_HBHENoiseFilter&&Flag_goodVertices&&Flag_CSCTightHaloFilter&&Flag_eeBadScFilter&&weight>0)"

    assert dataMC in ['Data','MC'], "dataMC = Data or MC, got %r."%dataMC
    assert self.channel in ['all', 'EE', 'MuMu', 'EMu'], "channel must be one of all,ee,mumu,emu. Got %r."%channel
    assert self.zWindow in ['offZ', 'onZ', 'allZ'], "zWindow must be one of onZ, offZ, allZ. Got %r"%zWindow
    if self.sys['selectionModifier']: assert self.sys['selectionModifier'] in jmeVariations, "Don't know about systematic variation %r preselection(), take one of %s"%(self.sys['selectionModifier'], ",".join(jmeVariations))
    assert not (dataMC=='Data' and self.sys['selectionModifier']), "Why would you need data preselection with selectionModifier=%r? Should be None."%self.sys['selectionModifier']

  #basic cuts
    cuts = getCuts(self.sys['selectionModifier'])
    presel = "&&".join(c[1] for c in cuts)
  #Z window
    if self.zWindow in ['onZ', 'offZ']:
       presel+="&&"+getZCut(self.zWindow, self.zMassRange)
  #triggers
    if self.useTriggers:
      pMuMu = preselMuMu + "&&" + triggerMuMu
      pEE   = preselEE  + "&&" + triggerEleEle 
      pEMu  = preselEMu + "&&" + triggerMuEle
    else:
      pMuMu = preselMuMu 
      pEE   = preselEE  
      pEMu  = preselEMu 
  # dilepton channels    
    if self.channel=="MuMu":
      presel+="&&"+pMuMu
    if self.channel=="EE":
      presel+="&&"+pEE
    if self.channel=="EMu":
      presel+="&&"+pEMu
    if self.channel=="all":
      presel+="&&("+pMuMu+'||'+pEE+'||'+pEMu+')'

    if dataMC=='Data':
      presel+="&&"+filterCut
    return presel 

#define analysis regions
from regions import regions1D, regions3D
regions =  regions1D

from collections import OrderedDict
from MCBasedEstimate import MCBasedEstimate
from DataDrivenDYEstimate import DataDrivenDYEstimate
#from WardsGreatCode import DataDrivenDYEstimate, DataDrivenTTZEstimate
estimates = OrderedDict([
  [ 'TTJets',MCBasedEstimate(sample=TTJetsSample)],
  [ 'TTZ',   MCBasedEstimate(sample=TTZSample)],
  [ 'DY' ,   DataDrivenDYEstimate()], #placeholder, is just MC based using setup.DYSample
  [ 'QCD',   MCBasedEstimate(sample=QCDSample)],
])
