from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
class DataDrivenDYEstimate(SystematicBaseClass):
  def __init__(self, name, cacheDir=None):
    super(DataDrivenDYEstimate, self).__init__(name, cacheDir=cacheDir)
    return
  #Ward, the following function just returns the MC based estimate, despite the name. Please implement the data-driven one.
  def estimate(self, region, setup):
    cut = "&&".join([region.cutString(), setup.preselection('MC')])
    weight = setup.sys['weight']
    if setup.sys['reweight']: weight+="*"+setup.sys['reweight']
    if setup.verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(setup.DYSample['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(setup.DYSample['chain'], cutString = cut, weight="("+weight+")**2")
    return {'val':val, 'sigma':sqrt(valVariance)}
