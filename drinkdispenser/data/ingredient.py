#!/bin/python3
class Ingredient:

    def __repr__(self):
        return type(self).nom

    def __self__(self):
        return type(self).nom


class Cafe(Ingredient):
    nom = "café"


class The(Ingredient):
    nom = "thé"


class Chocolat(Ingredient):
    nom = "chocolat"


class Lait(Ingredient):
    nom = "lait"


class Sucre(Ingredient):
    nom = "sucre"
