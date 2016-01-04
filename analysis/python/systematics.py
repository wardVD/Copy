jmeVariations = ["JER", "JERUp", "JERDown", "JECUp", "JECDown"]
jmeSystematics = [{'weight':None, 'reweight':None, 'selectionModifier':j} for j in jmeVariations]

btagVariationWeights = [
'reweightBTag_up_lfstats1',
'reweightBTag_up_lfstats2',
'reweightBTag_up_hfstats1',
'reweightBTag_up_hfstats2',
'reweightBTag_down_lfstats2',
'reweightBTag_down_lfstats1',
'reweightBTag_down_cferr1',
'reweightBTag_down_cferr2',
'reweightBTag_down_hf',
'reweightBTag_central',
'reweightBTag_up_lf',
'reweightBTag_down_lf',
'reweightBTag_up_cferr2',
'reweightBTag_up_cferr1',
'reweightBTag_up_hf',
'reweightBTag_down_hfstats2',
'reweightBTag_down_hfstats1',
#'reweightBTag_up_jes',
#'reweightBTag_down_jes',
]
btagSystematics = [{'weight':None, 'reweight':w, 'selectionModifier':None} for w in btagVariationWeights]

#weightPUUp
#weightPUDown
#reweightTopPt
#
