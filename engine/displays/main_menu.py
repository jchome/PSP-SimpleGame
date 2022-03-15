# -*- coding: iso-8859-1 -*-

from time import time
from engine.displays.menu import Menu

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper

import engine.translation
_ = engine.translation.translate

class MainMenu(Menu):

    def __init__(self):
        Menu.__init__(self, ["menu.item.play", "menu.item.options", "menu.item.exit"])

    def on_select(self, option_value):
        #print("MainMenu.on_select %s" % option_value)
        if option_value == "menu.item.play":
            self.game.start_to_play_with(self.play_board)
        elif option_value == "menu.item.options":
            ## Not yet implemented
            pass
        elif option_value == "menu.item.exit":
            self.game.is_finished = True

