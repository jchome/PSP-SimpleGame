# -*- coding: iso-8859-1 -*-

from time import time

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper

import engine.translation
_ = engine.translation.translate

class MenuItem():
    MENU_ITEM_WIDTH = 330
    MENU_ITEM_HEIGHT = 54

    def __init__(self, enum_value, label):
        self.enum_value = enum_value
        self.is_selected = False
        ## Sprite to display
        self.background = None
        self.font = None
        self.label = label
        self.text_height = 0
        self.pox_y = 0

    def draw(self, screen, lang):
        pos_x = (MAX_WIDTH - MenuDisplay.MENU_ITEM_WIDTH) / 2
        screen.blit(self.background, 0, 0, MenuDisplay.MENU_ITEM_WIDTH, MenuDisplay.MENU_ITEM_HEIGHT, pos_x, self.pos_y - 5, True)
        label = _(self.label, lang)
        if self.is_selected:
            label = "> " + label + " <"
        pos_x = (MAX_WIDTH - self.font.textWidth(label)) / 2
        self.font.drawText(screen, pos_x, self.pos_y, label)

class MenuDisplay(Display):
    PLAY = 0
    CREDITS = 1
    EXIT = 2

    MENU_ITEM_WIDTH = 330
    MENU_ITEM_HEIGHT = 54

    def __init__(self):
        Display.__init__(self, "Menu")

        (self.background, _) = helper.load_sprite("assets/displays/background-menu.png", 
            MAX_WIDTH, MAX_HEIGHT)
        (menu_bg, _) = helper.load_sprite("assets/displays/parchment.png", 
            MenuDisplay.MENU_ITEM_WIDTH, MenuDisplay.MENU_ITEM_HEIGHT)

        item_play = MenuItem(MenuDisplay.PLAY, "menu.item.play")
        item_credits = MenuItem(MenuDisplay.CREDITS, "menu.item.credits")
        item_exit = MenuItem(MenuDisplay.EXIT, "menu.item.exit")
        
        self.items = [item_play, item_credits, item_exit]
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

        item_play.is_selected = True
        self.user_choice_index = 0
        self.play_board = None
        self.first_display_time = None

    def update(self):
        ## Slow down the update feature
        if self.first_display_time is None:
            self.first_display_time = time()
        if time() - self.first_display_time < 0.1:
            return
        self.first_display_time = time()

        ## The update method is called only for active displays
        controller = psp2d.Controller()
        ## Move up / down
        if controller.down:
            self.items[self.user_choice_index].is_selected = False
            self.user_choice_index = (self.user_choice_index + 1) % len(self.items)
            self.items[self.user_choice_index].is_selected = True
        elif controller.up:
            self.items[self.user_choice_index].is_selected = False
            self.user_choice_index = (self.user_choice_index - 1) % len(self.items)
            self.items[self.user_choice_index].is_selected = True
        #print("self.user_choice: %d" % self.user_choice)
        ## Choice is done with the CIRCLE button
        if controller.circle:
            ## Apply the choice
            if self.user_choice_index == MenuDisplay.PLAY:
                self.game.start_to_play_with(self.play_board)
            elif self.user_choice_index == MenuDisplay.CREDITS:
                ## Not yet implemented
                pass
            elif self.user_choice_index == MenuDisplay.EXIT:
                self.game.is_finished = True

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        
        for item in self.items:
            item.draw(self.screen, self.game.current_language)

