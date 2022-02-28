# -*- coding: iso-8859-1 -*-


from engine.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH

import psp2d

class WelcomeDisplay(Display):

    def __init__(self, name):
        Display.__init__(self, name)
        self.font = psp2d.Font('font.png')


    def update(self):
        ## The update method is called only for active displays
        controller = psp2d.Controller()
        if controller.circle:
            print("EXIT")
            self.game.is_finished = True


    def draw(self):
        self.screen.fillRect(0, 0, MAX_WIDTH, MAX_HEIGHT, psp2d.Color(0,0,255,255))
        self.font.drawText(self.screen, 0, 0, "Welcome")
