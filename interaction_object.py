# -*- coding: iso-8859-1 -*-

import psp2d
from agent import Agent

"""
Agent base class, mother class of every visible item on the screen.
"""
class InteractionObject(Agent):
    def __init__(self, config_file):
        Agent.__init__(self)
        self.bonus = None
        self.load_config(config_file)
    
    def load_custom_config(self, config_parser):
        if config_parser.has_option("COLLISION", "bonus"):
            self.bonus = config_parser.getint("COLLISION", "bonus")
        