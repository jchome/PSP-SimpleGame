# -*- coding: iso-8859-1 -*-

from time import sleep
import psp2d

from engine.displays.selection_display import SelectionDisplay
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper

import engine.translation
_ = engine.translation.translate

class MenuItem():
    MENU_ITEM_WIDTH = 330
    MENU_ITEM_HEIGHT = 54

    def __init__(self, label):
        self.label = label
        self.is_selected = False

        #### Set these values using setters after init
        ## Sprite to display
        self.background = None
        self.font = None
        self.text_height = 0
        self.pox_y = 0

    def draw(self, screen, lang):
        pos_x = (MAX_WIDTH - MenuItem.MENU_ITEM_WIDTH) / 2
        screen.blit(self.background, 0, 0, MenuItem.MENU_ITEM_WIDTH, MenuItem.MENU_ITEM_HEIGHT, pos_x, self.pos_y - 5, True)
        label = _(self.label, lang)
        if self.is_selected:
            label = "> " + label + " <"
        pos_x = (MAX_WIDTH - self.font.textWidth(label)) / 2
        self.font.drawText(screen, pos_x, self.pos_y, label)

class Menu(SelectionDisplay):

    def __init__(self, name, options):
        SelectionDisplay.__init__(self, name)

        (self.background, _) = helper.load_sprite("assets/displays/background-menu.png", 
            MAX_WIDTH, MAX_HEIGHT)
        (menu_bg, _) = helper.load_sprite("assets/displays/parchment.png", 
            MenuItem.MENU_ITEM_WIDTH, MenuItem.MENU_ITEM_HEIGHT)

        self.items = []
        for option in options:
            item = MenuItem(option)
            self.items.append(item)

        menu_font = psp2d.Font('fonts/font-Karumbi-46-black.png')
        text_height = menu_font.textHeight("Sample Text")
        pos_y = (MAX_HEIGHT - text_height) / (len(self.items) + 1)
        ## Keep the same instance for all items
        i = 1
        for item in self.items:
            item.background = menu_bg
            item.font = menu_font
            item.text_height = text_height
            item.pos_y = ((pos_y + 20) * i ) - 40
            i = i + 1

        ## By default, select the first item
        self.items[0].is_selected = True
        self.user_choice_index = 0
        self.play_board = None

    """
    To override
    """
    def on_select(self, option_value):
        pass


    def update_for_selection(self, controller0):
        controller = psp2d.Controller()
        ## Slow down the update
        if self.first_display:
            self.first_display = False
            sleep(0.5)
            return

        ## The update method is called only for active displays
        ## Move up / down
        if controller.down:
            self.update_selection( (self.user_choice_index + 1) % len(self.items) )
        elif controller.up:
            self.update_selection( (self.user_choice_index - 1) % len(self.items) )
        
        #print("self.user_choice: %d" % self.user_choice)
        ## Choice is done with the CROSS button
        elif controller.cross:
            self.on_select(self.items[self.user_choice_index].label)
    
    def update_selection(self, item_number):
        self.items[self.user_choice_index].is_selected = False
        self.user_choice_index = item_number
        self.items[self.user_choice_index].is_selected = True

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        
        for item in self.items:
            item.draw(self.screen, self.game.current_language)

