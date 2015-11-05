data_path = "/data/rschoefbeck/cmgTuples/Run2015D_1l_2" 
from CMGTools.RootTools.samples.samples_13TeV_DATA2015 import * 
from StopsDilepton.samples.helpers import getSubDir 
import os

samples = [DoubleEG_Run2015D_Promptv4, MuonEG_Run2015D_Promptv4, DoubleMuon_Run2015D_Promptv4, DoubleEG_Run2015D_05Oct, MuonEG_Run2015D_05Oct, DoubleMuon_Run2015D_05Oct]

for s in samples:
  s.isData = True
  s.json = "$CMSSW_BASE/src/CMGTools/TTHAnalysis/data/json/Cert_246908-259891_13TeV_PromptReco_Collisions15_25ns_JSON.txt"
  s.treeName = "tree"
##for production with heppy_batch
  s.rootFileLocation = "treeProducerSusySingleLepton/tree.root"
  s.skimAnalyzerDir = "skimAnalyzerCount"
##for production with crab
#  s.skimAnalyzerDir = ""  
#  s.rootFileLocation = "tree.root"
  subDir = s.name 
  if not subDir:
    print "Not a good dataset name: %s"%s.dataset
    continue
#  path = '/'.join([ data_path, getSubDir(s.dataset) ] )
  path = data_path #'/'.join([ data_path, getSubDir(s.dataset) ] )
  if os.path.exists(path):
    print "Found %s in %s"%(s.name, path)
    s.path = path
    s.chunkString = subDir
  else:
    print "Did not find %s in %s"%(s.name, path)
   
  
