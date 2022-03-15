# -*- coding: iso-8859-1 -*-

from engine.displays.menu import Menu

import engine.translation
_ = engine.translation.translate

class LanguageMenu(Menu):

    def __init__(self):
        Menu.__init__(self, "LanguageMenu", ["menu.item.english", "menu.item.french", "menu.item.back"])

    def on_select(self, option_value):
        #print("MainMenu.on_select %s" % option_value)
        if option_value == "menu.item.french":
            self.game.current_language = "fr"
        elif option_value == "menu.item.english":
            self.game.current_language = "en"
        elif option_value == "menu.item.back":
            self.game.set_active_display("MainMenu")
            

