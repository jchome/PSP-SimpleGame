# -*- coding: iso-8859-1 -*-

from engine.widgets.actions_on_agent import ActionsOnAgent
from engine.widgets.controls_widget import Button

class ActionsOnSimpleObject(ActionsOnAgent):
    def __init__(self):
        ActionsOnAgent.__init__(self, "Object")
        self.add_action(Button.TRIANGLE, "Take", self.take)
        self.add_action(Button.CIRCLE, "Cancel", self.cancel)

    def take(self, player, action, simple_object):
        player.add_to_inventory(simple_object)
        player.current_renderer.remove_agent(simple_object)
        player.close_controls_widget()
        
    def cancel(self, player, action, simple_object):
        player.close_controls_widget()

