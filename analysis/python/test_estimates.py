from StopsDilepton.analysis.SetupHelpers import allChannels
from StopsDilepton.analysis.defaultAnalysis import setup, regions, bkgEstimators
#from multi_estimate import multi_estimate
from MCBasedEstimate import MCBasedEstimate
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_1l_postProcessed import *
setup.analysisOutputDir='/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test2'
setup.verbose=True

signalEstimators = [ MCBasedEstimate(name=s['name'],    sample={channel:s for channel in allChannels}, cacheDir=setup.getDefaultCacheDir() ) for s in signals_T2tt[:1] ]

channel = 'MuMu'
estimate = signalEstimators[0] 
region=regions[1]

bkgExample = bkgEstimators[0].cachedEstimate(region, channel, setup)

sigExample = estimate.cachedEstimate(region, channel, setup)
print "Region %s Channel %s sig %s bkg %s"%(region, channel, sigExample, bkgExample)
 
