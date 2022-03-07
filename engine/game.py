# -*- coding: iso-8859-1 -*-

import stackless
import pspmp3
from time import time

from engine.displays.board import Board
from engine.displays.inventory_display import InventoryDisplay

class Game():
    def __init__(self):
        self.displays = {}
        self.active_display = None
        self.is_finished = False
        self.player = None
        self.widgets = []
        self.lastPad = time()
        self.previous_display = None
    
    def set_active_display(self, display_param):
        ## De-active the current active board 
        if self.active_display is not None:
            self.active_display.active = False
        
        ## If the display is not already loaded
        if type(display_param) is str:
            display_name = display_param
            if display_name not in self.displays:
                ## By default, the display is a board
                display = Board(display_name)
                self.add_display(display)
            else:
                display = self.displays[display_name]
        else:
            display = display_param
            self.add_display(display)

        self.active_display = display
        self.active_display.active = True
        #print("self.active_display : %s" % display.name)


    def start_to_play_with(self, board):
        self.set_active_display(board)
        #pspmp3.end()
        #pspmp3.init(1)
        #pspmp3.load("assets/music/game.mp3")
        #pspmp3.play()

        self.show_widgets()

    def add_display(self, display):
        display.game = self
        self.displays[display.name] = display

    def add_widget(self, widget):
        self.widgets.append(widget)

    def remove_widget(self, widget):
        self.widgets.remove(widget)

    def show_widgets(self, visibility = True):
        for widget in self.widgets:
            widget.is_visible = visibility


    def start(self):
        self.is_finished = False
        stackless.tasklet(self.tasklet_display)() # Creates the agent tasklet


    def open_inventory(self):
        ## Hide all widgets
        self.show_widgets(False)

        inventory_display_name = "InventoryDisplay"
        if inventory_display_name not in self.displays:
            inventory_display = InventoryDisplay(inventory_display_name)
        else:
            inventory_display = self.displays[inventory_display_name]

        self.previous_display = self.active_display
        self.add_display(inventory_display)
        self.set_active_display(inventory_display_name)


    def close_inventory(self):
        self.set_active_display(self.previous_display)
        self.show_widgets()
        
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

            ## Loop the music
            #if pspmp3.endofstream():
            #    pspmp3.play()

            # Update the instance
            self.active_display.update()

            # Update the widgets
            for widget in self.widgets:
                if widget.is_visible:
                    widget.update()

            # Draw the instance
            self.active_display.draw()

            # At the end, draw the widgets (to be on top of all sprites)
            for widget in self.widgets:
                if widget.is_visible:
                    widget.draw()

            ## Everything is draw
            self.active_display.screen.swap()

            # Give other tasklets its turn
            stackless.schedule()
            