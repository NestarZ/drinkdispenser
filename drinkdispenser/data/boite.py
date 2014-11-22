#!/bin/python3
# Boite


class Boite():

    """Boite"""

    error = {
        -1: "Price must be defined for (at least) quantity = 1",
        0: "Dict must be fill of prices for quantities",
        1: "Quantities and prices must be intergers",
        2: "Quantities and prices must be positive intergers",
        3: "Each quantity less than max one must have a price (except 0).",
        4: "Price must be positive",
        5: "Price syntax is not correct, must be int or dict of int",
        6: "Product invalid, must be the same as __type_dingredient_acceptee",
        7: "Must be int less than taille_max and positive",
        8: "Reload only, you can't unload a box",
        9: "New taille_max must be a positive integer",
        10: "Empty box, need reload",
        11: "Not enough stock, need reload"
    }

    def __init__(self, ingredient_type):
        self.__type_dingredient_acceptee = ingredient_type
        self.__taille_max = 100
        self.__boite = []
        self.__taille = len(self.__boite)
        self.__prix_unitaire = {0: 0}

    def __repr__(self):
        """Retourne la boite"""
        return "Boite de {} doses de {} sur un maximum de {}".format(
            self.taille,
            self.type_dingredient_acceptee.nom,
            self.taille_max)

    def __str__(self):
        return self.type_dingredient_acceptee.nom

    def get_prix_unitaire(self, value):
        assert self.prix_unitaire.get(1, False), Boite.error[-1]
        return self.prix_unitaire.get(value, self.prix_unitaire[1] * value)

    @property
    def type_dingredient_acceptee(self):
        return self.__type_dingredient_acceptee

    @property
    def prix_unitaire(self):
        """Retourne le prix unitaire de chaque element de la boite"""
        return self.__prix_unitaire

    @property
    def boite(self):
        """Retourne la boite"""
        return self.__boite

    @property
    def taille_max(self):
        """Retourne la taille maximale de la boite"""
        return self.__taille_max

    @property
    def taille(self):
        """Retourne la taille de la boite"""
        return len(self.__boite)

    @prix_unitaire.setter
    def prix_unitaire(self, value):
        """Fixe le prix unitaire de chaque element de la boite
        (sous condition d'être valide)"""
        if isinstance(value, dict):
            assert value, Boite.error[0]
            assert not False in (
                isinstance(
                    v, int) and isinstance(
                    p, int) for v, p in value.items()), Boite.error[1]
            assert not False in (
                abs(v) == v and abs(p) == p
                for v, p in value.items()), Boite.error[2]
            assert not False in (
                (dose - 1 in value.keys() if not dose in range(
                    0, 2) else True)
                for dose, v in value.items()), Boite.error[3]
            self.__prix_unitaire = value
        elif isinstance(value, int):
            assert abs(value) == value, Boite.error[4]
            self.__prix_unitaire = {0: 0, 1: value}
        else:
            raise Exception(Boite.error[5])
        if not 0 in self.__prix_unitaire:
            self.__prix_unitaire.update({0: 0})

    def recharger_boite(self, type_dingredient, value):
        """Fixe le contenu de la boite"""
        assert type_dingredient is self.__type_dingredient_acceptee, Boite.error[
            6]
        assert ((isinstance(value, int) or isinstance(value, float))
                and int(abs(value)) == value
                and value <= self.taille_max), Boite.error[7]
        assert value >= self.taille, Boite.error[8]
        # Même chose ici, le nouveau Boite doit être inférieur
        # au Boite maximum mais doit être positif et naturel.
        # Encore uen fois, si ce n'est pas le cas,
        # je lève une erreur avec le texte adéquat.
        for i in range(self.taille, value):
            nouvel_ingredient = self.type_dingredient_acceptee()
            self.__boite.append(nouvel_ingredient)

    @taille_max.setter
    def taille_max(self, value):
        """Fixe le Boite max de l'Boite sous condition d'être un Boite max valide"""
        assert isinstance(value, int) and int(
            abs(value)) == value, Boite.error[9]
        # Idem que set_Boite mais pour le Boite maximum avec d'autres
        # contraintes.
        self.__taille_max = value

    def tirer(self, nombre):
        """Utilise l'Boite un nombre de fois détérminé (affecte les Boite)"""
        # Cette méthode (fonction) permet de simuler l'utilisation
        # de l'Boite dans le processus de conception d'une boisson
        # Le paramètre nombre correspond au nombre d'utilisation
        # de l'Boite dans le processus. Par exemple, si je veux 3
        # Sucres, je vais réduire le Boite de 3 sucres. Seulement si
        # le Boite est suffisant. La verif (si le Boite est suffisant
        # ne se fait toutefois pas ici, c'est la machine qui le vérifie).
        assert self.__boite, Boite.error[10]
        assert self.taille > nombre, Boite.error[11]
        print("Stock({}):{} to {}".format(
            self, self.taille, self.taille - nombre))
        return [self.__boite.pop() for i in range(nombre)]


class The:
    nom = "thé"
