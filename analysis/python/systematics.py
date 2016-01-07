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
    else:
      self.cache=None

  def uniqueKey(self, region, channel, setup):
    return region, setup.lumi, channel, json.dumps(setup.sys, sort_keys=True)

  def cachedEstimate(self, region, channel, setup):
    key =  self.uniqueKey(region, channel, setup)
    if self.cache and self.cache.contains(key):
      res = self.cache.get(key)
      if setup.verbose: print "Loading cached %s result for %r : %r"%(self.name, key, res)
      return res
    elif self.cache:
      return self.cache.add( key, self._estimate( region, channel, setup))
    else:
      return self._estimate( region, channel, setup)

  @abc.abstractmethod
  def _estimate(self, region, channel, setup):
    '''Estimate yield in 'region' using setup'''
    return
 
  def JERSystematic(self, region, channel, setup):
    up   = self.cachedEstimate(region, channel, setup.sysClone({'selectionModifier':'JERUp'}))
    down = self.cachedEstimate(region, channel, setup.sysClone({'selectionModifier':'JERDown'}))
    return {'val': 0.5*(up['val'] - down['val']), 'sigma':0.5*sqrt(up['sigma']**2 + down['sigma']**2)}

  def JECSystematic(self, region, channel, setup):
    up   = self.cachedEstimate(region, channel, setup.sysClone({'selectionModifier':'JECUp'}))
    down = self.cachedEstimate(region, channel, setup.sysClone({'selectionModifier':'JECDown'}))
    return {'val': 0.5*(up['val'] - down['val']), 'sigma':0.5*sqrt(up['sigma']**2 + down['sigma']**2)}
