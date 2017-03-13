import vec2
import math
import collections

class spring_model(object):
  def __init__(self,nodes):
  
    self.pull_length = 200.0
    self.push_length =  80.0
    self.pull        =  -0.05
    self.push        =   0.6
    
    self.damping     =   0.7
    
    self.nodes = nodes
    for node in self.nodes:
      node.vel = (0,0)

  def get_bounds(self):
    x = [node.pos[0] for node in self.nodes]
    y = [node.pos[1] for node in self.nodes]
    return (min(x), max(x), min(y), max(y))
  
  def scale_nodes(self):
    
    xmin,xmax,ymin,ymax = bounds = self.get_bounds()
    
    span = (xmax - xmin, ymax - ymin)
    mid  = ((xmax+xmin)/2, (ymax+ymin)/2)
    scale = math.sqrt(len(self.nodes)) * self.push_length * 1.5
    
    uniform = [scale / span[i] for i in range(2)]
    
    for node in self.nodes:
      node.pos = [(node.pos[i]-mid[i])*uniform[i] for i in range(2)]
  
  def build_grid(self):
    self.grid = collections.defaultdict(list)
    for node in self.nodes:
      index = tuple([int(node.pos[i]/self.push_length) for i in (0,1)])
      node.index = index
      self.grid[index].append(node)
  
  def reset_nodes(self):
    for node in self.nodes:
      node.done = False
  
  def step(self):
    
    self.reset_nodes()
    self.build_grid()
    
    pull = self.pull
    push = self.push
    pull_length = self.pull_length
    push_length = self.push_length
    damping = self.damping
    
    for node in self.nodes:
      
      node.done = True
      
      # Apply pull between neighbours
      for link in node.links:
        if not link.done:
          nx,ny = node.pos
          lx,ly = link.pos
          dx = nx - lx
          dy = ny - ly
          ax = dx * pull
          ay = dy * pull
          node.vel = (node.vel[0] + ax, node.vel[1] + ay)
          link.vel = (link.vel[0] - ax, link.vel[1] - ay)
      
      # Apply push between all nodes
      for x in (-1,0,1):
        for y in (-1,0,1):
          index = (node.index[0]+x,node.index[1]+y)
          for other in self.grid[index]:
            if not other.done:
              nx,ny = node.pos
              ox,oy = other.pos
              dx = nx - ox
              dy = ny - oy
              if dx > -push_length and dx < push_length and dy > -push_length and dy < push_length:
                length = math.sqrt(dx*dx + dy*dy)
                if length < push_length:
                  factor = push_length/length - 1
                  ax = dx * push * factor
                  ay = dy * push * factor
                  node.vel = (node.vel[0] + ax, node.vel[1] + ay)
                  other.vel = (other.vel[0] - ax, other.vel[1] - ay)
    
    # Update position
    for node in self.nodes:
      node.vel = (node.vel[0] * damping, node.vel[1] * damping)
      node.pos = (node.pos[0] + node.vel[0], node.pos[1] + node.vel[1])

  def steps(self,steps):
    for _ in xrange(steps):
      self.step()
