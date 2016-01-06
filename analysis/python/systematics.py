jmeVariations = ["JER", "JERUp", "JERDown", "JECUp", "JECDown"]

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

#Abstract base class for systematics
import os
import abc
from math import sqrt
from cache import cache
import json
class SystematicBaseClass:
  __metaclass__ = abc.ABCMeta

  def __init__(self, name, cacheDir=None):
    self.name = name
    if cacheDir:
      self.cacheDir=cacheDir
      cacheFileName = os.path.join(cacheDir, self.name+'.pkl')
      if not os.path.exists(os.path.dirname(cacheFileName)):
        os.makedirs(os.path.dirname(cacheFileName))
      self.cache = cache(cacheFileName, verbosity=2)

#      def uniqueKey():
#        '''return a unique key that changes when self.sys changes'''
#        return json.dumps(self.sys, sort_keys=True)

  def uniqueKey(self, region, setup):
    return region, json.dumps(setup.sys, sort_keys=True)

  @abc.abstractmethod
  def estimate(self, region, setup):
    '''Estimate yield in 'region' using setup'''
    return
 
  def JERSystematic(self, region, setup):
    up   = self.estimate(region, setup.sysClone({'selectionModifier':'JERUp'}))
    down = self.estimate(region, setup.sysClone({'selectionModifier':'JERDown'}))
    return {'val': 0.5*(up['val'] - down['val']), 'sigma':0.5*sqrt(up['sigma']**2 + down['sigma']**2)}

  def JECSystematic(self, region, setup):
    up   = self.estimate(region, setup.sysClone({'selectionModifier':'JECUp'}))
    down = self.estimate(region, setup.sysClone({'selectionModifier':'JECDown'}))
    return {'val': 0.5*(up['val'] - down['val']), 'sigma':0.5*sqrt(up['sigma']**2 + down['sigma']**2)}
