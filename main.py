import tkinter as tk

window = tk.Tk()
window.geometry("1000x1000")

class Board:
  instances = []
  cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
  
  def __init__(self, start_loc_x, start_loc_y, cursor_row, cursor_column):
    # Board Variables
    cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
    Board.instances.append(self)
    self.selected = [cursor_row, cursor_column]
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

    # --- Creation of the board ---
    self.space = tk.Canvas(width = cell_size*11, height = cell_size*11, highlightthickness=1, highlightbackground='black')
    self.space.place(x = start_loc_x, y = start_loc_y)
    
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

    # The cursor
    coords = self.space.coords(self.board_data[self.selected[0]][self.selected[1]-1])
    self.cursor = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="red")
    self.space.bind_all('<Key>', self.cell_movement)

  def focus(self):
    self.space.bind_all('<Key>', self.cell_movement)
    self.space.itemconfigure(self.cursor, fill="black")
    
  def cell_movement(self, event):
    pressed_key = event.keysym.lower()
    
    if pressed_key == 'w' and self.selected[0] > 1:
      self.space.move(self.cursor, 0, -30)
      self.selected = [self.selected[0]-1, self.selected[1]]
    elif pressed_key == 'a' and self.selected[1] > 1:
      self.space.move(self.cursor, -30, 0)
      self.selected = [self.selected[0], self.selected[1]-1]
    elif pressed_key == 's' and self.selected[0] < 10:
      self.space.move(self.cursor, 0, 30)
      self.selected = [self.selected[0]+1, self.selected[1]]
    elif pressed_key == 'd' and self.selected[1] < 10:
      self.space.move(self.cursor, 30, 0)
      self.selected = [self.selected[0], self.selected[1]+1]

    # Testing commands for switching boards
    match pressed_key:
      case "v":
        self.space.itemconfigure(self.cursor, fill="red")
        Board.instances[0].focus()
      case "b":
        self.space.itemconfigure(self.cursor, fill="red")
        Board.instances[1].focus()
      case "n":
        self.space.itemconfigure(self.cursor, fill="red")
        Board.instances[2].focus()
      case "m":
        self.space.itemconfigure(self.cursor, fill="red")
        Board.instances[3].focus()
        

# Function to start the game
def show_game():
  button.place_forget()
  board_1 = Board(10, 10, 1, 2)
  board_2 = Board(350, 10, 4, 2)
  board_3 = Board(10, 350, 4, 2)
  board_4 = Board(350, 350, 4, 2)

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()