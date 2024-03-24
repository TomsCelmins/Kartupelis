import tkinter as tk

window = tk.Tk()
window.title("Hello world")
window.geometry("1000x500")

cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.

class Board:
  def __init__(self, start_loc_x, start_loc_y):

    # Contents of the board
    self.board_data = {
      0:["K","A","R","T","U","P","E","L","I","S"],
      1:[],
      2:[],
      3:[],
      4:[],
      5:[],
      6:[],
      7:[],
      8:[],
      9:[],
      10:[],
    }

    # Creation of the boards static data
    self.space = tk.Canvas(width = cell_size*11, height = cell_size*11, highlightthickness=1, highlightbackground="black")
    self.space.place(x = start_loc_x, y = start_loc_y)
    
    y = cell_size
    x = cell_size
    self.space.create_rectangle(cell_size-cell_size,cell_size-cell_size,cell_size,cell_size)
    for key in self.board_data:
      if key != 0:
        self.space.create_rectangle(cell_size-cell_size,y,cell_size,y+cell_size)
        self.space.create_text(cell_size/2,y+cell_size/2, text = f"{key}")
        y += cell_size
      else:
        for element in self.board_data[key]:
          self.space.create_rectangle(x,cell_size-cell_size,x+cell_size,cell_size)
          self.space.create_text(x+cell_size/2,cell_size/2, text = element)
          x += cell_size

board_1 = Board(0, 0)
board_2 = Board(340, 0)

tk.mainloop()