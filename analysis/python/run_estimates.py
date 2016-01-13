from setup import setup, regions, estimates
setup.verbose = True

for estimate in estimates:

  def wrapper(args):
      r,channel,setup = args
      res = estimate.cachedEstimate(r, channel, setup, save=False)
      return (estimate.uniqueKey(r, channel, setup), res )

  jobs=[]
  for channel in ['MuMu' ,'EE', 'EMu']:
    for r in regions:
      jobs.append((r, channel, setup))
      jobs.extend(estimate.getAllSysJobs(r, channel, setup))

  from multiprocessing import Pool
  pool = Pool(processes=20)

  results = pool.map(wrapper, jobs)
  pool.close()
  pool.join()

  for r in results:
    estimate.cache.add(*r, save=False)

  estimate.cache.save()
