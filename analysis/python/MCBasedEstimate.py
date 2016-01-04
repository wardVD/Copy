from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt

class MCBasedEstimate():
  def __init__(self, sample):
    self.sample=sample
  def estimate(self, r, setup, verbose=False,sys=None):
    cut = "&&".join([r.cutString(setup.sys['selectionModifier']), setup.preselection('MC')])
    weight = setup.sys['weight']
    if setup.sys['reweight']: weight+="*"+setup.sys['reweight']
    if verbose: 
      print "Using cut %s and weight %s"%(cut, weight)
    val          = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight=weight)
    valVariance  = setup.lumi/1000.*getYieldFromChain(self.sample['chain'], cutString = cut, weight="("+weight+")**2")
    return {'val':val, 'sigma':sqrt(valVariance)}
