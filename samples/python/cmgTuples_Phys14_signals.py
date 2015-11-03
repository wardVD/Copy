allSignalData=[\
["/data/rschoefbeck/cmgTuples/Phys14_T2tt_lateProcessing/T2tt", "SMS_T2tt_2J_mStop425_mLSP325"], 
["/data/rschoefbeck/cmgTuples/Phys14_T2tt_lateProcessing/T2tt", "SMS_T2tt_2J_mStop500_mLSP325"], 
["/data/rschoefbeck/cmgTuples/Phys14_T2tt_lateProcessing/T2tt", "SMS_T2tt_2J_mStop650_mLSP325"], 
["/data/rschoefbeck/cmgTuples/Phys14_T2tt_lateProcessing/T2tt", "SMS_T2tt_2J_mStop850_mLSP100"], 

]
allSignalStrings = [s[1] for s in allSignalData]
def getSignalSample(dir, signal):
  if signal in allSignalStrings:
    return {\
      "name" : signal,
      "chunkString": signal,
      'dir' : dir,
      'dbsName':signal,
    "rootFileLocation":"treeProducerSusySingleLepton/tree.root",
    "skimAnalyzerDir":"skimAnalyzerCount",
    "treeName":"tree",
    'isData':False,

      }
  else:
    print "Signal",signal,"unknown. Available: ",", ".join(allSignalStrings)

#allSignals=[]
for d,s in allSignalData:
  exec(s+"=getSignalSample('"+d+"','"+s+"')")
#  exec("allSignals.append("+s+")")
