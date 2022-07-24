# -*- coding: iso-8859-1 -*-


class Energy():

    def __init__(self, water = 0, food = 0):
        self.water = water
        self.food = food

    def apply_energy(self, energy):
        self.water += energy.water
        self.food += energy.food

        if self.water < 0:
            self.water = 0
        if self.water > 100:
            self.water = 100

        if self.food < 0:
            self.food = 0
        if self.food > 100:
            self.food = 100

    def __str__(self):
        return "Energy(water = %f, food = %f)" % (self.water, self.food)


        