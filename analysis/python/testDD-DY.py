from StopsDilepton.analysis.Region import Region
from StopsDilepton.analysis.defaultAnalysis import setup

#Always taking data lumi
setup.lumi = {channel:setup.sample['Data'][channel]['lumi'] for channel in setup.sample['Data'].keys()}
setup.loadChains()

setup.verbose = True

from StopsDilepton.analysis.DataDrivenDYEstimate import DataDrivenDYEstimate
estimateDY = DataDrivenDYEstimate(name='DY-DD', cacheDir=None)

regionDY = Region('dl_mt2ll', (140,-1))

for channel in ['MuMu','EE','EMu']:
  res = estimateDY.cachedEstimate(regionDY,channel,setup)
  print "\n Result in ", channel," for estimate ", estimateDY.name, regionDY,":", res#, 'jer',jer, 'jec', jec
