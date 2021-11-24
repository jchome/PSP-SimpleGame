# -*- coding: iso-8859-1 -*-

import psp2d
import pspos
import stackless
from time import time

## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272

"""
Agent base class, mother class of every visible item on the screen.
"""
class Agent(object):
    def __init__(self):
        #self.ch = stackless.channel()       # Communication channel (not used here)
        pass

    """
    Update the visibility of the instance.
    """
    def update(self, walls):
        # In the base class do nothing
        pass

    """
    Draw the instance in the screen.
    """
    def draw(self, screen, walls):
        # In the base class do nothing
        pass

    """
    Returns True if the agent is in collision with walls
    @param walls: the image of the walls. Transparent = no wall
    """
    def detect_collision(self, walls, pos_x, pos_y):
        pixel = walls.getPixel(pos_x, pos_y)
        return pixel.alpha != 0

"""
Main class of the game.
Every item is resistered in this container.
"""
class Render():
    def __init__(self):
        self.screen = psp2d.Screen()
        self.agents = []
        self.running = True 
        stackless.tasklet(self.runAction)() # Creates the agent tasklet
        self.background = psp2d.Image('assets/bg-1.png')
        self.walls = psp2d.Image('assets/bg-1-walls.png')

    """
    Main action of the agent.
    Run the action() method while the instance is running.
    """
    def runAction(self):
        
        while self.running:
            # Update the instance
            self.update()

            # Draw the instance
            self.draw()

            # Give other tasklets its turn
            stackless.schedule()

    def exit(self):
        # When the player calls the exit, tell all Agents to stop running
        self.running = False
        for agent in self.agents:
            agent.running = False


    """
    Update all registered agents, then draw all
    """
    def update(self):
        pad = psp2d.Controller()
        if pad.cross:
            print("exit")
            self.exit()

        for agent in self.agents:
            agent.update(self.walls)

    def draw(self):
        # Each frame the renderer clears the screen,
        # writes the text and draws each registered agent.
        #background_color_1 = psp2d.Color(42,70,29,255)
        #background_color_2 = psp2d.Color(42,60,29,255)
        #self.screen.clear(background_color_1)

        ## 480 = 15 * 32
        ## 272 = 8.5 * 32
        #for i in range(0, 15):
        #    for j in range(0, 9):
        #        if (i%2 and (j+1)%2) or ((i+1)%2 and j%2):
        #            self.screen.fillRect(i*32,j*32,32,32, background_color_2)
        self.screen.blit(self.background, 0, 0, 480, 272, 0, 0, True)
        font.drawText(self.screen, 0, 0, "(0,0) - Press X to exit")
        for agent in self.agents:
            agent.draw(self.screen)
        self.screen.swap()

class Player(Agent):
    def __init__(self):
        Agent.__init__(self)
        self.sprite = psp2d.Image('assets/player.png')
        self.split = {
            "RIGHT": [[0,64], [0,32], [0,0], [0,32]],
            "LEFT": [[96,64], [96,32], [96,0], [96,32]],
            "UP": [[32,64], [32,32], [32,0], [32,32]],
            "DOWN": [[64,64], [64,32], [64,0], [64,32]]
            }
        self.width = 32
        self.height = 32
        self.direction = "DOWN"
        self.is_running = False
        self.animation_flow = 0
        self.velocity = 4
        self.pos_x = 10
        self.pos_y = 170
        self.shadow_with = 16
        self.shadow_height = 31
        self.lastPad = time()
    
    def update(self, walls):
        pad = psp2d.Controller()
        if pad.down and (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            self.direction = "DOWN"
            new_pos_y = min(self.pos_y + self.velocity, MAX_HEIGHT - self.height)
            if not self.detect_collision(walls, 
                                         self.pos_x + (self.shadow_with/2), 
                                         new_pos_y + (self.shadow_height/2)):
                self.pos_y = new_pos_y
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0
        elif pad.up and (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            self.direction = "UP"
            new_pos_y = max(self.pos_y - self.velocity, 0)
            if not self.detect_collision(walls, 
                                         self.pos_x + (self.shadow_with/2), 
                                         new_pos_y + (self.shadow_height/2)):
                self.pos_y = new_pos_y
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0
        elif pad.left and (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            self.direction = "LEFT"
            new_pos_x = max(self.pos_x - self.velocity, 0)
            if not self.detect_collision(walls, 
                                         new_pos_x + (self.shadow_with/2), 
                                         self.pos_y + (self.shadow_height/2)):
                self.pos_x = new_pos_x
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0
        elif pad.right and (not self.lastPad or time() - self.lastPad >= 0.05):
            self.lastPad = time()
            self.direction = "RIGHT"
            new_pos_x = min(self.pos_x + self.velocity, MAX_WIDTH - self.width)
            if not self.detect_collision(walls, 
                                         new_pos_x + (self.shadow_with/2), 
                                         self.pos_y + (self.shadow_height/2)):
                self.pos_x = new_pos_x
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0
        
    def draw(self, screen):
        image_bank = self.split[self.direction][int(self.animation_flow)]
        top = image_bank[0]
        left = image_bank[1]
        screen.blit(self.sprite, top, left, self.width, self.height, self.pos_x, self.pos_y, True)
        if self.is_running:
            if self.animation_flow > len(self.split[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0
                self.is_running = False
            else:
                # One more step of the animation
                self.animation_flow = self.animation_flow + 0.25

# Creates the screen and its background color (Black)

# Loads the font
font = psp2d.Font('font.png')

# Creates the renderer object
renderer = Render()
player = Player()
renderer.agents.append(player)

#Loads background music
#pspmp3.init(1)
#pspmp3.load("background-music.mp3")
#pspmp3.play()

# Starts the game loop
stackless.run()
#pspmp3.end()