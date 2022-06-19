# -*- coding: iso-8859-1 -*-

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH

import engine.helper as helper


class WelcomeDisplay(Display):

    def __init__(self):
        Display.__init__(self, "Welcome")
        self.debug_font = psp2d.Font('font.png')
        self.text = ""
        self.is_ready = False
        self.menu_display = None

        (self.background, _) = helper.load_sprite("assets/displays/welcome.png", 
            MAX_WIDTH, MAX_HEIGHT)


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
        if self.is_ready:
            self.debug_font.drawText(self.screen, 130, 240, "Press cross to start")

        self.screen.fillRect(0, 0, 250, 16, psp2d.Color(0,0,0,128))
        self.debug_font.drawText(self.screen, 0, 0, self.text)
