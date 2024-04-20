import tkinter as tk

window = tk.Tk()
window.geometry("1000x500")

class Board:
  def __init__(self, start_loc_x, start_loc_y):
    # Board Variables
    cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
    self.selected = [] # Currently selected cell (row, column)
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

    # Creation of the board
    self.space = tk.Canvas(width = cell_size*11, height = cell_size*11, highlightthickness=1, highlightbackground='black')
    self.space.place(x = start_loc_x, y = start_loc_y)
    self.space.bind_all('<Key>', self.cell_movement)

    y = cell_size # For the row
    for key in self.board_data:
      x = cell_size # For the column
      if key == 0:
        self.space.create_rectangle(cell_size-cell_size,cell_size-cell_size,cell_size,cell_size)
        for element in self.board_data[key]:
          self.space.create_rectangle(x,cell_size-cell_size,x+cell_size,cell_size)
          self.space.create_text(x+cell_size/2,cell_size/2, text = element)
          x += cell_size
      else:
        self.space.create_rectangle(cell_size-cell_size,y,cell_size,y+cell_size)
        self.space.create_text(cell_size/2,y+cell_size/2, text = f"{key}")
        for element in range(10):
          cell = self.space.create_rectangle(x,y,x+cell_size,y+cell_size, fill='lightblue')
          self.board_data[key].append(cell)
          x += cell_size
        y += cell_size

  # For getting the first selected cell and changing it.
  def selected_cell(self, row, column):
    self.selected = [row, column]
    coords = self.space.coords(self.board_data[self.selected[0]][self.selected[1]])
    self.cursor = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="black")

  def cell_movement(self, event):
    pressed_key = event.keysym.lower()
    
    if pressed_key == 'w' and self.selected[0] > 1:
      self.space.move(self.cursor, 0, -30)
      self.selected = [self.selected[0]-1, self.selected[1]]
    elif pressed_key == 'a' and self.selected[1] > 0:
      self.space.move(self.cursor, -30, 0)
      self.selected = [self.selected[0], self.selected[1]-1]
    elif pressed_key == 's' and self.selected[0] < 10:
      self.space.move(self.cursor, 0, 30)
      self.selected = [self.selected[0]+1, self.selected[1]]
    elif pressed_key == 'd' and self.selected[1] < 9:
      self.space.move(self.cursor, 30, 0)
      self.selected = [self.selected[0], self.selected[1]+1]

# Function to start the game
def show_game():
  button.place_forget()
  board_1 = Board(10, 10)
  board_1.selected_cell(1,2)
  board_2 = Board(350, 10)
  board_2.selected_cell(4,2)

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()