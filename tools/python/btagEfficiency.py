import ROOT, pickle, itertools, os

#Method 1b
effFile = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/btagEfficiencyData/TTJets_DiLepton_comb_2j_2l.pkl'
sfFile_1b =  '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/btagEfficiencyData/CSVv2.csv' 

#Method 1d
#https://twiki.cern.ch/twiki/bin/view/CMS/BTagShapeCalibration
#https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods
sfFile_1d = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/btagEfficiencyData/ttH_BTV_CSVv2_13TeV_2015D_20151120.csv'

ptBorders = [30, 40, 50, 60, 70, 80, 100, 120, 160, 210, 260, 320, 400, 500, 670]
ptBins = []
etaBins = [[0,0.8], [0.8,1.6], [ 1.6, 2.4]]

for i in range(len(ptBorders)-1):
  ptBins.append([ptBorders[i], ptBorders[i+1]])
ptBins.append([ptBorders[-1], -1])

btagMethod1DSystematics = ['central', 'up_jes', 'down_jes', 'up_lf', 'down_lf', 'up_hf', 'down_hf', 'up_hfstats1', 'down_hfstats1', 'up_hfstats2', 'down_hfstats2', 'up_lfstats1', 'down_lfstats1', 'up_lfstats2', 'down_lfstats2', 'up_cferr1', 'down_cferr1', 'up_cferr2', 'down_cferr2']
flavourSys_1d = {
  5:['central', 'up_jes', 'down_jes', 'up_lf', 'down_lf', 'up_hfstats1', 'down_hfstats1', 'up_hfstats2', 'down_hfstats2'], 
  0:['central', 'up_jes', 'down_jes', 'up_hf', 'down_hf', 'up_lfstats1', 'down_lfstats1', 'up_lfstats2', 'down_lfstats2'], 
  4:['central', 'up_cferr1', 'down_cferr1', 'up_cferr2', 'down_cferr2'], 
}

def toFlavourKey(pdgId):
  if abs(pdgId)==5: return ROOT.BTagEntry.FLAV_B
  if abs(pdgId)==4: return ROOT.BTagEntry.FLAV_C
  return ROOT.BTagEntry.FLAV_UDSG

class btagEfficiency:
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
    elif self.method=='1d':
      print "[btagEfficiency Method %s] Loading scale factors from %s"%(self.method, os.path.expandvars(scaleFactorFile))
      self.calib = ROOT.BTagCalibration("csvv2", os.path.expandvars(scaleFactorFile))
      self.readers = {sys: ROOT.BTagCalibrationReader(self.calib, ROOT.BTagEntry.OP_RESHAPING, "iterativefit", sys) for sys in btagMethod1DSystematics}
    else: 
      print "[btagEfficiency] Method %s not known!"%self.method

  def getMCEff(self, pdgId, pt, eta):
    if not self.method=='1b':
      print "[btagEfficiency] MC efficiency not available for method %s"%self.method
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

  def addBTagEffToJet(self, j):
    if self.method=='1b':
      mcEff = self.getMCEff(j['hadronFlavour'], j['pt'], j['eta'])
      sf =    self.getSF_1b(j['hadronFlavour'], j['pt'], j['eta'])
      j['beff'] =  {'MC':mcEff, 'SF':mcEff*sf[0], 'SF_b_Down':mcEff*sf[1], 'SF_b_Up':mcEff*sf[2], 'SF_l_Down':mcEff*sf[3], 'SF_l_Up':mcEff*sf[4]}
    elif self.method=='1d':
#      print self.readers
#      print {sys: 1. if sys not in flavourSys_1d[j['hadronFlavour']] else self.readers[sys].eval(toFlavourKey(j['hadronFlavour']), j['eta'], j['pt'], j['btagCSV']) for sys in btagMethod1DSystematics}
#      for sys in btagMethod1DSystematics:
#        print j['hadronFlavour'], flavourSys_1d[j['hadronFlavour']]
#        if sys not in flavourSys_1d[abs(j['hadronFlavour'])]:
#          print sys, self.readers[sys]
#        else: 
#          print sys, 1
      j['beff'] = {sys: 1. if sys not in flavourSys_1d[abs(j['hadronFlavour'])] else self.readers[sys].eval(toFlavourKey(j['hadronFlavour']), j['eta'], j['pt'], j['btagCSV']) for sys in btagMethod1DSystematics}
#      print j['hadronFlavour'], j['beff']
    else:
      print "[btagEfficiency] Method %s not known!"%self.method

# get the combinatorical weights for jet efficiency list eff 
  def getTagWeightDict(self, effs, maxConsideredBTagWeight):
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

## Function for different method, described in https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#1a_Event_reweighting_using_scale
## FastSim corrections not implemented yet
#
#def getBTagWeight(c, sms=""):
#  nsoftjets = int(getVarValue(c, "nJet30"))
#  njets = int(getVarValue(c, "nJet"))
#  jets = []
#  for i in range(njets):
#    isBtagged = False
#    jPt     = getVarValue(c, "Jet_pt", i)
#    jEta    = getVarValue(c, "Jet_eta", i)
#    jParton = getVarValue(c, "Jet_mcFlavour", i)
#    jBTagCSV = getVarValue(c, "Jet_btagCSV", i)
#    if jBTagCSV > 0.890: isBtagged = True
#    if jPt<=30. or abs(jEta)>=2.4 or (not getVarValue(c, "Jet_id", i)):
#      continue
#    jets.append([jParton, jPt, jEta, isBtagged])
#  if len(jets) != nsoftjets: print 'Different number of jets in collection than there should be!!'
#  mceffs = tuple()
#  mceffs_SF = tuple()
#  mceffs_SF_b_Up = tuple()
#  mceffs_SF_b_Down = tuple()
#  mceffs_SF_light_Up = tuple()
#  mceffs_SF_light_Down = tuple()
#  PMC = 1.
#  PData = 1.
#  PData_b_up = 1.
#  PData_b_down = 1.
#  PData_l_up = 1.
#  PData_l_down = 1.
#  for jParton, jPt, jEta, isBtagged in jets:
#    r = getMCEff(parton=jParton, pt=jPt, eta=jEta, year=2015)#getEfficiencyAndMistagRate(jPt, jEta, jParton )
#    if sms!="":
#      fsim_SF = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"mean",jEta)
#      fsim_SF_up = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"up",jEta)
#      fsim_SF_down = ROOT.getFastSimCorr(partonName(abs(jParton)),jPt,"down",jEta)
#    else:
#      fsim_SF = 1.
#      fsim_SF_up = 1.
#      fsim_SF_down = 1.
#    if isBtagged:
#      PMC *= r['mcEff']
#      PData *= r['mcEff']*r['SF']
#      if abs(jParton)==5 or abs(jParton)==4:
#        PData_b_up *= r['mcEff']*r['SF_up']
#        PData_b_down *= r['mcEff']*r['SF_down']
#        PData_l_up *= r['mcEff']*r['SF']
#        PData_l_down *= r['mcEff']*r['SF']
#      else:
#        PData_b_up *= r['mcEff']*r['SF']
#        PData_b_down *= r['mcEff']*r['SF']
#        PData_l_up *= r['mcEff']*r['SF_up']
#        PData_l_down *= r['mcEff']*r['SF_down']
#    else:
#      PMC *= (1. - r['mcEff'])
#      PData *= (1. - r['mcEff']*r['SF'])
#      if abs(jParton)==5 or abs(jParton)==4:
#        PData_b_up *=   (1 - r['mcEff']*r['SF_up'])
#        PData_b_down *= (1 - r['mcEff']*r['SF_down'])
#        PData_l_up *=   (1 - r['mcEff']*r['SF'])
#        PData_l_down *= (1 - r['mcEff']*r['SF'])
#      else:
#        PData_b_up *=   (1 - r['mcEff']*r['SF'])
#        PData_b_down *= (1 - r['mcEff']*r['SF'])
#        PData_l_up *=   (1 - r['mcEff']*r['SF_up'])
#        PData_l_down *= (1 - r['mcEff']*r['SF_down'])
#      #PData_up *= (1 - r['mcEff']*r['SF_up'])
#      #PData_down *= (1 - r['mcEff']*r['SF_down'])
#    res = {'w':PData/PMC, 'w_b_up':PData_b_up/PMC, 'w_b_down':PData_b_down/PMC, 'w_l_up':PData_l_up/PMC, 'w_l_down':PData_l_down/PMC}
#    return res
#
#
#
