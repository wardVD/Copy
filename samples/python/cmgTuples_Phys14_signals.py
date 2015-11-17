import ROOT

allSignalStrings=[\
"SMS_T2tt_2J_mStop425_mLSP325",
"SMS_T2tt_2J_mStop500_mLSP325",
"SMS_T2tt_2J_mStop650_mLSP325",
"SMS_T2tt_2J_mStop850_mLSP100",
]

def getSignalSample(signal):
  if signal in allSignalStrings:
    return {
      "name" : signal,
      'dir' : dir,
      #'dir' : "/afs/cern.ch/work/w/wvandrie/public/STOPS/ANALYSIS/CMSSW_7_4_7_patch1/src/StopsDilepton/samplesCopyWard_Phys14/",
      'bins':[signal]}
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

allSignals=[]
for s in allSignalStrings:
  sm = getSignalSample(s)
  exec(s+"=sm")
  exec("allSignals.append(s)")

SMS_T2tt_2J_mStop425_mLSP325['color'] = ROOT.kRed
SMS_T2tt_2J_mStop500_mLSP325['color'] = ROOT.kBlue
SMS_T2tt_2J_mStop650_mLSP325['color'] = ROOT.kGreen
SMS_T2tt_2J_mStop850_mLSP100['color'] = ROOT.kMagenta
