from StopsDilepton.tools.objectSelection import getGenPartsAll
from StopsDilepton.tools.pdgToName import pdgToName
def getDaughters(particle_, genParts):
  if particle_['daughterIndex2']==-1: return [genParts[particle_['daughterIndex1']]]
  return [genParts[particle_['daughterIndex1']],genParts[particle_['daughterIndex2']] ]

def descendDecay(particle_, genParts):
  daughters = getDaughters(particle_, genParts)
  particles_ = filter(lambda p:abs(p['pdgId'])==abs(particle_['pdgId']), daughters)
  assert len(particles_)<=1, "Found more than one particle with same pdgId %i in decay chain %r -> impossible."%(particle_['pdgId'], particles_)
  if len(particles_)>0:
    if particles_[0]==particle_:return particle_
    return descendDecay(particles_[0], genParts)
  return particle_

def decaysTo(particle_, pdgId, genParts):
  daughters = getDaughters(particle_, genParts)
  if len(daughters)==0 or (len(daughters)==1 and daughters[0]==particle_): return abs(particle_['pdgId'])==pdgId
  return any([decaysTo(d, pdgId, genParts) for d in daughters])

#def printDecay(particle_, genParts, prefix=""):
#  daughters = getDaughters(particle_, genParts)
#  if particle_['status']<=2: print prefix+"%s (status: %2i, n-daughters: %3i) pt: %6.2f eta: %6.2f phi: %6.2f"\
#      %(pdgToName[particle_['pdgId']].ljust(10), particle_['status'], len(daughters), particle_['pt'], particle_['eta'], particle_['phi'])
#  if len(daughters)==0 or (len(daughters)==1 and daughters[0]==particle_):
#    return
#  else:
#    for p in daughters:
#      printDecay(p, genParts, prefix="  "+prefix)
      

  
