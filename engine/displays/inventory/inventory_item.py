# -*- coding: iso-8859-1 -*-

class InventoryItem:
    def __init__(self, agent):
        self.count = 1
        self.metadata = agent.metadata

    def increment_counter(self):
        self.count += 1

    def decrement_counter(self):
        self.count -= 1