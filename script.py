# -*- coding: iso-8859-1 -*-

import psp2d
import stackless

from interaction_object import InteractionObject
from player import Player
from renderer import Render


class Game():
    def __init__(self):
        self.renderers = {}
        self.active_renderer = None
        self.is_finished = False
    
    def set_active_renderer(self, renderer_name):
        ## De-active the current active renderer 
        if self.active_renderer is not None:
            self.active_renderer.active = False
        
        if self.renderers[renderer_name] is None:
            print("No renderer in ")
            print(self.renderers)
            return

        self.active_renderer = self.renderers[renderer_name]
        self.active_renderer.active = True
        #print("self.active_renderer : %s" % renderer_name)

    def add_renderer(self, renderer):
        renderer.game = self
        self.renderers[renderer.name] = renderer

    def start(self):
        self.is_finished = False
        stackless.tasklet(self.tasklet_renderer)() # Creates the agent tasklet

    """
    Main action of the agent.
    Run the action() method while the instance is running.
    """
    def tasklet_renderer(self):
        pad = psp2d.Controller()
        while not self.is_finished:
            if pad.circle:
                print("exit")
                self.exit()

            if self.active_renderer is None:
                print("self.active_renderer is None")
                return

            # Update the instance
            self.active_renderer.update()

            # Draw the instance
            self.active_renderer.draw()

            # Give other tasklets its turn
            stackless.schedule()


# Loads the font
font = psp2d.Font('font.png')

game = Game()
# Creates the renderer object
meadow_001 = Render("conf/renderers/meadow-001.ini")
player = Player()
meadow_001.add_agent(player)

game.add_renderer(meadow_001)
game.set_active_renderer("meadow_001")

tavern_interior_001 = Render("conf/renderers/tavern-interior.ini")
game.add_renderer(tavern_interior_001)

game.start()

#Loads background music
#pspmp3.init(1)
#pspmp3.load("background-music.mp3")
#pspmp3.play()

# Starts the game loop
stackless.run()
#pspmp3.end()