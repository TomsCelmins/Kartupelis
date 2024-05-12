import time
import tkinter as tk

window = tk.Tk()
window.geometry("800x500")

cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
class Board:
  instances = []
  
  def __init__(self, start_loc_x, start_loc_y):
    # Board Variables
    cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
    Board.instances.append(self)
    self.overlays = []
    # key == ship size, element == amount of ships
    self.ship_amounts = {
      2: 3,
      3: 2,
      4: 1
    }
    self.cursor = {
      "row": 5,
      "column": 5,
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
          cell_coords = self.space.coords(cell)
          cell_coords.append(0.0) # Extra space for the state
          self.board_data[key].append(cell_coords) # Storing the coords
          x += cell_size
        y += cell_size

    # The cursor
    coords = self.board_data[self.cursor["row"]][self.cursor["column"]-1]
    self.cursor["overlay"] = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="red")
    self.space.bind_all('<Key>', self.cell_movement)

  def focus(self):
    self.space.bind_all('<Key>', self.cell_movement)
    self.space.itemconfigure(self.cursor["overlay"], fill="black")

  def placement_warning(self):
    self.space.itemconfigure(self.cursor["overlay"], fill="red")
    self.space.update()
    time.sleep(0.2)
    self.space.itemconfigure(self.cursor["overlay"], fill="black")

  def redraw_ship(self):
    self.space.delete(self.cursor["overlay"])
    coords = self.board_data[self.cursor["row"]][self.cursor["column"]-1]
    if self.cursor["ship_size"] == 1:
      self.cursor["overlay"] = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill="black")
    else:
      match self.cursor["direction"]:
        case "West":
          self.cursor["overlay"] = self.space.create_rectangle(coords[0]-(self.cursor["ship_size"]-1)*cell_size,coords[1],coords[2],coords[3], fill="black")
        case "North":
          self.cursor["overlay"] = self.space.create_rectangle(coords[0],coords[1]-(self.cursor["ship_size"]-1)*cell_size,coords[2],coords[3], fill="black")
        case "East":
          self.cursor["overlay"] = self.space.create_rectangle(coords[0],coords[1],coords[2]+(self.cursor["ship_size"]-1)*cell_size,coords[3], fill="black")
        case "South":
          self.cursor["overlay"] = self.space.create_rectangle(coords[0],coords[1],coords[2],coords[3]+(self.cursor["ship_size"]-1)*cell_size, fill="black")
    
  def cell_movement(self, event):
    pressed_key = event.keysym.lower()
    print(pressed_key)
    print(self.board_data[self.cursor["row"]][self.cursor["column"]-1])

    # Moving
    if pressed_key in {'w', 'a', 's', 'd'}:
      if pressed_key == 'w' and self.cursor["row"] > (self.cursor["ship_size"] if self.cursor["direction"] == "North" else 1):
        self.space.move(self.cursor["overlay"], 0, -30)
        self.cursor["row"] -= 1
      elif pressed_key == 'a' and self.cursor["column"] > (self.cursor["ship_size"] if self.cursor["direction"] == "West" else 1):
        self.space.move(self.cursor["overlay"], -30, 0)
        self.cursor["column"] -= 1
      elif pressed_key == 's' and self.cursor["row"] < (11-self.cursor["ship_size"] if self.cursor["direction"] == "South" else 10):
        self.space.move(self.cursor["overlay"], 0, 30)
        self.cursor["row"] += 1
      elif pressed_key == 'd' and self.cursor["column"] < (11-self.cursor["ship_size"] if self.cursor["direction"] == "East" else 10):
        self.space.move(self.cursor["overlay"], 30, 0)
        self.cursor["column"] += 1

    elif pressed_key == 'return':
      if self.cursor["ship_size"] == 1: # We dont have 1 sized ships
        return
      # Safety checks to see if a nother ship is in the way
      for cell in range(self.cursor["ship_size"]):
        match self.cursor["direction"]:
          case "West":
            if self.board_data[self.cursor["row"]][self.cursor["column"]-cell-1][4] != 0.0:
              self.placement_warning()
              return
          case "North":
            if self.board_data[self.cursor["row"]-cell][self.cursor["column"]-1][4] != 0.0:
              self.placement_warning()
              return
          case "East":
            if self.board_data[self.cursor["row"]][self.cursor["column"]+cell-1][4] != 0.0:
              self.placement_warning()
              return
          case "South": 
            if self.board_data[self.cursor["row"]+cell][self.cursor["column"]-1][4] != 0.0:
              self.placement_warning()
              return
      # Reference that these cells currently have a ship on it
      ship_identifier = self.cursor["ship_size"]*10+self.ship_amounts[self.cursor["ship_size"]]
      new_overlay = self.space.create_rectangle(self.space.coords(self.cursor["overlay"]), fill='black')
      self.overlays.append([new_overlay, ship_identifier])
      for cell in range(self.cursor["ship_size"]):
        match self.cursor["direction"]:
          case "West":
            self.board_data[self.cursor["row"]][self.cursor["column"]-cell-1][4] = ship_identifier
          case "North":
            self.board_data[self.cursor["row"]-cell][self.cursor["column"]-1][4] = ship_identifier
          case "East":
            self.board_data[self.cursor["row"]][self.cursor["column"]+cell-1][4] = ship_identifier
          case "South":
            self.board_data[self.cursor["row"]+cell][self.cursor["column"]-1][4] = ship_identifier
      # Remove 1 ship from the amount
      self.ship_amounts[self.cursor["ship_size"]] -= 1
      if self.ship_amounts[self.cursor["ship_size"]] == 0:
        self.cursor["ship_size"] = 1
        self.redraw_ship()

    elif pressed_key == 'backspace':
      if self.overlays == []: # Nothing to delete if theres nothing on the board
        return
      object = self.overlays[len(self.overlays)-1]
      print(object)
      for row in self.board_data:
        if row == 0:
          continue
        for cell in self.board_data[row]:
          if cell[4] == object[1]:
            cell[4] = 0.0

      self.space.itemconfigure(object[0], state='hidden')
      self.ship_amounts[object[1]//10] += 1
      self.overlays.remove(object)
      
    # Changing Direction
    elif pressed_key in {'q', 'e'}:
      # Early return if invalid
      match self.cursor["direction"]:
        case "West":
          if (self.cursor["row"]-self.cursor["ship_size"] < 0 if pressed_key == "e" else self.cursor["row"]+self.cursor["ship_size"] > 11):
            self.placement_warning()
            return
        case "North":
          if (self.cursor["column"]-self.cursor["ship_size"] < 0 if pressed_key == "q" else self.cursor["column"]+self.cursor["ship_size"] > 11):
            self.placement_warning()
            return
        case "East":
          if (self.cursor["row"]-self.cursor["ship_size"] < 0 if pressed_key == "q" else self.cursor["row"]+self.cursor["ship_size"] > 11):
            self.placement_warning()
            return
        case "South":
          if (self.cursor["column"]-self.cursor["ship_size"] < 0 if pressed_key == "e" else self.cursor["column"]+self.cursor["ship_size"] > 11):
            self.placement_warning()
            return
    
      directions = ["West", "North", "East", "South"]
      match pressed_key:
        case "q":
          self.cursor["direction"] = directions[directions.index(self.cursor["direction"])-1]
        case "e":
          directions_reversed = directions[::-1]
          self.cursor["direction"] = directions_reversed[directions_reversed.index(self.cursor["direction"])-1]
      self.redraw_ship()
            
    # Selecting ship size
    elif pressed_key in {"1", "2", "3", "4"}:
      if int(pressed_key) != 1 and self.ship_amounts[int(pressed_key)] == 0: # Cant place ships if there are none left
        self.placement_warning()
        return
        
      match self.cursor["direction"]:
        case "West":
          if self.cursor["column"]-int(pressed_key) < 0:
            self.placement_warning()
            return
        case "North":
          if self.cursor["row"]-int(pressed_key) < 0:
            self.placement_warning()
            return
        case "East":
          if self.cursor["column"]+int(pressed_key) > 11:
            self.placement_warning()
            return
        case "South":
          if self.cursor["row"]+int(pressed_key) > 11:
            self.placement_warning()
            return
      
      self.cursor["ship_size"] = int(pressed_key)
      self.redraw_ship()

    # Dev commands for switching boards
    match pressed_key:
      case "v":
        self.space.itemconfigure(self.cursor["overlay"], fill="red")
        Board.instances[0].focus()
      case "b":
        self.space.itemconfigure(self.cursor["overlay"], fill="red")
        Board.instances[1].focus()
        
    print(self.cursor)
    
# Function to start the game
def show_game():
  button.place_forget()
  board_1 = Board(10, 10)
  board_2 = Board(350, 10)

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()