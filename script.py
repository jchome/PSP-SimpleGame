# -*- coding: iso-8859-1 -*-

import psp2d
import stackless

from interaction_object import InteractionObject
from player import Player
from renderer import Render
from game import Game


# Loads the font
font = psp2d.Font('font.png')

game = Game()
# Creates the renderer object
meadow_001 = Render("conf/renderers/meadow-001.ini")
player = Player()
game.player = player
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