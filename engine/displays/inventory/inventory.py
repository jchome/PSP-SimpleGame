
from engine.displays.inventory.inventory_item import InventoryItem

# -*- coding: iso-8859-1 -*-

class Inventory:
    def __init__(self):
        self.all_items = {}

    def add_item(self, agent):
        if agent.metadata.name not in self.all_items:
            item = InventoryItem(agent)
            self.all_items[agent.metadata.name] = item
        else:
            item = self.all_items[agent.metadata.name]
            item.increment_counter()
        
    def size(self):
        total_size = 0
        for item in self.all_items.values():
            total_size += item.count
        return total_size