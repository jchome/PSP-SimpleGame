# -*- coding: iso-8859-1 -*-

from time import time

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper

import engine.translation
_ = engine.translation.translate

class MenuDisplay(Display):
    PLAY = 0
    CREDITS = 1
    EXIT = 2

    def __init__(self):
        Display.__init__(self, "Menu")

        (self.background, _) = helper.load_sprite("assets/displays/menu.png", 
            MAX_WIDTH, MAX_HEIGHT)
        self.choices = [MenuDisplay.PLAY, MenuDisplay.CREDITS, MenuDisplay.EXIT]
        self.user_choice = MenuDisplay.PLAY
        self.play_board = None
        self.menu_font = psp2d.Font('fonts/font-Karumbi-46-black.png')
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
            self.user_choice = (self.user_choice + 1) % len(self.choices)
        elif controller.up:
            self.user_choice = (self.user_choice - 1) % len(self.choices)
        #print("self.user_choice: %d" % self.user_choice)
        ## Choice is done with the CIRCLE button
        if controller.circle:
            ## Apply the choice
            if self.user_choice == MenuDisplay.PLAY:
                self.game.start_to_play_with(self.play_board)
            elif self.user_choice == MenuDisplay.CREDITS:
                ## Not yet implemented
                pass
            elif self.user_choice == MenuDisplay.EXIT:
                self.game.is_finished = True
    
    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        
        label = _("menu.item.play", self.game.current_language)
        if self.user_choice == MenuDisplay.PLAY:
            label = "> " + label + " <"
        pos_x = (MAX_WIDTH - self.menu_font.textWidth(label)) / 2
        pos_y = 50
        self.menu_font.drawText(self.screen, pos_x, pos_y, label)

        label = _("menu.item.credits", self.game.current_language)
        if self.user_choice == MenuDisplay.CREDITS:
            label = "> " + label + " <"
        pos_x = (MAX_WIDTH - self.menu_font.textWidth(label)) / 2
        pos_y = 120
        self.menu_font.drawText(self.screen, pos_x, pos_y, label)

        label = _("menu.item.exit", self.game.current_language)
        if self.user_choice == MenuDisplay.EXIT:
            label = "> " + label + " <"
        pos_x = (MAX_WIDTH - self.menu_font.textWidth(label)) / 2
        pos_y = 190
        self.menu_font.drawText(self.screen, pos_x, pos_y, label)

        ## Draw the user's choice
        #pos_x = 110
        #pos_y = [63, 130, 202][self.user_choice]
        #self.menu_font.drawText(self.screen, pos_x, pos_y, "abc")
