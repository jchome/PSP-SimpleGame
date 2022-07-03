# -*- coding: iso-8859-1 -*-

from engine.displays.inventory.inventory_item import InventoryItem


class InventoryItemFormula(InventoryItem):
    def __init__(self, metadata = None):
        InventoryItem.__init__(self, metadata)
        self.enough_in_inventory = False
