import math

def vadd(a,b):
  return (a[0]+b[0],a[1]+b[1])

def vneg(a):
  return (-a[0],-a[1])

def vsub(a,b):
  return (a[0]-b[0],a[1]-b[1])

def vmul(a,v):
  return (a[0]*v,a[1]*v)

def vdiv(a,b):
  return (a[0]/v, a[1]/v)

def vlength(a):
  return math.sqrt(a[0]*a[0] + a[1]*a[1])

def clamp(a,minimum,maximum):
  return max(minimum,min(maximum,a))

def vclamp(a,nw,se):
  return [clamp(a[0],nw[0],se[0]),
          clamp(a[1],nw[1],se[1])]
