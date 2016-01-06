#!/bin/sh
pileupCalc.py -i DoubleMuon_2100.json --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 69000 --maxPileupBin 50 --numPileupBins 50 PU_2100_XSecCentral.root
pileupCalc.py -i DoubleMuon_2100.json --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 72450 --maxPileupBin 50 --numPileupBins 50 PU_2100_XSecUp.root
pileupCalc.py -i DoubleMuon_2100.json --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 65550 --maxPileupBin 50 --numPileupBins 50 PU_2100_XSecDown.root
