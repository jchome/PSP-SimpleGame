# -*- coding: iso-8859-1 -*-

import psp2d
import stackless

import sys
# For PPSSPP
sys.path.insert(0,'.')
sys.path.insert(0,'./python')

import engine
import engine.widgets.debug_widget
import engine.widgets.controls_widget
import engine.widgets.inventory_widget
import engine.welcome_display


game = engine.Game()
## Creates the boards object
#meadow_001 = engine.Board("conf/boards/meadow-001.ini")
#player = engine.Player()
#game.player = player
#meadow_001.add_agent(player)

#game.add_display(meadow_001)
#game.set_active_display(meadow_001.name)

#inventory = engine.widgets.inventory_widget.InventoryWidget(player)
#game.add_widget(inventory)

#debug = engine.widgets.debug_widget.DebugWidget()
#game.add_widget(debug)

welcome = engine.welcome_display.WelcomeDisplay("Welcome")

game.start()
game.set_active_display(welcome)

#Loads background music
#pspmp3.init(1)
#pspmp3.load("background-music.mp3")
#pspmp3.play()

# Starts the game loop
stackless.run()
#pspmp3.end()