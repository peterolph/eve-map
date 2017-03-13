from Tkinter import *

def create_blob(w,bbox,fill):
  x1,y1,x2,y2 = bbox
  h = y2 - y1
  h2 = h / 2
  items = (
    # Fill in bg colour
    w.create_arc(x1-h2,y1,x1+h2,y2,style=PIESLICE,start=90,extent=180,fill=fill,outline=''),
    w.create_arc(x2-h2,y1,x2+h2,y2,style=PIESLICE,start=270,extent=180,fill=fill,outline=''),
    w.create_rectangle(x1,y1,x2,y2,fill=fill,outline=''),
    # Add outlines
    w.create_arc(x1-h2,y1,x1+h2,y2,style=ARC,start=90,extent=180),
    w.create_arc(x2-h2,y1,x2+h2,y2,style=ARC,start=270,extent=180),
    w.create_line(x1,y1,x2,y1),
    w.create_line(x1,y2,x2,y2)
  )
  return items

def create_text_blob(w,pos,text,fill):
  text = w.create_text(pos,text=text)
  items = w.create_blob(w.bbox(text),fill=fill)
  w.tag_raise(text)
  return (text, items)

Canvas.create_blob = create_blob
Canvas.create_text_blob = create_text_blob
