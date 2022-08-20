# -*- coding: iso-8859-1 -*-

import threading
import pspmp3
import stackless

## Comment these lines to make it work of the real PSP console
## For PPSSPP
import sys
sys.path.insert(0,'.')
sys.path.insert(0,'./python')

from engine.displays.welcome_display import WelcomeDisplay
from engine.game import Game
from engine.displays.board import Board

import engine.translation
_ = engine.translation.translate

def load_assets(game, welcome_display):
    welcome_display.set_text(_("welcome.loading.music", game.current_language))
    ## Loads background music
    #pspmp3.init(1)
    #pspmp3.load("assets/music/welcome.mp3")
    #pspmp3.play()

    ## Create the menu
    from engine.displays.main_menu import MainMenu
    welcome_display.set_text(_("welcome.loading.menu", game.current_language))
    menu = MainMenu()
    welcome_display.menu_display = menu
    game.add_display(menu)

    ## Create the boards object
    welcome_display.set_text(_("welcome.loading.1st-board", game.current_language))
    game.create_environment(menu)

    ## Inventory Widget
    from engine.widgets.inventory_widget import InventoryWidget
    welcome_display.set_text(_("welcome.loading.widgets", game.current_language))
    inventory = InventoryWidget(game.player)
    inventory.is_visible = False
    game.add_widget(inventory)
    
    ## Player's life Widget
    from engine.widgets.player_life_widget import PlayerLifeWidget
    players_life = PlayerLifeWidget(game.player)
    players_life.is_visible = False
    game.add_widget(players_life)

    ## Game Over Widget
    from engine.widgets.game_over_widget import GameOverWidget
    game.game_over_widget = GameOverWidget(game)
    
    ## Inventory Display
    from engine.displays.inventory_display import InventoryDisplay
    inventory_display_name = "InventoryDisplay"
    if inventory_display_name not in game.displays:
        inventory_display = InventoryDisplay(inventory_display_name)
        game.add_display(inventory_display)

    ## Everything is ready
    welcome_display.set_text(_("welcome.loading.done", game.current_language))
    welcome_display.is_ready = True

    

def test_inventory(game, welcome_display):
    import engine.interaction_object
    from engine.player import Player
    player = Player()
    game.player = player

    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/knife.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/knife.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/ananas.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/banana.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/crystal.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/metal.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/rope.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/stone.ini', 0, 0))
    player.inventory.add_item(engine.interaction_object.InteractionObject('conf/wood.ini', 0, 0))

    game.open_inventory()


game = Game()

welcome = WelcomeDisplay()
welcome.draw()
welcome.screen.swap()

game.set_active_display(welcome)
game.start()

loading_thread = threading.Thread(target=load_assets, args=(game, welcome, ))
#loading_thread = threading.Thread(target=test_inventory, args=(game, welcome, ))
loading_thread.start()

# Starts the game loop
stackless.run()
pspmp3.end()
