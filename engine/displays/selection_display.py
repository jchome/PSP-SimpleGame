# -*- coding: iso-8859-1 -*-

from time import time

from engine.displays.display import Display
import engine.helper as helper

"""
This display is for user-interaction, with arrow keys and selection 
"""
class SelectionDisplay(Display):

    def __init__(self, name):
        Display.__init__(self, name)
        
        self.last_update = time()
        self.last_keydown = []

    """
    Do not overrride this method in subclasses, or call
    SelectionDisplay.update(self, controller) in the subclass
    """
    def update(self, controller):
        if not self.active:
            print("This display is not active.")
            return

        if (time() - self.last_update < 0.01):
            return

        ## Step by step key
        keydown = helper.convert_keydown(controller)
        if len(keydown) == 0:
            self.update_nothing_happens()
            return
        if keydown == self.last_keydown and (time() - self.last_update < 0.15):
            ## The key is continuously pressed
            self.update_for_key_pressed(keydown)
            self.last_update = time()
            return
            
        self.last_keydown = keydown
        self.last_update = time()
        self.update_for_selection(controller)

    """
    Overrride this method to update the display
    """
    def update_for_selection(self, controller):
        pass


    """
    Overrride this method to update the display
    """
    def update_for_key_pressed(self, key):
        pass
    """
    Overrride this method to update the display
    """
    def update_nothing_happens(self):
        pass
