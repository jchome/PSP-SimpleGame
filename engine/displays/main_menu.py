# -*- coding: iso-8859-1 -*-

from engine.displays.language_menu import LanguageMenu
from engine.displays.menu import Menu

import engine.translation
_ = engine.translation.translate

class MainMenu(Menu):

    def __init__(self):
        Menu.__init__(self, "MainMenu", ["menu.item.play", "menu.item.language", "menu.item.exit"])

    def on_select(self, option_value):
        #print("MainMenu.on_select %s" % option_value)
        if option_value == "menu.item.play":
            self.game.start_to_play_with(self.play_board)
        elif option_value == "menu.item.language":
            ## Open the "LanguageMenu"
            if "LanguageMenu" not in self.game.displays:
                ## Create the language menu
                language_menu = LanguageMenu()
                self.game.set_active_display(language_menu)
            else:
                self.game.set_active_display("LanguageMenu")

        elif option_value == "menu.item.exit":
            self.game.is_finished = True

