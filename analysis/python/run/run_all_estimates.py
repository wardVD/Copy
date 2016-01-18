from optparse import OptionParser
parser = OptionParser()
parser.add_option("--dontSkipIfCachefileExists", dest="dontSkipIfCachefileExists", default = False, action="store_true", help="dontSkipIfCachefileExists?")
parser.add_option("--metSigMin", dest="metSigMin", default=5, type="int", action="store", help="metSigMin?")
parser.add_option("--metMin", dest="metMin", default=80, type="int", action="store", help="metMin?")
parser.add_option("--multiIsoWP", dest="multiIsoWP", default="", type="string", action="store", help="multiIsoWP?")
(options, args) = parser.parse_args()

from StopsDilepton.analysis.SetupHelpers import allChannels
from StopsDilepton.analysis.defaultAnalysis import setup, regions, bkgEstimators
setup.analysisOutputDir='/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test3'
setup.parameters['metMin'] = options.metMin
setup.parameters['metSigMin'] = options.metSigMin

if options.multiIsoWP!="":
  multiIsoWPs = ['VL', 'L', 'M', 'T', 'VT']
  assert options.multiIsoWP in multiIsoWPs, "MultiIsoWP not defined. Use one of %s"%",".join(multiIsoWPs)
  from StopsDilepton.tools.objectSelection import multiIsoLepString
  setup.externalCuts.append(multiIsoLepString(options.multiIsoWP, ('l1_index','l2_index')))
  setup.prefixes.append('multiIso'+options.multiIsoWP)

for e in bkgEstimators:
  e.initCache(setup.defaultCacheDir())

setup.verbose=True
#from multi_estimate import multi_estimate
from StopsDilepton.analysis.MCBasedEstimate import MCBasedEstimate
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_1l_postProcessed import *
signalEstimators = [ MCBasedEstimate(name=s['name'],    sample={channel:s for channel in allChannels}, cacheDir=setup.defaultCacheDir() ) for s in signals_T2tt ]

#estimate = signals_T2tt[0]['estimator']
#isSignal=True
#regions=regions[:1]
#bkgEstimators=[]
#signalEstimators = signalEstimators[:1]
#regions=regions[:1]

def wrapper(args):
    r,channel,setup = args
    res = estimate.cachedEstimate(r, channel, setup, save=False)
#    res = estimate._estimate(r, channel, setup)
    return (estimate.uniqueKey(r, channel, setup), res )

for isSignal, bkgEstimators_ in [ [ True, signalEstimators ], [ False, bkgEstimators ] ]:
  for estimate in bkgEstimators_:
    if not options.dontSkipIfCachefileExists and estimate.cache.cacheFileLoaded: 
      print "Cache file %s was loaded -> Skipping."%estimate.cache.filename
      continue
    jobs=[]
    for channel in ['MuMu' ,'EE', 'EMu']:
      for r in regions:
        jobs.append((r, channel, setup))
        jobs.extend(estimate.getBkgSysJobs(r, channel, setup))
        if isSignal:
          jobs.extend(estimate.getSigSysJobs(r, channel, setup))

    from multiprocessing import Pool
    pool = Pool(processes=20)

    results = pool.map(wrapper, jobs)
    pool.close()
    pool.join()

    for r in results:
      estimate.cache.add(*r, save=False)

    for channel in ['all']:
      for r in regions:
        estimate.cachedEstimate(r, channel, setup, save=False)
        map(lambda args:estimate.cachedEstimate(*args, save=False), estimate.getBkgSysJobs(r, channel, setup))
        if isSignal:
          map(lambda args:estimate.cachedEstimate(*args, save=False), estimate.getSigSysJobs(r, channel, setup))

    estimate.cache.save()
