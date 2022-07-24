# -*- coding: iso-8859-1 -*-

from engine.widgets.actions_on_agent import ActionsOnAgent
from engine.widgets.controls_widget import Button

import engine.translation
_ = engine.translation.translate

class ActionsOnBonus(ActionsOnAgent):
    def __init__(self):
        ActionsOnAgent.__init__(self, "Bonus")
        self.add_action(Button.TRIANGLE, "action.on_bonus.take", self.take)
        self.add_action(Button.CIRCLE, "action.on_simple_object.cancel", self.cancel)

    def take(self, player, action, simple_object):
        player.life.apply_energy(simple_object.bonus)
        player.current_board.remove_agent(simple_object)
        player.close_controls_widget()
        
    def cancel(self, player, action, simple_object):
        player.close_controls_widget()

