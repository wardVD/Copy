import pickle

class cache:
  def __init__(self, file_name, verbosity=0):
    self.verbosity=verbosity
    self.file_name=file_name
    try:
      self._cache = pickle.load(open(file_name, 'r'))
      if self.verbosity>=1: print "Loaded cache file %s"%file_name
    except (IOError, ValueError):
      if self.verbosity>=2: print "File %s not found or could not be loaded. Starting new cache."%file_name
      self._cache = {}

  def contains (self, key):
    return key in self._cache

  def get(self, key):
    return self._cache[key]
 
  def add(self, key, val):
    self._cache[key] = val 
    if self.verbosity>=2: print "Writing new result %r to key %r in  cache file %s"%(val, key, self.file_name)
    pickle.dump(self._cache, open(self.file_name, 'w'))
    return self._cache[key]

