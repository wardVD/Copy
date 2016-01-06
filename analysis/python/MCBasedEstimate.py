from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass

class MCBasedEstimate(SystematicBaseClass):
  def __init__(self, name, sample, cacheDir=None):
    super(MCBasedEstimate, self).__init__(name, cacheDir=cacheDir)
    self.sample=sample
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def estimate(self, region, setup):
    key =  self.uniqueKey(region, setup)
    if self.cache.contains(key):
      res = self.cache.get(key)
      if setup.verbose: print "Loading cached %s result for %r : %r"%(self.name, key, res)
      return res
    cut = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.preselection('MC')])
    weight = setup.sys['weight']
    if setup.sys['reweight']: weight+="*"+setup.sys['reweight']
    if setup.verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight="("+weight+")**2")
    res = {'val':val, 'sigma':sqrt(valVariance)}
    self.cache.add(self.uniqueKey(region, setup), res)
    return res
