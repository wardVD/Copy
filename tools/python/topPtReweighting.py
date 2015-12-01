from math import exp, sqrt

#def getUnscaledTopPtReweightungFunction(a,b):
#  def f(pt1):
#    return exp(a+b*pt1)
#  return f

def getUnscaledTopPairPtReweightungFunction(a,b):
  def f(pt1,pt2):
    return sqrt(exp(2*a+b*(pt1+pt2)))
  return f

#https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopPtReweighting
def getTopPtDrawString(a=0.148, b= -0.00129): 
#  assert b < 0, "b is not a negative number"
  return "sqrt(exp(Sum$(("+str(a)+"+("+str(b)+")*genPartAll_pt)*(abs(genPartAll_pdgId)==6&&genPartAll_nDaughters==2&&genPartAll_status==62&&genPartAll_pt<=400))))"

