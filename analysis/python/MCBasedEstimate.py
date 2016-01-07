from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass

class MCBasedEstimate(SystematicBaseClass):
  def __init__(self, name, sample, cacheDir=None):
    super(MCBasedEstimate, self).__init__(name, cacheDir=cacheDir)
    self.sample=sample
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    cut = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.preselection('MC', channel=channel)])
    weight = setup.weightString()

    if setup.verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(self.sample[channel]['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(self.sample[channel]['chain'], cutString = cut, weight="("+weight+")**2")
    res = {'val':val, 'sigma':sqrt(valVariance)}
    return res
