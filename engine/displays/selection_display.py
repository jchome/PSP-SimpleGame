# -*- coding: iso-8859-1 -*-

from time import time

from engine.displays.display import Display
import engine.helper as helper

class SelectionDisplay(Display):
    """
    This display is for user-interaction, with arrow keys and selection 
    """

    def __init__(self, name):
        Display.__init__(self, name)
        
        self.last_update = time()
        self.last_keydown = []

    def update(self, controller):
        """
        Do not override this method in subclasses, or call
        SelectionDisplay.update(self, controller) in the subclass
        """
        if not self.active:
            print("This display is not active.")
            return

        if (time() - self.last_update < 0.01):
            return

        ## Step by step key
        keydown = helper.convert_keydown(controller)
        if len(keydown) == 0:
            ## No key pressed
            if len(self.last_keydown) > 0:
                self.update_for_key_released(self.last_keydown)
                self.last_keydown = []
            else:
                self.update_nothing_happens()
            return
        #print("Key down: %s" % keydown)
        if keydown == self.last_keydown and (time() - self.last_update < 0.15):
            ## The key is continuously pressed
            self.update_for_key_pressed(keydown)
            self.last_update = time()
            return
            
        self.last_keydown = keydown
        self.last_update = time()
        self.update_for_selection(controller)

    def update_for_selection(self, controller):
        """
        Override this method to update the display
        """
        pass

    def update_for_key_pressed(self, key):
        """
        Override this method to update the display
        """
        pass

    def update_for_key_released(self, key):
        """
        Override this method to update the display
        """
        pass

    def update_nothing_happens(self):
        """
        Override this method to update the display
        """
        pass
