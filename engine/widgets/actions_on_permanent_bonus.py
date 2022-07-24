# -*- coding: iso-8859-1 -*-

from engine.widgets.actions_on_bonus import ActionsOnBonus

class ActionsOnPermanentBonus(ActionsOnBonus):
    def __init__(self):
        ActionsOnBonus.__init__(self)

    def take(self, player, action, simple_object):
        player.life.apply_energy(simple_object.bonus)
        player.close_controls_widget()
        

