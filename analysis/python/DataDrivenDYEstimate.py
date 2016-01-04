from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt

class DataDrivenDYEstimate():
  def __init__(self):
    return
  #Ward, the following function just returns the MC based estimate, despite the name. Please implement the data-driven one.
  def estimate(self, r, setup, verbose=False, sys=None):
    cut = "&&".join([r.cutString(), setup.preselection('MC')])
    weight = setup.sys['weight']
    if setup.sys['reweight']: weight+="*"+setup.sys['reweight']
    if verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(setup.DYSample['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(setup.DYSample['chain'], cutString = cut, weight="("+weight+")**2")
    return {'val':val, 'sigma':sqrt(valVariance)}
