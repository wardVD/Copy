from StopsDilepton.tools.helpers import getObjFromFile
#Define a functor that returns a reweighting-function according to the era
def getReweightingFunction(data="PU_2100_XSecCentral", mc="Spring15"):
  fileNameData = "$CMSSW_BASE/src/StopsDilepton/tools/python/puReweightingData/"+data+'.root'
  histoData = getObjFromFile(fileNameData, 'pileup')
  histoData.Scale(1./histoData.Integral())
  print "[puReweighting] Loaded 'pileup' from data file %s"%(fileNameData)
  if mc=='Spring15':
    from StopsDilepton.tools.puReweightingData.spring15MCProfile import mcProfile
    mcProfile.Scale(1./mcProfile.Integral()) 
    print "[puReweighting] Loaded mcProfile from $CMSSW_BASE/src/StopsDilepton/tools/python/puReweightingData/spring15MCProfile.py"
  reweightingHisto = histoData.Clone('_'.join(['reweightingHisto', data, mc])) 
  reweightingHisto.Divide(mcProfile) 
  def reweightingFunc(nvtx):
    return reweightingHisto.GetBinContent(reweightingHisto.FindBin(nvtx))

  return reweightingFunc
