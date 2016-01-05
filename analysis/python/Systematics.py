jmeVariations = ["JER", "JERUp", "JERDown", "JECUp", "JECDown"]
#jmeSystematics = {j:{'selectionModifier':j} for j in jmeVariations}

#def JERSystematic(**kwargs):
##  ref = m.estimate(r, setup, verbose)
#  up   = m.estimate(setup.sysClone({'selectionModifier':'JERUp'}))
#  down = m.estimate(setup.sysClone({'selectionModifier':'JERDown'}))
#  return 0.5*(up['val'] - down['val']) 
#def JECSystematic(**kwargs):
##  ref = m.estimate(r, setup, verbose)
#  up   = m.estimate(r, setup.sysClone({'selectionModifier':'JECUp'}), verbose)
#  down = m.estimate(r, setup.sysClone({'selectionModifier':'JECDown'}), verbose)
#  return 0.5*(up['val'] - down['val']) 
#  
#jmeSystematics = {
#
#"JER":{'func':lambda estimate, region, setup: estimate(region, setup.sysClone({'selectionModifier':'JERUp'})) - }
#
#}

btagVariationWeights = [
'reweightBTag_central',
'reweightBTag_up_hfstats1',
'reweightBTag_down_hfstats1',
'reweightBTag_up_hfstats2',
'reweightBTag_down_hfstats2',
'reweightBTag_up_hf',
'reweightBTag_down_hf',
'reweightBTag_up_lfstats1',
'reweightBTag_down_lfstats1',
'reweightBTag_up_lfstats2',
'reweightBTag_down_lfstats2',
'reweightBTag_up_lf',
'reweightBTag_down_lf',
'reweightBTag_up_cferr1',
'reweightBTag_down_cferr1',
'reweightBTag_up_cferr2',
'reweightBTag_down_cferr2',
#'reweightBTag_up_jes',
#'reweightBTag_down_jes',
]
#btagSystematics = {w.replace('reweightBTag_',''):{'reweight':w} for w in btagVariationWeights}

#Abstract base class for systematics
import abc
from math import sqrt
class AbstractSystematic:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def estimate(self, region, setup, verbose=False):
    '''Estimate yield in 'region' using setup'''
    return
 
  def JERSystematic(self, region, setup, verbose=False):
    up   = self.estimate(region, setup.sysClone({'selectionModifier':'JERUp'}), verbose=verbose)
    down = self.estimate(region, setup.sysClone({'selectionModifier':'JERDown'}), verbose=verbose)
    return {'val': 0.5*(up['val'] - down['val']), 'sigma':0.5*sqrt(up['sigma']**2 + down['sigma']**2)}
     
