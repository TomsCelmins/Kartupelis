import time
import tkinter as tk

window = tk.Tk()
window.geometry("800x500")

cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
class Board:
  previous_instance = None # For switching to the previous board
  
  def __init__(self, start_loc_x, start_loc_y):
    # --- Board Variables ---
    if Board.previous_instance is None:
      Board.previous_instance = self
      self.name = "1 spēlētājs"
    else:
      self.name = "2 spēlētājs"
    self.overlays = [] # Each element contains [(overlay_id), (ship_identifier)]
    self.hit_ships = []
    self.mode = "placing"
    self.ship_amounts = { # key == ship size, element == amount of ships 
      2: 3,
      3: 2,
      4: 1,
    }
    self.total_ships_left = 6
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
    self.space = tk.Canvas(width = cell_size*11, height = cell_size*12, highlightthickness=1, highlightbackground='black')
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

    self.space.create_text(cell_size*5.5,cell_size*11+cell_size/2, text=self.name)
    # The cursor
    coords = self.board_data[self.cursor["row"]][self.cursor["column"]-1]
    self.cursor["overlay"] = self.space.create_oval(coords[0]+10,coords[1]+10,coords[2]-10,coords[3]-10, fill='black')
    self.space.bind_all('<Key>', self.key_press)

  def switch_board(self):
    self.space.bind_all('<Key>', self.key_press)

  def show_board(self):
      for object in self.overlays:
        self.space.itemconfigure(object[0], state='normal', fill='green')

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
    
  def key_press(self, event):
    if self.mode == 'end':
      return
    pressed_key = event.keysym.lower()

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
    if self.mode == "placing":
      match pressed_key:
        # Action key
        case 'f':
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
    
        # Delete previously placed ship
        case 'backspace':
          if self.overlays == []: # Nothing to delete if theres nothing on the board
            return
          object = self.overlays[len(self.overlays)-1]
          for row in self.board_data:
            if row == 0:
              continue
            for cell in self.board_data[row]:
              if cell[4] == object[1]:
                cell[4] = 0.0
    
          self.space.itemconfigure(object[0], state='hidden')
          self.ship_amounts[object[1]//10] += 1
          self.overlays.remove(object)

        # Confirming your ship placement
        case 'return':
          # Safety check if all ships have been placed
          for num in self.ship_amounts:
            if self.ship_amounts[num] > 0:
              return

          for object in self.overlays:
            self.space.itemconfigure(object[0], state='hidden')

          self.mode = "shooting"
          other_board = Board.previous_instance
          Board.previous_instance = self
          other_board.switch_board()
          
        # Change cardinal direction
        case 'q'|'e':
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
                
        # Select ship size
        case "1"|"2"|"3"|"4":
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
    else:
      match pressed_key:
        case 'f':
          cell = self.board_data[self.cursor["row"]][self.cursor["column"]-1]
          if cell[4] != 0.0 and cell[4] != 'shot':
            self.space.create_line(cell[0],cell[1],cell[2],cell[3])
            self.space.create_line(cell[0]+cell_size,cell[1],cell[2]-cell_size,cell[3])

            # Referencing the ship part that was hit + checking if the entire ship has been destroyed
            self.hit_ships.append(cell[4])
            if self.hit_ships.count(cell[4]) == cell[4]//10:
              for object in self.overlays:
                if object[1] == cell[4]:
                  self.space.itemconfigure(object[0], state='normal', fill='red')
              self.total_ships_left -= 1
              # End game if all ships have been destroyed
              if self.total_ships_left == 0:
                print(Board.previous_instance.name, "uzvar!")
                self.mode = 'end'
                Board.previous_instance.show_board()
            cell[4] = "shot"
          elif cell[4] != 'shot':
            cell[4] = "shot"
            self.space.create_oval(cell[0]+5,cell[1]+5,cell[2]-5,cell[3]-5)
            
            other_board = Board.previous_instance
            Board.previous_instance = self
            other_board.switch_board()
          else:
            self.placement_warning()
    
# Function to start the game
def show_game():
  button.place_forget()
  Board(10, 10)
  Board(350, 10)

button = tk.Button(text="start game", command=show_game)
button.place(x = 0,y = 0)

tk.mainloop()