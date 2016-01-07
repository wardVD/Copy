from StopsDilepton.tools.helpers import getYieldFromChain
from math import sqrt
from systematics import SystematicBaseClass
from ufloat import u_add, u_sub, u_mult, u_div
class DataDrivenDYEstimate(SystematicBaseClass):
  def __init__(self, name, cacheDir=None):
    super(DataDrivenDYEstimate, self).__init__(name, cacheDir=cacheDir)
#Concrete implementation of abstract method 'estimate' as defined in Systematic
  def _estimate(self, region, channel, setup):
    weight = setup.weightString()

    #Sum of all channels for 'all'
    if channel=='all':
      res=[ self.cachedEstimate(region, c, setup) for c in ['MuMu', 'EE', 'EMu'] ]
      return {'val':sum([r['val'] for r in res]), 'sigma':sqrt(sum(r['sigma']**2 for r in res))}

    #MC based for 'EMu'
    elif channel=='EMu':
      cut = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.preselection('MC', channel=channel)])
      if setup.verbose: 
        print "Using cut %s and weight %s"%(cut, weight)
      val          = setup.lumi/1000.*getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut, weight=weight)
      valVariance  = setup.lumi/1000.*getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut, weight="("+weight+")**2")
      res = {'val':val, 'sigma':sqrt(valVariance)}
      return res

    #Data driven for EMu and MuMu
    else:
      cut_offZ_1b = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'offZ', nBTags= (1,-1))])
      cut_onZ_1b  = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'onZ',  nBTags= (1,-1))])
      cut_onZ_0b  = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('MC', channel=channel, zWindow = 'onZ',  nBTags= (0,0))])
      cut_data_onZ_0b    = "&&".join([region.cutString(setup.sys['selectionModifier']), setup.selection('Data', channel=channel, zWindow = 'onZ',  nBTags= (0,0))])
  #    R1 = DY-MC (offZ, 1b) / DY-MC (onZ, 1b)
  #    R2 = DY-MC (onZ, 1b) / DY-MC (onZ, 0b) 
  #    DY-est = R1*R2*(Data(2l, onZ, 0b) - EWK(onZ, 0b)) = DY-MC (offZ, 1b) / DY-MC (onZ, 0b) *( Data(2l, onZ, 0b) - EWK(onZ, 0b))
      
      yield_offZ_1b = {'val'   : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_offZ_1b, weight=weight),
                       'sigma' : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_offZ_1b, weight="("+weight+")**2") }
      if setup.verbose: print "yield_offZ_1b %r"%yield_offZ_1b 
#     yield_onZ_1b  = {'val'   : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_onZ_1b,  weight=weight)  
#                      'sigma' : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_onZ_1b,  weight="("+weight+")**2")  
      yield_onZ_0b  = {'val'   : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_onZ_0b,  weight=weight),
                       'sigma' : getYieldFromChain(setup.sample['DY'][channel]['chain'], cutString = cut_onZ_0b,  weight="("+weight+")**2") }
      if setup.verbose: print "yield_onZ_0b %r"%yield_onZ_0b 
      yield_data    = {'val'   : getYieldFromChain(setup.sample['data'][channel]['chain'], cutString = cut_data_onZ_0b,  weight=weight) }
      yield_data['sigma'] = sqrt(yield_data['val'])
      if setup.verbose: print "yield_data %r cut %s weight %s"%(yield_data, cut_data_onZ_0b, weight) 

      #electroweak subtraction
      yield_ewk = {'val':0, 'sigma':0}
      for ewk in ['TTJets' , 'singleTop' , 'TTZ' , 'diBoson', 'triBoson' , 'TTXNoZ' , 'WJetsToLNu_HT']:
        yield_ewk=u_add( yield_ewk, 
          {'val':  getYieldFromChain(setup.sample[ewk][channel]['chain'], cutString = cut_onZ_0b,  weight=weight),
           'sigma':getYieldFromChain(setup.sample[ewk][channel]['chain'], cutString = cut_onZ_0b,  weight="("+weight+")**2"),
          }
        )
        if setup.verbose: print "yield_ewk %s added, now: %r"%(ewk, yield_ewk)
      
      normRegYield = u_sub(yield_data, yield_ewk)
      if normRegYield['val']<0: print "Warning! negative normalization region yield data: %r MC %r"%(yield_data, yield_ewk)
      
      mcRatio = u_div(yield_offZ_1b, yield_onZ_0b)
      res = u_mult(mcRatio, normRegYield)
 
      return res
