# -*- coding: iso-8859-1 -*-

import psp2d
import stackless

import sys
# For PPSSPP
sys.path.insert(0,'.')
sys.path.insert(0,'./python')

import engine


# Loads the font
font = psp2d.Font('font.png')

game = engine.Game()
# Creates the renderer object
meadow_001 = engine.Render("conf/renderers/meadow-001.ini")
player = engine.Player()
game.player = player
meadow_001.add_agent(player)

game.add_renderer(meadow_001)
game.set_active_renderer(meadow_001.name)

game.start()

#Loads background music
#pspmp3.init(1)
#pspmp3.load("background-music.mp3")
#pspmp3.play()

# Starts the game loop
stackless.run()
#pspmp3.end()