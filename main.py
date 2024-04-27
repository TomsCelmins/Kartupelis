import tkinter as tk

window = tk.Tk()
window.geometry("800x500")

cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
class Board:
  instances = []
  
  def __init__(self, start_loc_x, start_loc_y, cursor_row, cursor_column):
    # Board Variables
    cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
    Board.instances.append(self)
    self.selected_area = {
      "row": cursor_row,
      "column": cursor_column,
      "ship_size": 1,
      "direction": "North",
      "overlay": None
    }
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
    coords = self.space.coords(self.board_data[self.selected_area["row"]][self.selected_area["column"]-1])
    self.selected_area["overlay"] = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="red")
    self.space.bind_all('<Key>', self.cell_movement)

  def focus(self):
    self.space.bind_all('<Key>', self.cell_movement)
    self.space.itemconfigure(self.selected_area["overlay"], fill="black")

  def redraw_ship(self):
    self.space.delete(self.selected_area["overlay"])
    coords = self.space.coords(self.board_data[self.selected_area["row"]][self.selected_area["column"]-1])
    if self.selected_area["ship_size"] == 1:
      self.selected_area["overlay"] = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="black")
    else:
      match self.selected_area["direction"]:
        case "West":
          self.selected_area["overlay"] = self.space.create_rectangle(coords[0]-(self.selected_area["ship_size"]-1)*cell_size,coords[1],coords[2],coords[3], fill="black")
        case "North":
          self.selected_area["overlay"] = self.space.create_rectangle(coords[0],coords[1]-(self.selected_area["ship_size"]-1)*cell_size,coords[2],coords[3], fill="black")
        case "East":
          self.selected_area["overlay"] = self.space.create_rectangle(coords[0],coords[1],coords[2]+(self.selected_area["ship_size"]-1)*cell_size,coords[3], fill="black")
        case "South":
          self.selected_area["overlay"] = self.space.create_rectangle(coords[0],coords[1],coords[2],coords[3]+(self.selected_area["ship_size"]-1)*cell_size, fill="black")
    
  def cell_movement(self, event):
    pressed_key = event.keysym.lower()

    # Moving
    if pressed_key in {"w", "a", "s", "d"}:
      if pressed_key == 'w' and self.selected_area["row"] > (self.selected_area["ship_size"] if self.selected_area["direction"] == "North" else 1):
        self.space.move(self.selected_area["overlay"], 0, -30)
        self.selected_area["row"] -= 1
      elif pressed_key == 'a' and self.selected_area["column"] > (self.selected_area["ship_size"] if self.selected_area["direction"] == "West" else 1):
        self.space.move(self.selected_area["overlay"], -30, 0)
        self.selected_area["column"] -= 1
      elif pressed_key == 's' and self.selected_area["row"] < (11-self.selected_area["ship_size"] if self.selected_area["direction"] == "South" else 10):
        self.space.move(self.selected_area["overlay"], 0, 30)
        self.selected_area["row"] += 1
      elif pressed_key == 'd' and self.selected_area["column"] < (11-self.selected_area["ship_size"] if self.selected_area["direction"] == "East" else 10):
        self.space.move(self.selected_area["overlay"], 30, 0)
        self.selected_area["column"] += 1
    # Changing Direction
    elif pressed_key in {"q", "e"}:
      directions = ["West", "North", "East", "South"]
      match pressed_key:
        case "q":
          if self.selected_area["direction"] == "West":
            self.selected_area["direction"] = "South"
          else:
            self.selected_area["direction"] = directions[directions.index(self.selected_area["direction"])-1]
        case "e":
          if self.selected_area["direction"] == "South":
            self.selected_area["direction"] = "West"
          else:
            self.selected_area["direction"] = directions[directions.index(self.selected_area["direction"])+1]
      self.redraw_ship()
            
    # Selecting ship size
    elif pressed_key in {"1", "2", "3", "4"}:
      self.selected_area["ship_size"] = int(pressed_key)
      self.redraw_ship()

    # Dev commands for switching boards
    match pressed_key:
      case "v":
        self.space.itemconfigure(self.selected_area["overlay"], fill="red")
        Board.instances[0].focus()
      case "b":
        self.space.itemconfigure(self.selected_area["overlay"], fill="red")
        Board.instances[1].focus()
        
    print(self.selected_area)
    
# Function to start the game
def show_game():
  button.place_forget()
  board_1 = Board(10, 10, 1, 2)
  board_2 = Board(350, 10, 4, 2)

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()