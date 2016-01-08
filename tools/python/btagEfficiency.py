import ROOT, pickle, itertools, os
from operator import or_

#Method 1b
effFile   = '$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'
sfFile_1b = '$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/CSVv2.csv' 

#Method 1d
#https://twiki.cern.ch/twiki/bin/view/CMS/BTagShapeCalibration
#https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
sfFile_1d = '$CMSSW_BASE/src/StopsDilepton/tools/data/btagEfficiencyData/ttH_BTV_CSVv2_13TeV_2015D_20151120.csv'

#binning in pt and eta
ptBorders = [30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670]
ptBins = []
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]
for i in range(len(ptBorders)-1):
  ptBins.append([ptBorders[i], ptBorders[i+1]])
ptBins.append([ptBorders[-1], -1])

flavourSys_1d = {
  5:{'central', 'up_jes', 'down_jes', 'up_lf', 'down_lf', 'up_hfstats1', 'down_hfstats1', 'up_hfstats2', 'down_hfstats2'}, 
  4:{'central', 'up_cferr1', 'down_cferr1', 'up_cferr2', 'down_cferr2'}, 
  0:{'central', 'up_jes', 'down_jes', 'up_hf', 'down_hf', 'up_lfstats1', 'down_lfstats1', 'up_lfstats2', 'down_lfstats2'}, 
}
btagMethod1DSystematics = reduce(or_, flavourSys_1d.values())

def toFlavourKey(pdgId):
  if abs(pdgId)==5: return ROOT.BTagEntry.FLAV_B
  if abs(pdgId)==4: return ROOT.BTagEntry.FLAV_C
  return ROOT.BTagEntry.FLAV_UDSG

# get the combinatorical weights for jet efficiency list eff 
def getTagWeightDict(effs, maxConsideredBTagWeight):
  zeroTagWeight = 1.
  for e in effs:
    zeroTagWeight*=(1-e)
  tagWeight={}
  for i in range(min(len(effs), maxConsideredBTagWeight)+1):
    tagWeight[i]=zeroTagWeight
    twfSum = 0.
    for tagged in itertools.combinations(effs, i):
      twf=1.
      for fac in [x/(1-x) for x in tagged]:
        twf*=fac
      twfSum+=twf
    tagWeight[i]*=twfSum
  for i in range(maxConsideredBTagWeight+1):
    if not tagWeight.has_key(i):
      tagWeight[i] = 0.
  return tagWeight


class btagEfficiency:
  def getMCEff(self, pdgId, pt, eta):
    for ptBin in ptBins:
      if pt>=ptBin[0] and (pt<ptBin[1] or ptBin[1]<0):
        aeta=abs(eta)
        for etaBin in etaBins:
          if abs(aeta)>=etaBin[0] and abs(aeta)<etaBin[1]:
  #          print ptBin, etaBin      , mcEff[tuple(ptBin)][tuple(etaBin)]
            if abs(pdgId)==5:      return  self.mcEff[tuple(ptBin)][tuple(etaBin)]["b"]
            elif abs(pdgId)==4:    return  self.mcEff[tuple(ptBin)][tuple(etaBin)]["c"]
            else:                  return  self.mcEff[tuple(ptBin)][tuple(etaBin)]["other"]
    if self.verbose: print "[btagEfficiency] [getMCEff] No MC efficiency for pt %f eta %f pdgId %i"%(pt,eta,pdgId)
    return 1

  def getSF_1b(self, pdgId, pt, eta):
    assert pt>=20, "BTag SF Not implemented below 20 GeV"
    doubleUnc = False
    pt_=pt
    if pt<30: 
      pt_=30 
      doubleUnc=True
    if pt>=670: 
      pt_=669.9
      doubleUnc = True
    if abs(pdgId)==5: #SF for b
      sf      = self.readerMuCentral.eval(ROOT.BTagEntry.FLAV_B, eta, pt_)
      sf_b_d  = self.readerMuDown   .eval(ROOT.BTagEntry.FLAV_B, eta, pt_)
      sf_b_u  = self.readerMuUp     .eval(ROOT.BTagEntry.FLAV_B, eta, pt_)
      sf_l_d  = 1.
      sf_l_u  = 1.
    elif abs(pdgId)==4: #SF for c
      sf     = self.readerMuCentral.eval(ROOT.BTagEntry.FLAV_C, eta, pt_)
      sf_b_d = self.readerMuDown .eval(ROOT.BTagEntry.FLAV_C, eta, pt_)
      sf_b_u = self.readerMuUp   .eval(ROOT.BTagEntry.FLAV_C, eta, pt_)
      sf_l_d = 1.
      sf_l_u = 1.
    else: #SF for light flavours
      sf     = self.readerCombCentral.eval(ROOT.BTagEntry.FLAV_UDSG, eta, pt_)
      sf_b_d = 1.
      sf_b_u = 1.
      sf_l_d = self.readerCombDown .eval(ROOT.BTagEntry.FLAV_UDSG, eta, pt_)
      sf_l_u = self.readerCombUp   .eval(ROOT.BTagEntry.FLAV_UDSG, eta, pt_)
    if doubleUnc:
      sf_b_d = sf + 2.*(sf_b_d - sf)
      sf_b_u = sf + 2.*(sf_b_u - sf)
      sf_l_d = sf + 2.*(sf_l_d - sf)
      sf_l_u = sf + 2.*(sf_l_u - sf)
    return (sf, sf_b_d, sf_b_u, sf_l_d, sf_l_u)

  def addBTagEffToJet_1b(self, j):
    mcEff = self.getMCEff(j['hadronFlavour'], j['pt'], j['eta'])
    sf =    self.getSF_1b(j['hadronFlavour'], j['pt'], j['eta'])
    j['beff'] =  {'MC':mcEff, 'SF':mcEff*sf[0], 'SF_b_Down':mcEff*sf[1], 'SF_b_Up':mcEff*sf[2], 'SF_l_Down':mcEff*sf[3], 'SF_l_Up':mcEff*sf[4]}

  def addBTagEffToJet_1d(self, j):
#      print self.readers
#      print {sys: 1. if sys not in flavourSys_1d[j['hadronFlavour']] else self.readers[sys].eval(toFlavourKey(j['hadronFlavour']), j['eta'], j['pt'], j['btagCSV']) for sys in btagMethod1DSystematics}
#      for sys in btagMethod1DSystematics:
#        print j['hadronFlavour'], flavourSys_1d[j['hadronFlavour']]
#        if sys not in flavourSys_1d[abs(j['hadronFlavour'])]:
#          print sys, self.readers[sys]
#        else: 
#          print sys, 1
    j['beff'] = {sys: 1. if sys not in flavourSys_1d[abs(j['hadronFlavour'])] else self.readers[sys].eval(toFlavourKey(j['hadronFlavour']), j['eta'], j['pt'], j['btagCSV']) for sys in btagMethod1DSystematics}

  def __init__(self, method = '1d', WP = ROOT.BTagEntry.OP_MEDIUM, mcEfficiencyFile = effFile, scaleFactorFile = sfFile_1d, verbose=True):
    self.verbose=verbose
    self.method=method
    if self.method=='1b':
      print "[btagEfficiency Method %s] Loading scale factors from %s"%(self.method, os.path.expandvars(scaleFactorFile))
      self.calib = ROOT.BTagCalibration("csvv2", os.path.expandvars(scaleFactorFile))
  ## get SF
      self.readerMuUp        = ROOT.BTagCalibrationReader(self.calib, WP, "mujets", "up")
      self.readerMuCentral   = ROOT.BTagCalibrationReader(self.calib, WP, "mujets", "central")
      self.readerMuDown      = ROOT.BTagCalibrationReader(self.calib, WP, "mujets", "down")
      self.readerCombUp      = ROOT.BTagCalibrationReader(self.calib, WP, "comb", "up")
      self.readerCombCentral = ROOT.BTagCalibrationReader(self.calib, WP, "comb", "central")
      self.readerCombDown    = ROOT.BTagCalibrationReader(self.calib, WP, "comb", "down")
      print "[btagEfficiency Method %s] Loading MC efficiency %s"%(self.method, os.path.expandvars(mcEfficiencyFile))
      self.mcEff = pickle.load(file(os.path.expandvars(mcEfficiencyFile)))
  #    for ptk in self.mcEff.keys():
  #      for ek in self.mcEff[ptk].keys():
  #        for fk in ["b", "c", "other"]:
  #            if self.mcEff[ptk][ek][fk]==1.:
  #            print "[btagEfficiency] Found efficiency of 1"
      self.addBTagEffToJet = self.addBTagEffToJet_1b
    elif self.method=='1d':
      print "[btagEfficiency Method %s] Loading scale factors from %s"%(self.method, os.path.expandvars(scaleFactorFile))
      self.calib = ROOT.BTagCalibration("csvv2", os.path.expandvars(scaleFactorFile))
      self.readers = {sys: ROOT.BTagCalibrationReader(self.calib, ROOT.BTagEntry.OP_RESHAPING, "iterativefit", sys) for sys in btagMethod1DSystematics}
      self.addBTagEffToJet = self.addBTagEffToJet_1d
    else: 
      print "[btagEfficiency] Method %s not known!"%self.method
