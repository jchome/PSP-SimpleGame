# -*- coding: iso-8859-1 -*-


import psp2d

class Display:

    def __init__(self, name):
        self.screen = psp2d.Screen()
        self.name = name
        self.game = None
        self.active = False
        self.debug = False


    def exit(self):
        # When the player calls the exit, tell all Agents to stop running
        self.active = False
        if self.game is not None:
            self.game.is_finished = True

    def update(self):
        pass


    def draw(self):
        pass
