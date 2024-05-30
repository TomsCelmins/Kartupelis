import time
import tkinter as tk
import random

window = tk.Tk()

window.geometry("1000x500")

canvas_1 = tk.Canvas(window, width=1000, height=500,bg='lightblue')
canvas_1.pack()

# Create a line on the canvas
rectangle_1 = canvas_1.create_rectangle(0, 0, 1000, 500, fill='lightblue')
rectangle_2 = canvas_1.create_rectangle(0, 250, 1000, 500, fill='blue')

#set speeds
line_speed = 5
ship_speed = 3

#line lenght
line_lenght = 100

#create lines 
line1 = canvas_1.create_line(0,250,line_lenght,250, fill='black',width=2)
line2 = canvas_1.create_line(100,300, 100 + line_lenght,300, fill='black',width=2)
line3 = canvas_1.create_line(200, 350, 200 + line_lenght, 350, fill='black', width=2)
line4 = canvas_1.create_line(300, 400, 300 +line_lenght, 400, fill='black', width=2)

# crate ship
moving_ship = canvas_1.create_polygon(100,200,150,250,350,250,400,200,fill='gray',outline='black')
moving_ship_head = canvas_1.create_rectangle(200,150,300,200,fill='grey', outline='black')
# create clouds

cloud1 = canvas_1.create_oval(50,50,150,100,fill='white', outline='white')
cloud2 = canvas_1.create_oval(300,100,400,140,fill='white', outline='white')
cloud3 = canvas_1.create_oval(650,50,750,100,fill='white', outline='white')
cloud4 = canvas_1.create_oval(850,90,950,140,fill='white', outline='white')

clouds = [cloud1, cloud2, cloud3, cloud4]

def move_clouds():
  for cloud in clouds:
    cx = random.randint(-1,1)
    cy = random.randint(-1,1)
    canvas_1.move(cloud,cx,cy)

  window.after(100,move_clouds)

move_clouds()


def move_ship():
  global moving_ship, moving_ship_head
# move the ship sideways

  canvas_1.move(moving_ship, ship_speed,0) # move sideways
  canvas_1.move(moving_ship_head, ship_speed,0) # move sideways

  pos1 = canvas_1.coords(moving_ship)
  pos2 = canvas_1.coords(moving_ship_head)

  if pos1[0] >= 1000:
    canvas_1.coords(moving_ship, 0, 200, 50, 250, 250, 250, 300, 200) #reset position if it goes out of screen

    canvas_1.coords(moving_ship_head, 50, 150, 150, 200) # reset the position of head with ship

  if pos2[2] <= 0:
    canvas_1.coords(moving_ship_head, 950, 150, 1050, 200) # reset if it goes out screen

  window.after(50, move_ship)

move_ship()


def move_lines():
  global line1, line2

  #move the lines sideway
  canvas_1.move(line1, line_speed,0)
  canvas_1.move(line2,-line_speed,0)
  canvas_1.move(line3, line_speed,0)
  canvas_1.move(line4,-line_speed,0)

  # get lines coordinates
  pos1 = canvas_1.coords(line1)
  pos2 = canvas_1.coords(line2)
  pos3 = canvas_1.coords(line3)
  pos4 = canvas_1.coords(line4)

  # make a loop so if line goes out of lenght it resets 
  if pos1[0] >= 1000:
    canvas_1.coords(line1, -line_lenght, 250, 0, 250)
  if pos2[2] <= 0:
    canvas_1.coords(line2, 1000, 300, 1000 + line_lenght, 300)
  if pos3[0] >= 1000:
    canvas_1.coords(line3, -line_lenght, 350, 0, 350)
  if pos4[2] <= 0:
    canvas_1.coords(line4, 1000, 400, 1000 + line_lenght, 400)

  window.after(50, move_lines)


# acctivate the function
move_lines()


cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
class Board:
  previous_instance = None # For switching to the previous board

window.geometry("800x500")

cell_size = 30 # Size of the boards individual cell's, which would also mean the boards size.
class Board:
  previous_instance = None # For switching to the previous board
  

  def __init__(self, start_loc_x, start_loc_y):
    # --- Board Variables ---
    if Board.previous_instance is None:
      Board.previous_instance = self
      self.name = "2 spēlētājs"
    else:
      self.name = "1 spēlētājs"
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

# will show guides and explain how to play the game
# Guide screen
def toogle_guide():
  global guide_window
  if 'guide_window' in globals() and guide_window.winfo_exists():
      guide_window.destroy()
  else:
    guide_window = tk.Toplevel(window)
    guide_window.title("Game Guide")
    guide_text = tk.Label(guide_window, text="Set up the game grid: The game grid consists of 11 rows labeled 'K', 'A', 'R', 'T', 'U', 'P', 'E', 'L', 'I', 'S',\n and 11 columns labeled '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'.\n\nPlace ships: Each player secretly places their ships on their grid. The ships can vary in size:\n\nBattleship: occupies 4 consecutive squares.\nCruiser: occupies 3 consecutive squares.\nDestroyer: occupies 2 consecutive squares.\nSubmarine: occupies 1 square.\n\nTake turns guessing: Players take turns guessing coordinates on the opponent's grid to try and hit their ships. For example, 'K3' or 'S11'.\n\nFeedback on guesses: After each guess, provide feedback on whether it was a hit or a miss:\n\nIf the guess hits a ship, mark the corresponding square as hit.\nIf the guess misses, mark the corresponding square as a miss.\n\nSink ships: When a player hits all the squares of a ship, it's considered sunk. Keep track of the number of hits on each ship.\n\nWin condition: The game ends when one player has sunk all of their opponent's ships.\n\nKeyBinds: w-up, s-down, a-left, d-right\nq-turn ship 90* to left, e - turn ship 90* to right\nf-place ship\n 1,2,3,4 - chose a ship", justify="left",anchor="nw")
    guide_text.pack()

Guide_button = tk.Button(text="?", command=toogle_guide)
Guide_button.place(x=10, y=460)

# Function to start the game
def show_game():
  button.place_forget()
  Board(450, 80)
  Board(10, 80)

# Headline 
kartupeli_text = tk.Label(window, text="KARTUPELI", font=("Helvetica", 40), bg='lightblue')
kartupeli_text.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
# Button that starts the game
button = tk.Button(text="START GAME", command=show_game, height=5, width=20, fg='black',bg='yellow')
button.place(x = 400,y = 200)


window.mainloop()
