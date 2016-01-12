from region import region
from setup import setup
#regionTTZ = getRegionsFromThresholds('dl_mt2ll', [0])  ##intention was to not use this stupid func outside. 

from DataDrivenDYEstimate import DataDrivenDYEstimate
estimateDY = DataDrivenDYEstimate(name='DY-DD', cacheDir=setup.cacheDir)

regionDY = region('dl_mt2ll', (140,-1))

for channel in ['MuMu','EE','EMu']:
  res = estimateDY.cachedEstimate(regionDY,channel,setup)
  print "\n Result in ", channel," for estimate ", estimateDY.name, regionDY,":", res#, 'jer',jer, 'jec', jec
