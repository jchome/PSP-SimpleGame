# -*- coding: iso-8859-1 -*-

import psp2d
from agent import Agent

"""
Agent base class, mother class of every visible item on the screen.
"""
class InteractionObject(Agent):
    def __init__(self, config_file, pos_x = 0, pos_y = 0):
        Agent.__init__(self)
        self.bonus = None
        self.load_config(config_file)
        self.pos_x = pos_x
        self.pos_y = pos_y
    
    def load_custom_config(self, config_parser):
        if config_parser.has_option("COLLISION", "bonus"):
            self.bonus = config_parser.getint("COLLISION", "bonus")
        