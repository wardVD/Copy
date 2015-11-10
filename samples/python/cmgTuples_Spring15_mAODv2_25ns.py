data_path = "/data/rschoefbeck/cmgTuples/MC25ns_v2_1l/"
from CMGTools.RootTools.samples.samples_13TeV_RunIISpring15MiniAODv2 import * 
from StopsDilepton.samples.helpers import getSubDir 
import os

for s in samples:
  s.isData = False
  s.treeName = "tree"
##for production with heppy_batch
#  s.rootFileLocation = "treeProducerSusySingleLepton/tree.root"
#  s.skimAnalyzerDir = "skimAnalyzerCount"
##for production with crab
  s.skimAnalyzerDir = ""  
  s.rootFileLocation = "tree.root"
  subDir = getSubDir(s.dataset)
  if not subDir:
    print "Not a good dataset name: %s"%s.dataset
    continue
  path = '/'.join([ data_path, getSubDir(s.dataset) ] )
  if os.path.exists(path):
    print "Found %s in %s"%(s.name, path)
    s.path = path
    s.chunkString = subDir
  else:
    print "Did not find %s in %s"%(s.name, path)
   
  
