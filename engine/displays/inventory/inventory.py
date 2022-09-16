# -*- coding: iso-8859-1 -*-

from engine.displays.inventory.inventory_item import InventoryItem


class Inventory:
    """
    Inventory of the player, always used during the gameplay
    """

    def __init__(self):
        self.objects = {}
        self.knowledge = {}
        self.all_items = {}

        ## Default size
        self.limit_size = 4

    def add_item(self, agent):
        """
        Add an item in the inventory
        """

        print("agent.metadata.name=%s" % agent.metadata.name)
        if agent.metadata.category == "OBJECT":
            if agent.metadata.name not in self.objects:
                item = InventoryItem(agent.metadata)
                self.objects[agent.metadata.name] = item
            else:
                item = self.objects[agent.metadata.name]
                item.increment_counter()

        elif agent.metadata.category == "CRAFT":
            if agent.metadata.name not in self.knowledge:
                item = InventoryItem(agent.metadata)
                self.knowledge[agent.metadata.name] = item
            else:
                item = self.knowledge[agent.metadata.name]
                item.increment_counter()

    def size(self):
        """
        Get the size of the inventory, only for objects
        """
        total_size = 0
        for item in self.objects.values():
            total_size += item.count
        return total_size

    def contains(self, item_name, item_counter):
        """
        Check if the inventory has an item, to prepare the craft
        """
        if item_name not in self.objects:
            return False
        item = self.objects[item_name]
        return item.count >= item_counter

    def remove_item(self, item):
        """
        Remove an item from the inventory, only for objects
        """
        if item.metadata.name not in self.objects:
            return
        item_of_inventory = self.objects[item.metadata.name]
        item_of_inventory.count -= item.count
        if item_of_inventory.count == 0:
            del(self.objects[item.metadata.name])