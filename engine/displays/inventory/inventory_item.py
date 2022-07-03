# -*- coding: iso-8859-1 -*-

class InventoryItem:
    def __init__(self, metadata = None):
        self.count = 1
        self.metadata = metadata
    
    def increment_counter(self):
        self.count += 1

    def decrement_counter(self):
        self.count -= 1