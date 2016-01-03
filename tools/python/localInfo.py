import os
if os.environ['USER'] in ['wvandrie']:
  #plotDir = "/afs/cern.ch/user/w/wvandrie/www/Stops/"
  plotDir = "/user/wvandrie/public_html/"
<<<<<<< HEAD
  #dataDir = "/afs/cern.ch/work/w/wvandrie/public/STOPS/ANALYSIS_new2/CMSSW_7_4_12_patch4/src/StopsDilepton/samplesCopyWard_Spring15_new/"
  #dataDir = "/afs/cern.ch/work/w/wvandrie/public/STOPS/ANALYSIS_new2/CMSSW_7_4_12_patch4/src/StopsDilepton/samplesCopyWard_Spring15_mAOD/"
  dataDir = "/user/wvandrie/STOPS/ANALYSIS/CMSSW_7_4_12_patch4/src/mAODv2_tiny/"
  #dataDir = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/postProcessed_mAODv2/dilep/"
  analysisOutputDir = '.' #Path to analysis results
=======
  dataDir = "/user/wvandrie/STOPS/ANALYSIS/CMSSW_7_4_12_patch4/src/tuples_2015_12_2/dilepTiny/"
>>>>>>> c2099514cf17f7f9f64ea9c4711aa02c99f2c962
if os.environ['USER'] in ['didar']:
  plotDir = "."
  dataDir = "~/eos/cms/store/cmst3/group/susy/schoef/postProcessed_Phys14V3_diLep" #needs EOS mount on lxplus at ~/eos 
if os.environ['USER'] in ['schoef', 'rschoefbeck', 'schoefbeck']:
  plotDir = "/afs/hephy.at/user/r/rschoefbeck/www/"
  dataDir = "/afs/hephy.at/data/rschoefbeck01/cmgTuples/postProcessed_mAODv2/dilep" 
  analysisOutputDir = '/afs/hephy.at/data/rschoefbeck01/StopsDilepton/results' #Path to analysis results
if os.environ['USER'] in ['sigamani']:
  plotDir = "/afs/cern.ch/user/s/sigamani/www/php-plots/2LeptonStops13TeV/"
  dataDir = "/afs/cern.ch/work/w/wvandrie/public/STOPS/ANALYSIS_new2/CMSSW_7_4_12_patch4/src/StopsDilepton/samplesCopyWard_Spring15_new/"
if os.environ['USER'] in ['nbulte']:
  plotDir = "/afs/cern.ch/user/n/nbulte/www/plots/"
  dataDir = "/afs/cern.ch/work/w/wvandrie/public/STOPS/ANALYSIS_new2/CMSSW_7_4_12_patch4/src/StopsDilepton/samplesCopyWard_Spring15_new/"
  analysisOutputDir = '.' #Path to analysis results
