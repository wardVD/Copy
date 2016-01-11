from setup import setup, regions, regionTTZ, estimates, estimateTTZ

setup.verbose = True
for channel in ['MuMu' ,'EE', 'EMu']:
  for r in regions:
    for e in estimates:
      res = e.cachedEstimate(r, channel, setup)
      #jer = e.JERSystematic(r, channel, setup)
      #jec = e.JECSystematic(r, channel, setup)
      print "\n Result in ", channel," for estimate ", e.name, r,":", res#, 'jer',jer, 'jec', jec
      print "\n"
    print

for channel in ['MuMu','EE','EMu']:
  res = estimateTTZ.cachedEstimate(regionTTZ[0],channel,setup)
  print "\n Result in ", channel," for estimate ", estimateTTZ.name, regionTTZ[0],":", res#, 'jer',jer, 'jec', jec
