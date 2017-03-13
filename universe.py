import nodes
import spring_model
import display
import cProfile

class app(object):
  def __init__(self):
    
    self.x = 600
    self.y = 600
    
    self.all_nodes = nodes.nodes('datadump/universeDataDx.db','systems')
    
    #self.nodes = self.all_nodes.select(20000020,20000) # Kimotoro
    self.nodes = self.all_nodes.select(30000142,2000000) # Jita
    #self.nodes = self.all_nodes.nodes.values()

    self.spring_model = spring_model.spring_model(self.nodes)
    self.spring_model.scale_nodes()
    
    #cProfile.runctx("self.spring_model.steps(1000)",globals(),locals(),sort='time')
    #exit(1)
    
    self.display = display.display(self.x, self.y, self.nodes, self.spring_model.step)

if __name__ == '__main__':
  app = app()


