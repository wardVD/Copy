from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
from u_float import u_float
class DataDrivenDYEstimate(SystematicBaseClass):
  def __init__(self, name, cacheDir=None):
    super(DataDrivenDYEstimate, self).__init__(name, cacheDir=cacheDir)
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    weight = setup.weightString()
    #Sum of all channels for 'all'
    if channel=='all':
      return sum( [ self.cachedEstimate(region, c, channel, setup) for c in ['MuMu', 'EE', 'EMu'] ] )

    #MC based for 'EMu'
    elif channel=='EMu':
      cut = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.preselection('MC', channel=channel)])
      if setup.verbose: 
        print "Using cut %s and weight %s"%(cut, weight)
      return setup.lumi[channel]/1000. * u_float( getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut, weight=weight, returnError = True) )

    #Data driven for EMu and MuMu
    else:
      assert abs(1.-setup.lumi[channel]/setup.sample['Data'][channel]['lumi'])<0.01, "Lumi specified in setup %f does not match lumi in data sample %f in channel %s"%(setup.lumi[channel], setup.sample['Data'][channel]['lumi'], channel)
      cut_offZ_1b = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'offZ', nBTags= (1,-1))])
      cut_onZ_1b  = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'onZ',  nBTags= (1,-1))])
      cut_onZ_0b  = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'onZ',  nBTags= (0,0))])
      cut_data_onZ_0b    = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('Data', channel=channel, zWindow = 'onZ',  nBTags= (0,0))])
  #    R1 = DY-MC (offZ, 1b) / DY-MC (onZ, 1b)
  #    R2 = DY-MC (onZ, 1b) / DY-MC (onZ, 0b) 
  #    DY-est = R1*R2*(Data(2l, onZ, 0b) - EWK(onZ, 0b)) = DY-MC (offZ, 1b) / DY-MC (onZ, 0b) *( Data(2l, onZ, 0b) - EWK(onZ, 0b))
      
      yield_offZ_1b = u_float( getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_offZ_1b, weight=weight, returnError = True))
      if setup.verbose: print "yield_offZ_1b %s"%yield_offZ_1b 
      yield_onZ_0b  = u_float( getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_onZ_0b,  weight=weight, returnError = True))
      if setup.verbose: print "yield_onZ_0b %s"%yield_onZ_0b 
      yield_data    = u_float( getYieldFromChain(setup.sample['Data'][channel]['chain'], cutString = cut_data_onZ_0b,  weight=weight, returnError = True))
      if setup.verbose: print "yield_data %s cut %s weight %s"%(yield_data, cut_data_onZ_0b, weight) 

      #electroweak subtraction
      yield_ewk = u_float(0., 0.) 
      for ewk in ['TTJets' , 'singleTop' , 'TTZ' , 'diBoson', 'triBoson' , 'TTXNoZ' , 'WJetsToLNu_HT']:
        yield_ewk+=u_float(getYieldFromChain(setup.sample[ewk][channel]['chain'], cutString = cut_onZ_0b,  weight=weight, returnError=True))
        if setup.verbose: print "yield_ewk %s added, now: %s"%(ewk, yield_ewk)
      
      normRegYield = yield_data - yield_ewk
      if normRegYield.val<0: print "Warning! negative normalization region yield data: %s MC %s"%(yield_data, yield_ewk)
      
      mcRatio = yield_offZ_1b / yield_onZ_0b
      res = mcRatio * normRegYield
 
      return res
