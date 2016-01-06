export PATH=$HOME/.local/bin:/afs/cern.ch/cms/lumi/brilconda-1.0.3/bin:$PATH
for x in `ls /afs/hephy.at/data/rschoefbeck01/cmgTuples/postProcessed_mAODv2_fix/dilepTiny/*/*.json`; do echo $x; brilcalc lumi -u /fb -i $x; done
