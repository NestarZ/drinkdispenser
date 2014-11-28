#!/bin/python3
# -*- coding: utf-8 -*-
try:
    from .distrib_usine import Distributeur
except (ImportError, SystemError) as e:
    from .distrib_usine import Distributeur

# MODES DE LA MACHINE


class DistributeurFonctionnement(Distributeur):

    exception = lambda fct: \
        Exception('Action {} indisponnible en mode fonctionnement'.format(fct))
    state = 'Distributeur en mode fonctionnement'

    def __new__(cls, other):
        """Change la classe d'un objet distributeur en
        classe DistributeurFonctionnement"""

        assert isinstance(other, Distributeur), \
            'Seul un distributeur peut etre bascule en mode fonctionnement.'
        other.__class__ = DistributeurFonctionnement
        return other

    def __init__(self, other=None):
        pass

    def __str__(self):
        return type(self).state

    def changer_prix_unitaire(self, item, prix):
        raise type(self).exception('changer_prix_unitaire')

    def prix_unitaire(self, item):
        raise type(self).exception('prix_unitaire')

    def set_max_stock(self, item, max_stock):
        raise type(self).exception('set_max_stock')

    def reset(self):
        raise type(self).exception('reset')

    def vider_caisse(self):
        raise type(self).exception('vider_caisse')

    def get_stock(self, item):
        raise type(self).exception('get_stock')

    def get_all_stock(self):
        raise type(self).exception('get_all_stock')

    def remplir_stock(self, item):
        raise type(self).exception('remplir_stock')

    def remplir_tout_stock(self):
        raise type(self).exception('remplir_tout_stock')

    def ajouter_stock(self, niveau):
        raise type(self).exception('ajout_stock')

    def hitorique(self):
        raise type(self).exception('hitorique')


class DistributeurMaintenance(Distributeur):

    exception = lambda fct: \
        Exception('Action {} indisponnible en mode maintenance'.format(fct))
    state = 'Distributeur en mode maintenance'

    def __new__(cls, other):
        """Change la classe d'un objet Distributeur en classe
        DistributeurMaintenance et au lieu de creer un tout nouveau
        distributeur, il modifie juste la nature de l'objet en parametre
        et le definit comme un objet DistributeurMaintenance.
        """

        assert isinstance(other, Distributeur), \
            'Seul un distributeur peut etre bascule en mode maintenance.'
        other.__class__ = DistributeurMaintenance
        return other

    def __init__(self, other=None):
        pass

    def __str__(self):
        return type(self).state

    def verifier_commande(self, cmd):
        raise type(self).exception('verifier_commande')

    def formater_commande(self, cmd):
        raise type(self).exception('formater_commande')

    def get_boites(self, cmd):
        raise type(self).exception('get_boites')

    def verifier_monnaie(self, monnaie):
        raise type(self).exception('verifier_monnaie')

    def verifier_rendu_monnaie_possible(self, monnaie, prix):
        raise type(self).exception('verifier_rendu_monnaie_possible')

    def correspondance_boisson(self, boites):
        raise type(self).exception('correspondance_boisson')

    def get_prix_boisson(self, cmd):
        raise type(self).exception('get_prix_boisson')

    def verifier_stock_suffisant(self):
        raise type(self).exception('verifier_stock_suffisant')

    def preparer_commande(
        self,
        boites,
        cmd,
        boisson,
    ):
        raise DistributeurFonctionnement.exception('preparer_commande')

    def rendre_monnaie(self, monnaie):
        raise DistributeurFonctionnement.exception('rendre_monnaie')

    def commander(self, monnaie, commande):
        raise DistributeurFonctionnement.exception('commander')
