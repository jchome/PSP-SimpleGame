# -*- coding: iso-8859-1 -*-

class InventoryItem:
    def __init__(self, agent = None):
        self.count = 1
        if agent is None:
            self.metadata = None
        else:
            self.metadata = agent.metadata
    
    def increment_counter(self):
        self.count += 1

    def decrement_counter(self):
        self.count -= 1