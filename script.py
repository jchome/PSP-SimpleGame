# -*- coding: iso-8859-1 -*-

import threading
import psp2d, pspmp3
import stackless

import sys
# For PPSSPP
sys.path.insert(0,'.')
sys.path.insert(0,'./python')

import engine
import engine.widgets.debug_widget
import engine.widgets.controls_widget
import engine.widgets.inventory_widget
import engine.displays.welcome_display
import engine.displays.main_menu

import engine.translation
_ = engine.translation.translate

def load_assets(game, welcome_display):
    welcome_display.set_text(_("welcome.loading.music", game.current_language))
    ## Loads background music
    pspmp3.init(1)
    pspmp3.load("assets/music/welcome.mp3")
    pspmp3.play()

    ## Create the menu
    welcome_display.set_text(_("welcome.loading.menu", game.current_language))
    menu = engine.displays.main_menu.MainMenu()
    welcome_display.menu_display = menu

    ## Create the boards object
    welcome_display.set_text(_("welcome.loading.1st-board", game.current_language))
    meadow_001 = engine.Board("conf/boards/meadow-001.ini")
    player = engine.Player()
    meadow_001.add_agent(player)
    menu.play_board = meadow_001
    game.player = player

    #game.add_display(meadow_001)
    #game.set_active_display(meadow_001.name)

    welcome_display.set_text(_("welcome.loading.widgets", game.current_language))
    inventory = engine.widgets.inventory_widget.InventoryWidget(player)
    inventory.is_visible = False
    game.add_widget(inventory)

    #debug = engine.widgets.debug_widget.DebugWidget()
    #game.add_widget(debug)

    welcome_display.set_text(_("welcome.loading.done", game.current_language))
    welcome_display.is_ready = True



game = engine.Game()
game.current_language = "fr"

welcome = engine.welcome_display.WelcomeDisplay()
welcome.draw()
welcome.screen.swap()

game.set_active_display(welcome)
game.start()

loading_thread = threading.Thread(target=load_assets, args=(game, welcome, ))
loading_thread.start()

# Starts the game loop
stackless.run()
pspmp3.end()
