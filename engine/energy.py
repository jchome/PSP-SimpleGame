# -*- coding: iso-8859-1 -*-


class Energy():

    def __init__(self):
        self.drink = 100
        self.food = 100

    def take_bonus(self, energy):
        self.drink += energy.drink
        self.food += energy.food
        if self.drink > 100:
            self.drink = 100
        if self.food > 100:
            self.food = 100
        