# -*- coding: iso-8859-1 -*-

from engine.renderer import Render
import stackless
import psp2d

class Game():
    def __init__(self):
        self.renderers = {}
        self.active_renderer = None
        self.is_finished = False
        self.player = None
        self.widgets = []
    
    def set_active_renderer(self, renderer_name):
        ## De-active the current active renderer 
        if self.active_renderer is not None:
            self.active_renderer.active = False
        
        ## If the renderer is not already loaded
        if renderer_name not in self.renderers:
            self.add_renderer(Render(renderer_name))

        self.active_renderer = self.renderers[renderer_name]
        self.active_renderer.active = True
        #print("self.active_renderer : %s" % renderer_name)

    def add_renderer(self, renderer):
        renderer.game = self
        self.renderers[renderer.name] = renderer

    def add_widget(self, widget):
        self.widgets.append(widget)

    def start(self):
        self.is_finished = False
        stackless.tasklet(self.tasklet_renderer)() # Creates the agent tasklet

    """
    Main action of the agent.
    Run the action() method while the instance is running.
    """
    def tasklet_renderer(self):
        pad = psp2d.Controller()
        while not self.is_finished:
            if pad.circle:
                print("exit")
                self.exit()

            if self.active_renderer is None:
                print("self.active_renderer is None")
                return

            # Update the instance
            self.active_renderer.update()

            # Update the widgets
            for widget in self.widgets:
                widget.update()

            # Draw the instance
            self.active_renderer.draw()

            # At the end, draw the widgets (to be on top of all sprites)
            for widget in self.widgets:
                if widget.visible:
                    widget.draw()

            ## Everything is draw
            self.active_renderer.screen.swap()

            # Give other tasklets its turn
            stackless.schedule()