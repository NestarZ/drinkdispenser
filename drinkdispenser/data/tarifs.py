#!/bin/python3
# Boite

DEBUG = False


class Tarifs(object):

    """Tarifs"""

    error = {
        -1: "Price must be defined for (at least) quantity = 1",
        0: "Dict must be fill of prices for quantities",
        1: "Quantities and prices must be intergers",
        2: "Quantities and prices must be positive intergers",
        3: "Each quantity less than max one must have a price (except 0).",
        4: "Price must be positive",
        5: "Price syntax is not correct, must be int or dict of int"
    }

    def __init__(self, nom):
        self.__nom_item = nom
        self.__table = {0: 0}

    @property
    def table(self):
        """Retourne le prix unitaire de chaque ingrédient de la boite"""
        return self.__table

    @table.setter
    def table(self, value):
        """Fixe le prix unitaire de chaque ingrédient de la boite
        (sous condition d'être valide) (dict de prix possible)"""
        if isinstance(value, dict):
            assert value, Boite.error[0]
            assert not False in (
                isinstance(
                    v, int) and isinstance(
                    p, int) for v, p in value.items()), Tarifs.error[1]
            assert not False in (
                abs(v) == v and abs(p) == p
                for v, p in value.items()), Tarifs.error[2]
            assert not False in (
                (dose - 1 in value.keys() if not dose in range(
                    0, 2) else True)
                for dose, v in value.items()), Tarifs.error[3]
            self.__table = value
        elif isinstance(value, int):
            assert abs(value) == value, Tarifs.error[4]
            self.__table = {0: 0, 1: value}
        else:
            raise Exception(Tarifs.error[5])
        if not 0 in self.__table:
            self.__table.update({0: 0})

    def get_table(self, value):
        if value == 0:
            return self.table[0]
        assert self.table.get(1, False), Tarifs.error[-1]
        return self.table.get(value, self.table[1] * value)
