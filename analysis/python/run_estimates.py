from setup import regions, estimates

from setup import setup as setup_
setup=setup_()

for r in regions:
  for e in estimates.keys():
    res = estimates[e].estimate(r, setup, verbose=False)
    jer = estimates[e].JERSystematic(r, setup, verbose=False)
    print e,r, res, 'jer',jer
  print
