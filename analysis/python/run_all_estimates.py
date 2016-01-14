from StopsDilepton.analysis.SetupHelpers import allChannels
from StopsDilepton.analysis.defaultAnalysis import setup, regions, bkgEstimators
#from multi_estimate import multi_estimate
from MCBasedEstimate import MCBasedEstimate
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_1l_postProcessed import *
setup.analysisOutputDir='/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results/test2'
setup.verbose=True

signalEstimators = [ MCBasedEstimate(name=s['name'],    sample={channel:s for channel in allChannels}, cacheDir=setup.getDefaultCacheDir() ) for s in signals_T2tt ]

#estimate = signals_T2tt[0]['estimator']
#isSignal=True
#regions=regions[:1]

def wrapper(args):
    r,channel,setup = args
    res = estimate.cachedEstimate(r, channel, setup, save=False)
#    res = estimate._estimate(r, channel, setup)
    return (estimate.uniqueKey(r, channel, setup), res )

for isSignal, bkgEstimators_ in [ [ True, signalEstimators ], [ False, bkgEstimators ] ]:
  for estimate in bkgEstimators_:
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
