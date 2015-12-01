from math import exp

def getUnscaledTopPtReweightungFunction(a,b):
  def f(pt1):
    return exp(a+b*pt1)
  return f

def getUnscaledTopPairPtReweightungFunction(a,b):
  def f(pt1,pt2):
    return exp(2*a+b*(pt1+pt2))
  return f

def getTopPtDrawString(a,b):
#  assert b < 0, "b is not a negative number"
  return "exp(Sum$(("+str(a)+"+("+str(b)+")*genPartAll_pt)*(abs(genPartAll_pdgId)==6&&genPartAll_nDaughters==2&&genPartAll_status==62)))"
##### c.Draw(getTopPtDrawString(a,b)+">>h")
##### average=ROOT.h.GetMean()
##### topPairPtWeight = getUnscaledTopPairPtReweightungFunction(a,b)(pt1,pt2)/average
