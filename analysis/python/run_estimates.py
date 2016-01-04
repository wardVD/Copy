from setup import regions, estimates

from setup import setup as setup_
setup=setup_()

from systematics import jmeSystematics, btagSystematics

for r in regions:
  for e in estimates.keys():
    for sys in [None] + jmeSystematics + btagSystematics:
      res = estimates[e].estimate(r, setup.clone(sys), verbose=True)
      print sys, e,r,res
    print
  print
