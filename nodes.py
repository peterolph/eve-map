import sqlite3

class nodes(object):

  class node(object):
    def __init__(self,ID,name,x,y,value):
      self.ID = ID
      self.name = name
      self.pos = (x,y)
      self.value = value
    def __str__(self):
      return "%s %s (%g %g)" % (self.ID, self.name, self.pos[0], self.pos[1]  )
    def __repr__(self):
      return str(self)
  
  def __init__(self,database,select='constellations'):

    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    main_query = {'constellations':
                    '''SELECT
                         c.constellationID,
                         c.constellationName,
                         c.x,
                         c.z,
                         AVG(s.security)
                       FROM mapConstellations AS c
                         JOIN mapSolarSystems AS s
                         ON c.constellationID == s.constellationID
                       GROUP BY s.constellationID''',
                  
                  'systems':
                    '''SELECT
                         solarSystemID,
                         solarSystemName,
                         x,
                         z,
                         security
                       FROM mapSolarSystems
                    '''}

    link_query = {'constellations':
                    '''SELECT fromConstellationID,toConstellationID
                       FROM mapConstellationJumps''',
                  
                  'systems':
                    '''SELECT fromSolarSystemID,toSolarSystemID
                       FROM mapSolarSystemJumps'''}

    results = cursor.execute(main_query[select]).fetchall()
    # transform z to -y to account for EVE coords
    self.nodes = {ID:self.node(ID,name,x,-y,value) for ID,name,x,y,value in results}

    for node in self.nodes.values():
      node.links = []
    results = cursor.execute(link_query[select]).fetchall()
    for result in results:
      from_node, to_node = [self.nodes[ID] for ID in result]
      if from_node not in to_node.links:
        from_node.links.append(to_node)

  def select(self,start,number):
    queue = [self.nodes[start]]
    nodeset = set(queue)
    for node in queue:
      for link in node.links:
        if link not in nodeset:
          queue.append(link)
          nodeset.add(link)
      if len(queue) >= number:
        queue = queue[:number]
        nodeset = set(queue)
        break
    for node in queue:
      node.links = [link for link in node.links if link in nodeset]
    return queue
            
            
