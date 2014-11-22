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
            stock_size = machine.get_stock_size(produit)
            stock_max_size = machine.get_stock_max(produit)
            self.assertEqual(stock_size, stock_max_size)

    def test_remplir_stock(self):
        machine = Distributeur()
        for produit in machine.ingredients:
            machine.remplir_stock(produit)
            stock_size = machine.get_stock_size(produit)
            stock_max_size = machine.get_stock_max(produit)
            self.assertEqual(stock_size, stock_max_size)

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

        # Prix pour des doses inférieurs à 3 (!=0) non déf.
        prix = {3: 10, 4: 20}
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

    def test_commander(self):
        machine = Distributeur()
        machine.remplir_tout_stock()
        with self.assertRaises(AssertionError) as cm:
            boisson, monnaie = machine.commander(
                (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        machine.changer_prix_unitaire("Thé", 10)
        machine.changer_prix_unitaire("Lait", 5)
        machine.changer_prix_unitaire("Sucre", {1: 5, 2: 5, 3: 15})
        print(machine.tarifs)
        boisson, monnaie = machine.commander(
            (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        from data.boisson import The
        self.assertIsInstance(boisson, The)

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

    def test_statistiques(self):
        machine = Distributeur()
        machine.reset()
        machine.remplir_tout_stock()
        machine.changer_prix_unitaire("Café", 10)
        machine.changer_prix_unitaire("Chocolat", 5)
        machine.changer_prix_unitaire("Thé", 10)
        machine.changer_prix_unitaire("Lait", 5)
        machine.changer_prix_unitaire("Sucre", {1: 5, 2: 5, 3: 15})
        boisson, monnaie = machine.commander(
            (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        machine.statistiques()
        boisson, monnaie = machine.commander(
            (1, 1, 1, 1, 1, 1), (1, 0, 0, 0, 1, 1))
        machine.statistiques()
        boisson, monnaie = machine.commander(
            (1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 1, 0))
        machine.statistiques()
        boisson, monnaie = machine.commander(
            (1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1))
        machine.statistiques()


def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), \
        "Le parametre n'est pas un distributeur."
    assert not distributeur.commande_en_cours, "La machine traite une commande"
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
