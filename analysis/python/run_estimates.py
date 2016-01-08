from setup import setup, regions, estimates

setup.verbose = True
for channel in ['EE']:
  for r in regions[:1]:
    for e in estimates:
      res = e.cachedEstimate(r, channel, setup)
      #jer = e.JERSystematic(r, channel, setup)
      #jec = e.JECSystematic(r, channel, setup)
      print "\n Result", channel, e.name, r, res#, 'jer',jer, 'jec', jec
      print "\n"
    print
