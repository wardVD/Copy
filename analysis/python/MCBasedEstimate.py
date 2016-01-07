from StopsDilepton.tools.helpers import getYieldFromChain
from u_float import u_float 
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
    return setup.lumi[channel]/1000.*u_float(getYieldFromChain(self.sample[channel]['chain'], cutString = cut, weight=weight, returnError = True) )
