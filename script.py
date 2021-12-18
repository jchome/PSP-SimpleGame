# -*- coding: iso-8859-1 -*-

import psp2d
import stackless

import helper
from interaction_object import InteractionObject
from player import Player

## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272
## X = left axis
## Y = bottom axis

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
        (self.background, self.walls) = helper.load_sprite("assets/bg-1.png", 
            MAX_WIDTH, MAX_HEIGHT)
        self.final_walls = psp2d.Image(MAX_WIDTH, MAX_HEIGHT)
        self.final_walls.blit(self.walls, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)

    """
    Add the static agent with its wall
    """
    def add_static_agent(self, agent):
        self.final_walls.blit(agent.walls, 0, 0, 
            agent.width, agent.height, 
            agent.pos_x, agent.pos_y, True)
        self.agents.append(agent)
        

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
        if pad.circle:
            print("exit")
            self.exit()

        ## Update agents considering all walls
        for agent in self.agents:
            agent.update(self.agents, self.walls)

    def draw(self):
        # Each frame the renderer apply the background,
        # writes the text and draws each registered agent.
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        
        #player = self.agents[0]
        #font.drawText(self.screen, 0, 0, "coins: %d - Press O to exit" % (player.bonus))
        # Sort agents before display
        for agent in sorted(self.agents, key=lambda agent: agent.pos_y + agent.sort_position, reverse=False):
            agent.draw(self.screen)

        self.screen.swap()


# Loads the font
font = psp2d.Font('font.png')

# Creates the renderer object
renderer = Render()
player = Player()
renderer.agents.append(player)

coin = InteractionObject('conf/coin.ini')
coin.pos_x = 300
coin.pos_y = 160
renderer.agents.append(coin)

building = InteractionObject('conf/tavern.ini')
building.pos_x = 130
building.pos_y = 0
renderer.agents.append(building)


#Loads background music
#pspmp3.init(1)
#pspmp3.load("background-music.mp3")
#pspmp3.play()

# Starts the game loop
stackless.run()
#pspmp3.end()