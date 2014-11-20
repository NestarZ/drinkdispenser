#!/bin/python3
class Ingredient:
    def __repr__(self):
        return type(self).nom

    def __self__(self):
        return type(self).nom


class Cafe(Ingredient):
    nom = "Café"


class The(Ingredient):
    nom = "Thé"


class Chocolat(Ingredient):
    nom = "Chocolat"


class Lait(Ingredient):
    nom = "Lait"


class Sucre(Ingredient):
    nom = "Sucre"
