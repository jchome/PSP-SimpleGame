# -*- coding: iso-8859-1 -*-

from engine.displays.inventory.inventory_item import InventoryItem
from engine.helper import debug
from engine.metadata import Metadata


class Inventory:
    """
    Inventory of the player, always used during the gameplay
    """

    def __init__(self):
        self.all_items = { Metadata.CATEGORY_OBJECT: {}, Metadata.CATEGORY_CRAFT: {} }

        ## Default size
        self.limit_size = {Metadata.CATEGORY_OBJECT: 4, Metadata.CATEGORY_CRAFT: 36}

    def add_item(self, agent):
        """
        Add an item in the inventory
        """
        if agent.metadata.category not in self.all_items:
            self.all_items[agent.metadata.category] = {}
        items_of_category = self.all_items[agent.metadata.category]
        if agent.metadata.name not in items_of_category:
            item = InventoryItem(agent.metadata)
            items_of_category[agent.metadata.name] = item
        else:
            item = items_of_category[agent.metadata.name]
            item.increment_counter()

    def size(self):
        """
        Get the size of the inventory, only for objects
        """
        total_size = 0
        if Metadata.CATEGORY_OBJECT in self.all_items:
            for item in self.all_items[Metadata.CATEGORY_OBJECT].values():
                total_size += item.count
        return total_size

    def contains(self, item_name, item_counter):
        """
        Check if the inventory has an item, to prepare the craft
        """
        if Metadata.CATEGORY_OBJECT in self.all_items:
            if item_name not in self.all_items[Metadata.CATEGORY_OBJECT]:
                return False
            item = self.all_items[Metadata.CATEGORY_OBJECT][item_name]
            return item.count >= item_counter
        else:
            return False

    def remove_item(self, item):
        """
        Remove an item from the inventory, only for objects
        """
        if Metadata.CATEGORY_OBJECT in self.all_items:
            if item.metadata.name not in self.all_items[Metadata.CATEGORY_OBJECT]:
                return
            item_of_inventory = self.all_items[Metadata.CATEGORY_OBJECT][item.metadata.name]
            item_of_inventory.count -= item.count
            if item_of_inventory.count == 0:
                del(item_of_inventory[item.metadata.name])
        
