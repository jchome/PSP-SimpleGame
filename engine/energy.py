# -*- coding: iso-8859-1 -*-


class Energy():

    def __init__(self, drink = 100, food = 100):
        self.drink = drink
        self.food = food

    def apply_energy(self, energy):
        self.drink += energy.drink
        self.food += energy.food

        if self.drink < 0:
            self.drink = 0
        if self.drink > 100:
            self.drink = 100

        if self.food < 0:
            self.food = 0
        if self.food > 100:
            self.food = 100

    def __str__(self):
        return "Energy(drink = %f, food = %f)" % (self.drink, self.food)


        