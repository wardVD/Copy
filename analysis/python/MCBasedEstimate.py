from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from Systematics import AbstractSystematic

class MCBasedEstimate(AbstractSystematic):
  def __init__(self, sample):
    self.sample=sample
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def estimate(self, region, setup, verbose=False):
    cut = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.preselection('MC')])
    weight = setup.sys['weight']
    if setup.sys['reweight']: weight+="*"+setup.sys['reweight']
    if verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight="("+weight+")**2")
    return {'val':val, 'sigma':sqrt(valVariance)}
