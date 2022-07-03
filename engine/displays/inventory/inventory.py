
from engine.displays.inventory.inventory_item import InventoryItem

# -*- coding: iso-8859-1 -*-

class Inventory:
    def __init__(self):
        ## all_items is a dict of
        ##  key = agent.metadata.name
        ##  value = InventoryItem instance
        self.all_items = {}

    def add_item(self, agent):
        if agent.metadata.name not in self.all_items:
            item = InventoryItem(agent.metadata)
            self.all_items[agent.metadata.name] = item
        else:
            item = self.all_items[agent.metadata.name]
            item.increment_counter()
        
    def size(self):
        total_size = 0
        for item in self.all_items.values():
            total_size += item.count
        return total_size
    
    def contains(self, item_name, item_counter):
        if item_name not in self.all_items:
            return False
        item = self.all_items[item_name]
        return item.count >= item_counter

    def remove_item(self, item):
        if item.metadata.name not in self.all_items:
            return
        item_of_inventory = self.all_items[item.metadata.name]
        item_of_inventory.count -= item.count
        if item_of_inventory.count == 0:
            del(self.all_items[item.metadata.name])