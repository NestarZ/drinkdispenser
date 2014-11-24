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
m = Distributeur()


class TestDistributeur(unittest.TestCase):

    def test_unicite(self):
        m1 = Distributeur()
        m2 = Distributeur()
        self.assertNotEqual(m1, m2)

    def test_remplir_tout_stock(self):
        m = Distributeur()
        m.remplir_tout_stock()
        for produit in m.ingredients:
            stock_size = m.get_stock_size(produit)
            stock_max_size = m.get_stock_max(produit)
            self.assertEqual(stock_size, stock_max_size)

    def test_remplir_stock(self):
        m = Distributeur()
        for produit in m.ingredients:
            m.remplir_stock(produit)
            stock_size = m.get_stock_size(produit)
            stock_max_size = m.get_stock_max(produit)
            self.assertEqual(stock_size, stock_max_size)

    def test_vider_caisse(self):
        m = Distributeur()
        m.vider_caisse()
        self.assertEqual(m.caisse.somme, 0)

    def test_changer_prix(self):
        m = Distributeur()
        prix = {0: 0, 1: 100}
        for produit in m.ingredients:
            m.changer_prix_unitaire(produit, prix)
            self.assertEqual(prix, m.prix_unitaire(produit))

        prix = 50
        for produit in m.ingredients:
            m.changer_prix_unitaire(produit, prix)
            prix_unitaire = m.prix_unitaire(produit)
            self.assertEqual({0: 0, 1: prix}, prix_unitaire)

        # Prix pour des doses inférieurs à 3 (!=0) non déf.
        prix = {3: 10, 4: 20}
        for produit in m.ingredients:
            with self.assertRaises(AssertionError) as cm:
                m.changer_prix_unitaire(produit, prix)
                prix_unitaire = m.prix_unitaire(produit)
            the_exception = cm.exception

        prix = "10"
        for produit in m.ingredients:
            with self.assertRaises(Exception) as cm:
                m.changer_prix_unitaire(produit, prix)
                prix_unitaire = m.prix_unitaire(produit)
            the_exception = cm.exception

    def test_commander(self):
        m = Distributeur()
        prev_somme = m.caisse.somme
        m.remplir_tout_stock()
        # with self.assertRaises(AssertionError) as cm:
        #    boisson, monnaie = m.commander(
        #        (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        m.changer_prix_unitaire("thé", 10)
        m.changer_prix_unitaire("lait", 5)
        m.changer_prix_unitaire("sucre", {1: 5, 2: 5, 3: 15})
        boisson = m.commander((0, 0, 0, 0, 2, 3), (1, 1, 1, 1, 1, 1))
        from data.boisson import The
        self.assertIsInstance(boisson, The)
        self.assertEqual(prev_somme, m.caisse.somme - 35)

    def test_correspondance_boisson(self):
        m = Distributeur()
        boisson_cmd = m.trad((1, 1, 1, 1, 1, 1))
        boisson_type, supplements = m.match(boisson_cmd)
        from data.boisson import The
        self.assertEqual(boisson_type, The)
        from data.ingredient import Cafe, Sucre, Lait, Chocolat
        self.assertIn(Sucre, supplements)
        self.assertIn(Lait, supplements)
        self.assertNotIn(Cafe, supplements)
        self.assertNotIn(Chocolat, supplements)

    def test_mise_en_service(self):
        m = Distributeur()
        self.assertNotIsInstance(m, DistributeurFonctionnement)
        mise_en_service(m)
        self.assertIsInstance(m, Distributeur)
        self.assertIsInstance(m, DistributeurFonctionnement)

    def test_mise_en_maintenance(self):
        m = Distributeur()
        self.assertNotIsInstance(m, DistributeurMaintenance)
        maintenance(m)
        self.assertIsInstance(m, Distributeur)
        self.assertIsInstance(m, DistributeurMaintenance)

    @unittest.skip("not now")
    def test_statistiques(self):
        m = Distributeur()
        m.reset()
        m.remplir_tout_stock()
        m.changer_prix_unitaire("Café", 10)
        m.changer_prix_unitaire("Chocolat", 5)
        m.changer_prix_unitaire("Thé", 10)
        m.changer_prix_unitaire("Lait", 5)
        m.changer_prix_unitaire("Sucre", {1: 5, 2: 5, 3: 15})
        boisson, monnaie = m.commander(
            (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        m.statistiques()
        boisson, monnaie = m.commander(
            (1, 1, 1, 1, 1, 1), (1, 0, 0, 0, 1, 1))
        m.statistiques()
        boisson, monnaie = m.commander(
            (1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 1, 0))
        m.statistiques()
        boisson, monnaie = m.commander(
            (1, 1, 1, 1, 1, 1), (0, 0, 1, 0, 1, 1))
        m.statistiques()


def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), \
        "Le parametre n'est pas un distributeur."
    assert not distributeur.commande_en_cours, "La m traite une commande"
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
    m = Distributeur()
    m.changer_prix_unitaire("chocolat", 30)
    m.changer_prix_unitaire("café", 20)
    m.changer_prix_unitaire("thé", 10)
    m.changer_prix_unitaire("lait", 5)
    m.changer_prix_unitaire("sucre", {1: 5, 2: 15, 3: 15})
    unittest.main()
