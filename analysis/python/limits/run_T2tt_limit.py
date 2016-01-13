import os
from StopsDilepton.analysis.setup import setup, regions, estimates, allChannels
setup.verbose = False
from StopsDilepton.samples.cmgTuples_FastSimT2tt_mAODv2_25ns_1l_postProcessed import *
from StopsDilepton.analysis.MCBasedEstimate import MCBasedEstimate
from StopsDilepton.analysis.u_float import u_float
from math import sqrt
##https://twiki.cern.ch/twiki/bin/viewauth/CMS/SUSYSignalSystematicsRun2
from StopsDilepton.tools.btagEfficiency import btagWeightNames_FS_1b, btagWeightNames_1b
from StopsDilepton.tools.localInfo import releaseLocation71XC, analysisOutputDir 
from StopsDilepton.tools.cardFileWriter import cardFileWriter
c = cardFileWriter.cardFileWriter()
c.releaseLocation = releaseLocation71XC

T2tt_exp      = ROOT.TH2F("T2tt_exp", "T2tt_exp", 1000/25, 0, 1000, 1000/25, 0, 1000)
T2tt_exp_down = T2tt_exp.Clone("T2tt_exp_down")
T2tt_exp_up   = T2tt_exp.Clone("T2tt_exp_up")
T2tt_obs      = T2tt_exp.Clone("T2tt_obs")

#for s in [T2tt_400_0]:
for s in signals_T2tt:
  counter=0
  c.reset()
  c.addUncertainty('PU', 'lnN')
  c.addUncertainty('topPt', 'lnN')
  c.addUncertainty('JEC', 'lnN')
  c.addUncertainty('JER', 'lnN')
  c.addUncertainty('SFb', 'lnN')
  c.addUncertainty('SFl', 'lnN')
  c.addUncertainty('SFFS', 'lnN')
  c.addUncertainty('leptonSF', 'lnN')

  eSignal = MCBasedEstimate(name=s['name'],    sample={channel:s for channel in allChannels}, cacheDir=setup.cacheDir )
  outfileName = os.path.join(setup.analysisOutputDir,  setup.prefix(), 'cardFiles', s['name']+'.txt')
  if not os.path.exists(outfileName):
    for r in regions:
      for channel in ['all']:
        niceName = ' '.join([channel, r.__str__()])
        binname = 'Bin'+str(counter)
        counter += 1
        total_exp_bkg = 0
        c.addBin(binname, [e.name for e in estimates], niceName)
        for e in estimates:
          expected = e.cachedEstimate(r, channel, setup)
          total_exp_bkg += expected.val
          c.specifyExpectation(binname, e.name, expected.val )

          if expected.val>0:

            #PU bkg
            c.specifyUncertainty('PU', binname, e.name, 1 + e.PUSystematic(r, channel, setup).val )

            #JEC bkg
            c.specifyUncertainty('JEC', binname, e.name, 1 + e.JECSystematic(r, channel, setup).val )

            #JER bkg
            c.specifyUncertainty('JER', binname, e.name, 1 + e.JERSystematic(r, channel, setup).val )

            #topPt reweighting
            c.specifyUncertainty('topPt', binname, e.name, 1 + e.topPtSystematic(r, channel, setup).val )

            #b-tagging SF
            c.specifyUncertainty('SFb', binname, e.name, 1 + e.btaggingSFbSystematic(r, channel, setup).val )
            c.specifyUncertainty('SFl', binname, e.name, 1 + e.btaggingSFlSystematic(r, channel, setup).val )

            #MC bkg stat (some condition to neglect the smaller ones?)
            uname = 'Stat_'+binname+'_'+e.name
            c.addUncertainty(uname, 'lnN') 
            c.specifyUncertainty('Stat_'+binname+'_'+e.name, binname, e.name, 1+expected.sigma/expected.val )

  #      assert total_exp_bkg>=0, "Total background is negative. Don't know what to do."

        c.specifyObservation(binname, int(total_exp_bkg) )

        #signal
        e = eSignal
        signal = e.cachedEstimate(r, channel, setup.sysClone({'reweight':['reweightLeptonFastSimSF']}))

        c.specifyExpectation(binname, 'signal', signal.val )

        if signal.val>0:

          #PU signal
          c.specifyUncertainty('PU', binname, 'signal', 1 + e.PUSystematic(r, channel, setup).val )

          #JEC signal
          c.specifyUncertainty('JEC', binname, 'signal', 1 + e.JECSystematic(r, channel, setup).val )

          #JER signal
          c.specifyUncertainty('JER', binname, 'signal', 1 + e.JERSystematic(r, channel, setup).val )

          #lepton FastSim SF uncertainty
          c.specifyUncertainty('leptonSF', binname, 'signal', 1 + e.leptonFSSystematic(r, channel, setup).val )

          #b-tagging SF (including FastSim SF)
          c.specifyUncertainty('SFb', binname, 'signal', 1 + e.btaggingSFbSystematic(r, channel, setup).val )
          c.specifyUncertainty('SFl', binname, 'signal', 1 + e.btaggingSFlSystematic(r, channel, setup).val )
          c.specifyUncertainty('SFFS', binname, 'signal', 1 + e.btaggingSFFSSystematic(r, channel, setup).val )

          #signal MC stat added in quadrature with PDF uncertainty: 10% uncorrelated
          uname = 'Stat_'+binname+'_signal'
          c.addUncertainty(uname, 'lnN') 
          c.specifyUncertainty(uname, binname, 'signal', 1 + sqrt(0.1**2 + signal.sigma/signal.val) )

        if signal.val<=0.01 or total_exp_bkg<=0 or (total_exp_bkg>10 and signal.val/total_exp_bkg<0.05):
          print "Muting bin %s. Total sig: %f, total bkg: %f, s/b %f"%(binname, signal.val, total_exp_bkg, signal.val/total_exp_bkg)
          c.muted[binname] = True 
    #
    c.addUncertainty('Lumi', 'lnN')
    c.specifyFlatUncertainty('Lumi', 1.046)
    outfileName = c.writeToFile(outfileName)
  else:
    print "File %s found. Reusing."%outfileName

  res = c.calcLimit(outfileName)
  mStop, mNeu = s['mStop'], s['mNeu']
#    print "Result: mStop %i mNeu %i obs %5.3f exp %5.3f -1sigma %5.3f +1sigma %5.3f"%(mStop, mNeu, res['-1.000'], res['0.500'], res['0.160'], res['0.840'])
  try:
    T2tt_exp      .Fill(mStop, mNeu, res['0.500'])
  except:
    print "Something failed."
  try:
    T2tt_exp_down .Fill(mStop, mNeu, res['0.160'])
  except:
    print "Something failed."
  try:
    T2tt_exp_up   .Fill(mStop, mNeu, res['0.840'])
  except:
    print "Something failed."
  try:
    T2tt_obs      .Fill(mStop, mNeu, res['-1.000'])
  except:
    print "Something failed."

ofile = os.path.join(os.path.join(analysisOutputDir, setup.prefix(), 'limits', 'T2tt.root'))
outfile = ROOT.TFile(ofile, "recreate")
T2tt_exp      .Write()
T2tt_exp_down .Write() 
T2tt_exp_up   .Write() 
T2tt_obs      .Write() 
outfile.Close()
print "Written %s"%ofile
