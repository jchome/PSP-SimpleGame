# -*- coding: iso-8859-1 -*-

import stackless
from time import time

from engine.board import Board

class Game():
    def __init__(self):
        self.displays = {}
        self.active_display = None
        self.is_finished = False
        self.player = None
        self.widgets = []
        self.lastPad = time()
    
    def set_active_display(self, display_name):
        ## De-active the current active board 
        if self.active_display is not None:
            self.active_display.active = False
        
        ## If the display is not already loaded
        if display_name not in self.displays:
            self.add_display(Board(display_name))

        self.active_display = self.displays[display_name]
        self.active_display.active = True
        #print("self.active_display : %s" % display_name)

    def add_display(self, display):
        display.game = self
        self.displays[display.name] = display

    def add_widget(self, widget):
        self.widgets.append(widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)

    def start(self):
        self.is_finished = False
        stackless.tasklet(self.tasklet_display)() # Creates the agent tasklet

    def open_inventory(self):
        print("open_inventory !!")

    """
    Main action of the agent.
    Run the action() method while the instance is running.
    """
    def tasklet_display(self):
        while not self.is_finished:
            if self.active_display is None:
                print("self.active_display is None")
                return

            if (self.lastPad and time() - self.lastPad < 0.005):
                # To short time between 2 events
                continue
            self.lastPad = time()

            # Update the instance
            self.active_display.update()

            # Update the widgets
            for widget in self.widgets:
                widget.update()

            # Draw the instance
            self.active_display.draw()

            # At the end, draw the widgets (to be on top of all sprites)
            for widget in self.widgets:
                widget.draw()

            ## Everything is draw
            self.active_display.screen.swap()

            # Give other tasklets its turn
            stackless.schedule()
            