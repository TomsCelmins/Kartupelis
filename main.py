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
    
    x = cell_size
    y = cell_size
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

class Board_Cell(Board):
  def __init__(self, parent, x, y, row, column):
    self.parent = parent
    self.row = row
    self.column = column
    self.cell = self.parent.space.create_rectangle(x,y,x+cell_size,y+cell_size)
    
  def change_cell_color(self, color):
    self.parent.space.itemconfigure(self.parent.board_data[self.row][self.column-1].cell, fill=color)

def fill_board(board):
  y = cell_size
  for row in board.board_data:
    x = cell_size
    if len(board.board_data[row]) == 0:
      for column in range(10):
        board.board_data[row].append(Board_Cell(board, x, y, row, column))
        x += cell_size
      y += cell_size

def show_game():
  button.place_forget()
  board_1 = Board(10, 10) # Placing the board down
  
  fill_board(board_1) # Filling the board with its cells
  
  # Modifying cells (board_data[row][column])
  for i in range(3,9):
    board_1.board_data[7][i].change_cell_color("red")
  
  board_1.board_data[6][2].change_cell_color("red")
  board_1.board_data[6][9].change_cell_color("red")
  board_1.board_data[2][4].change_cell_color("red")
  board_1.board_data[3][4].change_cell_color("red")
  board_1.board_data[2][7].change_cell_color("red")
  board_1.board_data[3][7].change_cell_color("red")
  
  board_2 = Board(350, 10)
  
  fill_board(board_2)
  
  for i in range(3,9):
    board_2.board_data[7][i].change_cell_color("blue")
  
  board_2.board_data[8][2].change_cell_color("blue")
  board_2.board_data[8][9].change_cell_color("blue")
  board_2.board_data[2][4].change_cell_color("blue")
  board_2.board_data[3][4].change_cell_color("blue")
  board_2.board_data[2][7].change_cell_color("blue")
  board_2.board_data[3][7].change_cell_color("blue")

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()