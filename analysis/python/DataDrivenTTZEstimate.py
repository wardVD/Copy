from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
from u_float import u_float
class DataDrivenTTZEstimate(SystematicBaseClass):
  def __init__(self, name, cacheDir=None):
    super(DataDrivenTTZEstimate, self).__init__(name, cacheDir=cacheDir)
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    print   "\n" \
          + "********************************* \n" \
          + "Starting Data Driven TTZ printouts \n" \
          + "********************************* \n" 

    weight = setup.weightString()
    #Sum of all channels for 'all'
    if channel=='all':
      return sum( [ self.cachedEstimate(region, c, channel, setup) for c in ['MuMu', 'EE', 'EMu'] ] )


    #Data driven for EE, EMu and  MuMu
    assert abs(1.-setup.lumi[channel]/setup.sample['Data'][channel]['lumi'])<0.01, "Lumi specified in setup %f does not match lumi in data sample %f in channel %s"%(setup.lumi[channel], setup.sample['Data'][channel]['lumi'], channel)
    selection_2l = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1), NumberOfLeptons = 2)])
    selection_3l = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1), NumberOfLeptons = 3)])
    data_selection_3l = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('Data', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1), NumberOfLeptons = 3)])
    
    yield_2l = u_float( getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = selection_2l, weight=weight, returnError = True))
    if setup.verbose: print "yield_2l: %s"%yield_2l 
    yield_3l = u_float( getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = selection_3l, weight=weight, returnError = True))
    if setup.verbose: print "yield_3l: %s"%yield_3l 
    yield_data_3l = u_float( getYieldFromChain(setup.sample['Data'][channel]['chain'], cutString = data_selection_3l, weight=weight, returnError = True))
    if setup.verbose: print "yield_data_3l: %s (for cut: %s \n with weight: %s)"%(yield_data_3l, data_selection_3l, weight)      
    
    #electroweak subtraction
    print "\n Substracting electroweak backgrounds from data: \n"
    yield_ewk = u_float(0., 0.) 
    for ewk in ['TTJets' , 'singleTop' , 'DY_HT_LO' , 'diBoson', 'triBoson' , 'TTXNoZ' , 'WJetsToLNu_HT']:
      yield_ewk+=u_float(getYieldFromChain(setup.sample[ewk][channel]['chain'], cutString = selection_3l,  weight=weight, returnError=True))
      if setup.verbose: print "yield_ewk %s added, now: %s"%(ewk, yield_ewk)
      
    normRegYield = yield_data_3l - yield_ewk
    if normRegYield.val<0: print "\n !!!Warning!!! \n Negative normalization region yield data: (%s), MC: (%s) \n"%(yield_data_3l, yield_ewk)
      
