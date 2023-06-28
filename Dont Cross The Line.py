'''
Author: Kacie Varner
Version: 0.2 Final, for now
Last Modified: 5/16/2017

See sources.txt for media sources

Contains the following classes:

Game
Player
Block
'''

from Tkinter import *
from PIL import Image, ImageTk
import winsound

global game_state
global time

class Game():
    #Defines the lists, X Y coordinates, and game state at the beginning
    blocks = []
    game_objects = []
    init_x_mouse = 0
    init_y_mouse = 0
    game_state = 'play'

    def start(self):
        #Initiates the game and binds all of the different classes and keys to one another
        self.root = Tk()
        self.root.title("Don't Cross The Line")
        self.game_area = Canvas(self.root, bg='black', width=1000, height=600)
        self.game_area.pack()
        self.player = Player(950,500,self.game_area, 'left','blue', self)
        self.AI = Player(50,50,self.game_area, 'right','red', self)
        self.game_objects.append(self.AI)
        self.game_objects.append(self.player)
        self.root.bind("<Key>", self.key_handler)
        self.start_screen()
        self.play()
        self.root.mainloop()
        
    def key_handler(self, event):
        #Allows the arrow keys to move the player
        if event.keysym == 'Up':
            self.player.direction = 'up'
        if event.keysym == 'Left':
            self.player.direction = 'left'
        if event.keysym == 'Right':
            self.player.direction = 'right'
        if event.keysym == 'Down':
            self.player.direction = 'down'
        #Allows WSAD keys to move the AI
        if event.char == 'w':
            self.AI.direction = 'up'
        if event.char == 'a':
            self.AI.direction = 'left'
        if event.char == 'd':
            self.AI.direction = 'right'
        if event.char == 's':
            self.AI.direction = 'down'
        #If the spacebar is hit while on the start screen then the game starts and the text is deleted
        if event.char == ' ':
            if self.game_state == 'stop':
                winsound.PlaySound('beep.mp3', winsound.SND_FILENAME|winsound.SND_ASYNC)
                self.game_state = 'play'
                self.game_area.delete('start_message')
            
            
    def play(self):
        #Lets the player move in an infinate loop only if the game state is 'play'
        if self.game_state == 'play':
            for objects in self.game_objects:
                objects.act()
                objects.create()
        self.root.after(30, self.play)
        
    def start_screen(self):
        #Sets the game state to stop and displays the start screen
        self.game_state = 'stop'
        self.game_area.create_text(500, 300, text="- Press Space to Start Game -", fill="white", font="comicsans 18", tags = 'start_message')

class Player():
    
    def __init__(self, x, y, game_area, direction, color, parent):
        #Creates the player block and stores the line of blocks in a list that is referenced to for hit detection
        self.x = x
        self.y = y
        self.game_area = game_area
        self.color = color
        self.sprite = self.game_area.create_rectangle(x,y,x+20,y+20, fill = self.color, outline = self.color,tags='player')
        self.direction = direction
        self.player_line = []
        self.parent = parent
        self.count = 1
        
    def create(self):
        #Creates the line of blocks behind the player and AI
        createx = self.x
        createy = self.y
        self.count += 1
        if self.count == 2:
            self.block = Block(createx,createy, self.game_area,self.color)
            self.parent.blocks.append(self.block)
            self.count = 0

    def act(self):
        #Allows the block to move in every direction smoothly by only moving 3 pixels at a time
        if self.direction == 'right' and self.can_move():
            self.game_area.move(self.sprite, 3, 0)
        if self.direction == 'left' and self.can_move():
            self.game_area.move(self.sprite, -3, 0)
        if self.direction == 'down' and self.can_move():
            self.game_area.move(self.sprite,0,3)
        if self.direction == 'up' and self.can_move():
            self.game_area.move(self.sprite,0,-3)
            
        coords = self.game_area.coords(self.sprite)
        self.x, self.y = coords[0], coords[1]
        
    def can_move(self):
        #Stops the player on the edges
        if self.direction == 'right':
            if self.x > 980:
                return False
        if self.direction == 'left':
            if self.x < 0:
                return False            
        if self.direction == 'down':
            if self.y > 580:
                return False
        if self.direction == 'up':
            if self.y < 0:
                return False
        for block in self.parent.blocks:
            if self.does_collide(block):
                self.die()
        return True
        
    def does_collide(self, block):
        #Detects if the block collides with another block
        block.count -= 1
        flag = False
        if abs(self.x - block.x) < 20 and abs(self.y - block.y) < 20 and block.count <= 0:
            flag = True
        return flag
        
    def die(self):
        #stops the game and says game over and who wins when the blocks collide
        winsound.PlaySound('impact.wav', winsound.SND_FILENAME|winsound.SND_ASYNC)
        die = False
        self.parent.game_state = 'stop'
        self.game_area.create_text(500, 300, text="Game Over", fill="white", font="comicsans 48")
        #If the players collide the game over screen will be displayed along with the player who won
        if self.parent.game_state == 'stop':
            for block in self.parent.blocks:
                if self.does_collide(block):
                    if self.color == 'red':
                        self.game_area.create_text(700, 400, text="Blue Wins!", fill="blue", font="comicsans 48")
                    else:
                        self.game_area.create_text(300, 200, text="Red Wins!", fill="red", font="comicsans 48")
        
class Block():
    
   def __init__(self, x, y, game_area, color):
       #Creates the block behind the initial block with a delay
        self.x = x
        self.y = y
        self.game_area = game_area
        self.sprite = self.game_area.create_rectangle(x,y,x+20,y+20, outline = color,fill = color, tags='player')
        self.direction = 'e'
        self.count = 40
        
if __name__ == "__main__":
    #Starts the game
    game = Game()
    game.start()       