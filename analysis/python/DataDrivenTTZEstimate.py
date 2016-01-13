from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
from u_float import u_float
from StopsDilepton.tools.helpers import printHeader

class DataDrivenTTZEstimate(SystematicBaseClass):
  def __init__(self, name, cacheDir=None):
    super(DataDrivenTTZEstimate, self).__init__(name, cacheDir=cacheDir)
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    printHeader("DD TTZ prediction for '%s' channel %s" %(self.name, channel))

    #Sum of all channels for 'all'
    if channel=='all':
      return sum( [ self.cachedEstimate(region, c, channel, setup) for c in ['MuMu', 'EE', 'EMu'] ] )
    else:
      #Data driven for EE, EMu and  MuMu. 
      preSelection = setup.preselection('MC', channel=channel)
      weight = preSelection['weightStr']

      #check lumi consistency
      assert abs(1.-setup.lumi[channel]/setup.sample['Data'][channel]['lumi'])<0.01, "Lumi specified in setup %f does not match lumi in data sample %f in channel %s"%(setup.lumi[channel], setup.sample['Data'][channel]['lumi'], channel)
      
      selection_2l = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1))['cut']])
      threeLeptonCut = "nGoodMuons+nGoodElectrons==3" #use whatever
      selection_3l = "&&".join([
  #      region.cutString(setup.sys['selectionModifier']), ??? is this not a bug? Why the region
        setup.selection('MC', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1), hadronicSelection = True)['cut'],
        threeLeptonCut
      ])

      #continue similarly
      data_selection_3l = "&&".join([
  #      region.cutString(setup.sys['selectionModifier']), ??? is this not a bug? Why the region
        setup.selection('Data', channel=channel, zWindow = 'offZ', nJets = (4,-1), nBTags= (2,-1), hadronicSelection = True)['cut'],
        threeLeptonCut
      ])
      
      yield_2l = u_float( getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = selection_2l, weight=weight, returnError = True))
      if setup.verbose: print "yield_2l: %s"%yield_2l 
      yield_3l = u_float( getYieldFromChain(setup.sample['TTZ'][channel]['chain'], cutString = selection_3l, weight=weight, returnError = True))
      if setup.verbose: print "yield_3l: %s"%yield_3l 
      yield_data_3l = u_float( getYieldFromChain(setup.sample['Data'][channel]['chain'], cutString = data_selection_3l, weight=weight, returnError = True))
      if setup.verbose: print "yield_data_3l: %s (for cut: %s \n with weight: %s)"%(yield_data_3l, data_selection_3l, weight)      
      
      #electroweak subtraction
      print "\n Substracting electroweak backgrounds from data: \n"
      yield_other = u_float(0., 0.) 
      for s in ['TTJets' , 'DY', 'other']:
        yield_other+=u_float(getYieldFromChain(setup.sample[s][channel]['chain'], cutString = selection_3l,  weight=weight, returnError=True))
        if setup.verbose: print "yield_other %s added, now: %s"%(s, yield_other)
        
      normRegYield = yield_data_3l - yield_other
      if normRegYield.val<0: print "\n !!!Warning!!! \n Negative normalization region yield data: (%s), MC: (%s) \n"%(yield_data_3l, yield_other)

      print  "normRegYield", normRegYield
      return u_float(0., 0.) 
