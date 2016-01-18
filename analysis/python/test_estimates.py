from StopsDilepton.analysis.SetupHelpers import allChannels
from StopsDilepton.analysis.defaultAnalysis import setup, regions, bkgEstimators
#from multi_estimate import multi_estimate
from MCBasedEstimate import MCBasedEstimate
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_1l_postProcessed import *
setup.analysisOutputDir='/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/multiIso'
setup.verbose=True

#from StopsDilepton.tools.objectSelection import multiIsoLepString
#wp = 'VL'
#setup.externalCuts.append(multiIsoLepString(wp, ('l1_index','l2_index')))
#setup.prefixes.append('multiIso'+wp)

signalEstimators = [ MCBasedEstimate(name=s['name'],    sample={channel:s for channel in allChannels}, cacheDir=setup.defaultCacheDir() ) for s in signals_T2tt[:1] ]

channel = 'MuMu'
sigEstimate = signalEstimators[0] 
from StopsDilepton.analysis.Region import Region
region=Region('dl_mt2ll', (140,-1))

for e in bkgEstimators:
  e.initCache(setup.defaultCacheDir())
bkgExample = bkgEstimators[1].cachedEstimate(region, channel, setup)

sigExample = sigEstimate.cachedEstimate(region, channel, setup)
print "Region %s Channel %s sig %s bkg %s"%(region, channel, sigExample, bkgExample)
 
