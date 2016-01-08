from setup import setup, regions, estimates

setup.verbose = True
for channel in ['all']:
  for r in regions:
    for e in estimates:
      res = e.cachedEstimate(r, channel, setup)
      jer = e.JERSystematic(r, channel, setup)
      jec = e.JECSystematic(r, channel, setup)
      print "Result", channel, e.name, r, res, 'jer',jer, 'jec', jec
    print
