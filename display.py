import tkinter_wrap as tk
import time

def interpolate(offset,array):
  """Interpolate a 0-1 offset across an array of value"""
  if offset <= 0:
    return array[0]
  if offset >= 1:
    return array[-1]
  scale = len(array) - 1
  scaled_offset = offset * scale
  integer_part = int(scaled_offset)
  decimal_part = scaled_offset - integer_part
  return array[integer_part]*(1-decimal_part) + array[integer_part+1]*decimal_part

class display(object):
  def __init__(self, x, y, nodes, stepfunc):
    
    self.x = x
    self.y = y
    self.nodes = nodes
    self.stepfunc = stepfunc
    
    self.root = tk.Tk()
    self.canvas = tk.Canvas(self.root, width=self.x, height=self.y)
    self.canvas.pack()
    self.labels = {}
    self.lines = []
    
    self.run = True
    self.canvas.bind('<Button-1>', self.mouse_down)
    self.canvas.bind('<B1-Motion>', self.mouse_drag)
    self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
    self.root.bind('<Return>',self.toggle)
    self.root.bind('p',self.write_file)
    self.mouse = (0,0)
    self.target = None
    
    self.draw()
    self.root.after(0,self.update)
    
    self.root.mainloop()
      
  def draw(self):
    
    class line(object):
      def __init__(self,ID,a,b,visible):
        self.ID = ID
        self.a = a
        self.b = b
        self.visible = visible
    
    for node in self.nodes:
      node.visible = True
    
    count = 0
    for node in self.nodes:
      node.lines = []
      for link in node.links:
          count += 1
          ID = self.canvas.create_line(node.pos, link.pos)
          self.lines.append(line(ID,node,link,True))
    print count
      
    for node in self.nodes:
      red   = interpolate(node.value,[255,255,0])
      green = interpolate(node.value,[0,255,255])
      blue = 0
      fill = '#%02x%02x%02x' % (red, green, blue)
      (node.label, node.blob) = self.canvas.create_text_blob(node.pos, text=node.name, fill=fill)
      self.labels[node.label] = node
    
    self.step_timer = self.canvas.create_text((20,15),text='0',fill='red')
    self.draw_timer = self.canvas.create_text((20,30),text='0',fill='red')
  
  def update(self):
    
    start = time.clock()
    
    if self.run:
      self.stepfunc()
      
    middle = time.clock()
    
    if self.target:
      self.target.pos = self.mouse
    self.redraw()
    
    end = time.clock()
    
    self.canvas.itemconfig(self.step_timer, text=int((middle-start)*1000))
    self.canvas.itemconfig(self.draw_timer, text=int((end-middle)*1000))
    
    self.canvas.after(10,self.update)

  def redraw(self):
    
    for node in self.nodes:
      x,y = node.pos
      should_be_visible = (x > -30 and x < self.x+30 and y > -30 and y < self.y+30)
      if should_be_visible != node.visible:
        if node.visible:
          self.canvas.itemconfig(node.label,state=tk.HIDDEN)
          for item in node.blob:
            self.canvas.itemconfig(item,state=tk.HIDDEN)
        else:
          self.canvas.itemconfig(node.label,state=tk.NORMAL)
          for item in node.blob:
            self.canvas.itemconfig(item,state=tk.NORMAL)
        node.visible = not node.visible  
      if node.visible:
        old = self.canvas.coords(node.label)
        new = node.pos
        diff = (x-old[0], y-old[1])
        self.canvas.coords(node.label,node.pos)
        for item in node.blob:
          self.canvas.move(item,diff[0],diff[1])
    
    for line in self.lines:
      should_be_visible = (line.a.visible or line.b.visible)
      if should_be_visible != line.visible:
        if line.visible:
          self.canvas.itemconfig(line.ID,state=tk.HIDDEN)
        else:
          self.canvas.itemconfig(line.ID,state=tk.NORMAL)
        line.visible = not line.visible
      if line.visible:
        self.canvas.coords(line.ID,line.a.pos[0],line.a.pos[1],line.b.pos[0],line.b.pos[1])

  def mouse_down(self,event):
    self.mouse = (event.x, event.y)
    w = self.canvas.find_withtag(tk.CURRENT)
    if not w or w[0] not in self.labels:
      self.target = None
    else:
      self.target = self.labels[w[0]]
  
  def mouse_drag(self,event):
    if not self.target:
      move = (event.x - self.mouse[0], event.y - self.mouse[1])
      for node in self.nodes:
        node.pos = (node.pos[0] + move[0], node.pos[1] + move[1])
    self.mouse = (event.x, event.y)
  
  def mouse_up(self,event):
    self.target = None

  def write_file(self,event):
    bbox = self.canvas.bbox(tk.ALL)
    self.canvas.postscript(file='universe.ps', x=bbox[0], y=bbox[1], width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])
  
  def toggle(self,event):
    self.run = not self.run

