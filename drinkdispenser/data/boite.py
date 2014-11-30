#!/bin/python3
# Boite

DEBUG = False


class Boite(object):

    """Boite"""

    error = {
        6: "Item invalid, must be the same as __type_ditem",
        7: "Must be int less than taille_max and positive",
        8: "Reload only, you can't unload a box",
        9: "New taille_max must be a positive integer",
        10: "Empty box, need reload",
        11: "Not enough stock, need reload"
    }

    item_name = 'item'

    def __init__(self, item_type, max_size):
        self.__type_ditem = item_type
        self.taille_max = max_size
        self.__boite = []

    def __repr__(self):
        """Retourne la boite"""
        return "Boite({}/{} {} de {})".format(
            self.taille,
            self.taille_max,
            type(self).item_name,
            self.type_ditem.nom)

    def __str__(self):
        return self.type_ditem.nom

    def __len__(self):
        return len(self.__boite)

    @property
    def type_ditem(self):
        return self.__type_ditem

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

    def recharger(self, value):
        """Recharge le contenu de la boite jusqu'à une certaine quantité"""
        assert ((isinstance(value, int) or isinstance(value, float))
                and int(abs(value)) == value
                and value <= self.taille_max), Boite.error[7]
        assert value >= self.taille, Boite.error[8]
        # Même chose ici, le nouveau Boite doit être inférieur
        # au Boite maximum mais doit être positif et naturel.
        # Encore uen fois, si ce n'est pas le cas,
        # je lève une erreur avec le texte adéquat.
        for i in range(self.taille, value):
            nouvel_item = self.type_ditem()
            self.__boite.append(nouvel_item)

    @taille_max.setter
    def taille_max(self, value):
        """Fixe la taille max de la boite sous condition d'être une taille max valide"""
        assert isinstance(value, int) and int(
            abs(value)) == value, Boite.error[9]
        # Idem que set_Boite mais pour le Boite maximum avec d'autres
        # contraintes.
        self.__taille_max = value

    def tirer(self, nombre):
        """Utilise l'ingrédient un nombre de fois détérminé"""
        # Cette méthode (fonction) permet de simuler l'utilisation
        # de l'Boite dans le processus de conception d'une boisson
        # Le paramètre nombre correspond au nombre d'utilisation
        # de l'Boite dans le processus. Par exemple, si je veux 3
        # Sucres, je vais réduire le Boite de 3 sucres. Seulement si
        # le Boite est suffisant. La verif (si le Boite est suffisant
        # ne se fait toutefois pas ici, c'est la machine qui le vérifie).
        if nombre == 0:
            return []
        assert self.__boite, Boite.error[10]
        assert self.taille > nombre, Boite.error[11]
        if DEBUG:
            print("Stock({}):{} to {}".format(
                self, self.taille, self.taille - nombre))
        return [self.__boite.pop() for i in range(nombre)]

    def is_empty(self):
        return len(self) == 0


class BoitePiece(Boite):
    item_name = 'pièce(s)'

    def vider(self):
        self.__boite = []


class BoiteProduit(Boite):
    item_name = 'dose(s)'
