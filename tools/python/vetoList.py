class vetoList:
  def __init__(self, PDName, suffix='_Nov14', baseDir='/afs/hephy.at/data/rschoefbeck01/cmgTuples/vetoLists/Run2015D/', verbose=False):
    self.filteredEvents=[]
    import tarfile
    import os, sys
    filename = os.path.join(baseDir,PDName+suffix+'.tar.gz')
    assert os.path.exists(filename), "File not found for PD %s.  Was looking for %s"%(PDName, filename)
    tar = tarfile.open(filename, 'r:gz')
    if verbose: print "[vetoList] Loaded %s"%filename
    for member in tar.getmembers():
      if verbose: print "[vetoList] Now looping over %s"%member.name
      f=tar.extractfile(member)
      count=0
      for x in f.read().split('\n'):
          try:
            self.filteredEvents.append( (int(i) for i in x.split(":")) )
            count+=1
          except:
            if verbose: print "Skipping line %s in %s in %s"%(x, member.name, filename)
      if verbose: print "[vetoList] Loaded %i events from %s in %s"%(count, member.name, filename)
    print "[vetoList] Loaded in total %i events from %s"%(len(self.filteredEvents), filename)
