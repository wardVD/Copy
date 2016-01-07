from math import sqrt
def u_add(a,b):
  return {'val':a['val']+b['val'], 'sigma':sqrt(a['sigma']**2+b['sigma']**2)}
def u_sub(a,b):
  return {'val':a['val']-b['val'], 'sigma':sqrt(a['sigma']**2+b['sigma']**2)}
def u_mult(a,b):
  return {'val':a['val']*b['val'], 'sigma':sqrt((a['sigma']*b['val'])**2 + (b['sigma']*a['val'])**2)}
def u_div(a,b):
  return {'val':a['val']/b['val'], 'sigma':1./b['val']*sqrt( (a['sigma'])**2 + (b['sigma']/b['val'])**2) }
#class yield:
#  def __init__(self, val=0, sigma=0):
#    self.val=0
#    self.sigma=0
#  
