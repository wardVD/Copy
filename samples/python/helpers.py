def getSubDir(dataset):
  import re
  m=re.match("\/(.*)\/(.*)\/(.*)",dataset)
  if not m :
    print "NO GOOD DATASET"
    return
  sample=m.group(1)+"_"+m.group(2)
  return sample
