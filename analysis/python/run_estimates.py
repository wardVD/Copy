from setup import setup, regions, estimates
setup.verbose = True
<<<<<<< HEAD
for channel in ['MuMu']:
  for r in regions:
    for e in estimates:
      res = e.cachedEstimate(r, channel, setup)
      #jer = e.JERSystematic(r, channel, setup)
      #jec = e.JECSystematic(r, channel, setup)
      print "\n Result in ", channel," for estimate ", e.name, r,":", res#, 'jer',jer, 'jec', jec
      print "\n"
    print
=======
>>>>>>> central/master

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
