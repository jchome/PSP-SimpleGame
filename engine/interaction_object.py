# -*- coding: iso-8859-1 -*-

from agent import Agent
from engine.energy import Energy

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
            self.bonus = Energy()
            bonus_definition = config_parser.get("COLLISION", "bonus")
            for item in bonus_definition.split("\n"):
                if len(item.strip()) == 0:
                    continue
                data = item.strip().split("=")
                key = data[0].strip()
                value = int(data[1].strip())
                if key == "water":
                    self.bonus.water = value
                if key == "food":
                    self.bonus.food = value
        