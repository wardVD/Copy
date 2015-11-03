# Stops-dilepton 
```
cmsrel CMSSW_7_4_12_patch4
cd CMSSW_7_4_12_patch4/src
cmsenv
git cms-init
git clone https://github.com/GhentAnalysis/StopsDilepton
scram b -j9
```
## To run: 
```
cd StopsDilepton/plots/plotsWard/
python plot.py
```
# for CMG
see here:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/CMGToolsReleasesExperimental#Git_MiniAOD_release_for_Summer_2

minimal fetch of central and ghent fork:
```
git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git  -f -t CMGTools-from-CMSSW_7_4_12 -t heppy_74X
git fetch cmg-central
git remote add cmg-ghent git@github.com:GhentAnalysis/cmg-cmssw.git -f -t CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2
git fetch cmg-ghent
```
sparse checkout (extra echos can be omitted)
```
cp /afs/cern.ch/user/c/cmgtools/public/sparse-checkout_7412_heppy .git/info/sparse-checkout
echo "/CMGTools/ObjectStudies/" >> .git/info/sparse-checkout
echo "/JetMETCorrections/Type1MET/" >> .git/info/sparse-checkout
echo "/PhysicsTools/PatAlgos/" >> .git/info/sparse-checkout
echo "/PhysicsTools/PatUtils/" >> .git/info/sparse-checkout
git read-tree -mu HEAD
```
configure local branch
```
git checkout -b CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2 cmg-ghent/CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2
git push -u cmg-ghent CMGTools-from-CMSSW_7_4_12_LocalDevelopmentsPass2
```
