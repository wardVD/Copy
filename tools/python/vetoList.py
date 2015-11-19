class vetoList:
  def __init__(self, filename, verbose=False):
    self.events=set([])
    import tarfile
    import os, sys
#    filename = os.path.join(baseDir,PDName+suffix+'.tar.gz')
    self.filename=filename
    assert os.path.exists(filename), "[vetoList] File %s not found."%(filename)
    tar = tarfile.open(filename, 'r:gz')
    if verbose: print "[vetoList] Loaded %s"%filename
    for member in tar.getmembers():
      if verbose: print "[vetoList] Now looping over %s"%member.name
      f=tar.extractfile(member)
      count=0
      for x in f.read().split('\n'):
          try:
            self.events.add( tuple([int(i) for i in x.split(":")]) )
            count+=1
          except:
            if verbose: print "Skipping line %s in %s in %s"%(x, member.name, filename)
      if verbose: print "[vetoList] Loaded %i events from %s in %s"%(count, member.name, filename)
    print "[vetoList] Loaded in total %i events from %s"%(len(self.events), filename)
