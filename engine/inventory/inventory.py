
from engine.inventory.inventory_item import InventoryItem

# -*- coding: iso-8859-1 -*-

class Inventory:
    def __init__(self):
        self.all_items = []

    def add_item(self, agent):
        items_matching = self.find_item(agent)
        if len(items_matching) == 0:
            item = InventoryItem(agent)
            self.all_items.append(item)
        else:
            item = items_matching[0]
            item.increment_counter()

    def find_item(self, agent):
        return [i for i in self.all_items if i.match_with(agent)]
        
    def size(self):
        total_size = 0
        for item in self.all_items:
            total_size += item.count
        return total_size