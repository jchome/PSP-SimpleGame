# -*- coding: iso-8859-1 -*-

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH

import engine.helper as helper


class WelcomeDisplay(Display):

    def __init__(self):
        Display.__init__(self, "Welcome")
        self.debug_font = psp2d.Font('assets/fonts/font-white.png')
        self.text = ""
        self.is_ready = False
        self.menu_display = None

        (self.background, _) = helper.load_sprite("assets/displays/welcome.png", 
            MAX_WIDTH, MAX_HEIGHT)
        self.button_CROSS_asset = psp2d.Image("assets/control-cross.png")


    def set_text(self, text):
        self.text = text


    def update(self, controller):
        if not self.is_ready:
            return
        ## The update method is called only for active displays
        if controller.cross:
            self.game.set_active_display(self.menu_display)
            

    def draw(self):
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        #self.screen.fillRect(0, 0, MAX_WIDTH, MAX_HEIGHT, psp2d.Color(0,0,0,255))

        ## Draw the current debug text
        pos_y = 200
        self.screen.fillRect(100, pos_y, MAX_WIDTH - 200, 16, psp2d.Color(0,0,0,128))
        text_width = self.debug_font.textWidth(self.text)
        pos_x = (MAX_WIDTH - text_width) / 2
        self.debug_font.drawText(self.screen, pos_x, pos_y, self.text)
        
        if self.is_ready:
            pos_y = 220
            pos_x = (MAX_WIDTH - self.debug_font.textWidth("Start")) / 2
            self.screen.blit(self.button_CROSS_asset, 0, 0, 16, 16, pos_x, pos_y, True)
            pos_x += 16
            self.debug_font.drawText(self.screen, pos_x, pos_y + 1, "Start")

        

