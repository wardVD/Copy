allowedVars = ["dl_mt2ll", "dl_mt2blbl", "dl_mt2bb"]
class region:
  def __init__(self, var, val):
    assert type(val)==type(()) and len(val)==2, "Don't know how to make region with this val argument: %r."%val
#    assert type(var)==type(""), "Argument 'var' must be string"
    assert var in allowedVars, "Use only these variables: %r"%allowedVars
    assert val[0]>=0, "Need nonzero lower threshold."
    self.vals = {var:val}
  def variables(self):
    return self.vals.keys()
  def __iadd__(self, otherRegion):
    if not type(self)==type(otherRegion): raise TypeError("Can't add this type to a region %r"%type(otherRegion))
    for v in otherRegion.vals.keys():
      assert v not in self.vals.keys(), "Can't add regions, variable %s in both summands!"%v
    self.vals.update(otherRegion.vals)
    return self
  def __add__(self, otherRegion):
    if not type(self)==type(otherRegion): raise TypeError("Can't add this type to a region %r"%type(otherRegion))
    for v in otherRegion.vals.keys():
      assert v not in self.variables(), "Can't add regions, variable %s in both summands!"%v
    import copy
    res=copy.deepcopy(self)
    res.vals.update(otherRegion.vals)
    return res
  def cutString(self, sys=None):
    res=[]
    for var in self.variables():
      svar = var if not sys else var+"_"+sys
      s1=svar+">="+str(self.vals[var][0])
      if self.vals[var][1]>0: s1+="&&"+svar+"<"+str(self.vals[var][1])
      res.append(s1)
    return "&&".join(res)
  def __str__(self):
    return self.cutString()
  def __repr__(self):
#    return self.cutString()
    return "+".join([ "region('%s', %r)"%(v, self.vals[v]) for v in self.variables()])
  def __hash__(self):
    return hash(repr(self))
