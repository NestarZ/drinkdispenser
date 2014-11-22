# ====================================================================
"""Distributeur de boissons chaudes"""
# ====================================================================
__author__ = "Medeville Marion and Rhouzlane Elias"
__version__ = "1.0"
__date__ = "2014-15-11"
# ====================================================================
from data.distrib_usine import Distributeur
from data.distrib_mode import DistributeurMaintenance
from data.distrib_mode import DistributeurFonctionnement
import unittest

DEBUG = True


class TestDistributeur(unittest.TestCase):

    def test_unicite(self):
        machine1 = Distributeur()
        machine2 = Distributeur()
        self.assertNotEqual(machine1, machine2)

    def test_remplir_tout_stock(self):
        machine = Distributeur()
        machine.remplir_tout_stock()
        for produit in machine.ingredients:
            stock = machine.get_stock_size(produit)
            stock_max = machine.get_stock_max(produit)
            self.assertEqual(stock, stock_max)

    def test_remplir_stock(self):
        machine = Distributeur()
        for produit in machine.ingredients:
            machine.remplir_stock(produit)
            stock = machine.get_stock_size(produit)
            stock_max = machine.get_stock_max(produit)
            self.assertEqual(stock, stock_max)

    def test_vider_caisse(self):
        machine = Distributeur()
        machine.vider_caisse()
        caisse = machine.caisse
        self.assertEqual(tuple(0 for v in caisse), caisse)
        self.assertEqual(len(caisse), len(machine.monnaie_acceptee))

    def test_changer_prix(self):
        machine = Distributeur()
        prix = {0: 0, 1: 100}
        for produit in machine.ingredients:
            machine.changer_prix_unitaire(produit, prix)
            self.assertEqual(prix, machine.prix_unitaire(produit))

        prix = 50
        for produit in machine.ingredients:
            machine.changer_prix_unitaire(produit, prix)
            prix_unitaire = machine.prix_unitaire(produit)
            self.assertEqual({0: 0, 1: prix}, prix_unitaire)

        prix = {2:10, 3:20}
        for produit in machine.ingredients:
            with self.assertRaises(AssertionError) as cm:
                machine.changer_prix_unitaire(produit, prix)
                prix_unitaire = machine.prix_unitaire(produit)
            the_exception = cm.exception

        prix = "10"
        for produit in machine.ingredients:
            with self.assertRaises(Exception) as cm:
                machine.changer_prix_unitaire(produit, prix)
                prix_unitaire = machine.prix_unitaire(produit)
            the_exception = cm.exception


    def test_correspondance_boisson(self):
        machine = Distributeur()
        commande_the = (0,0,0,1,0,0)
        boisson = machine.correspondance_boisson(commande_the)
        self.assertIsInstance(boisson, The)

    def test_commander(self):
        machine = Distributeur()
        machine.remplir_tout_stock()
        with self.assertRaises(Exception) as cm:
            boisson, monnaie = machine.commander(
                (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))

    def test_mise_en_service(self):
        machine = Distributeur()
        self.assertNotIsInstance(machine, DistributeurFonctionnement)
        mise_en_service(machine)
        self.assertIsInstance(machine, Distributeur)
        self.assertIsInstance(machine, DistributeurFonctionnement)

    def test_mise_en_maintenance(self):
        machine = Distributeur()
        self.assertNotIsInstance(machine, DistributeurMaintenance)
        maintenance(machine)
        self.assertIsInstance(machine, Distributeur)
        self.assertIsInstance(machine, DistributeurMaintenance)


def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), \
        "Erreur : Le parametre n'est pas un distributeur."
    if not isinstance(distributeur, DistributeurMaintenance):
        return DistributeurMaintenance(distributeur)
    return distributeur


def mise_en_service(distributeur):
    assert isinstance(distributeur, Distributeur), \
        "Erreur : Le parametre n'est pas un distributeur."
    if not isinstance(distributeur, DistributeurFonctionnement):
        return DistributeurFonctionnement(distributeur)
    return distributeur

if __name__ == "__main__":
    unittest.main()
    machine = Distributeur()
    print(machine)
    maintenance(machine)
    print(machine)
