from setup import setup, regions, estimates

setup.verbose = True
for r in regions:
  for e in estimates:
    res = e.estimate(r, setup)
    jer = e.JERSystematic(r, setup)
    jec = e.JECSystematic(r, setup)
    print "Result", e.name, r, res, 'jer',jer, 'jec', jec
  print
