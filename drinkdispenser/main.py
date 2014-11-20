# ==============================================================================
"""Distributeur de boissons chaudes"""
# ==============================================================================
__author__ = "Medeville Marion and Rhouzlane Elias"
__version__ = "1.0"
__date__ = "2014-15-11"
# ==============================================================================
from data.distrib_usine import Distributeur
from data.distrib_mode import DistributeurMaintenance
from data.distrib_mode import DistributeurFonctionnement
import unittest

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
        prix = {0:0, 1:100}
        for produit in machine.ingredients:
            machine.changer_prix_unitaire(produit, prix)
            self.assertEqual(prix, machine.prix_unitaire(produit))
            
        prix = 50
        for produit in machine.ingredients:
            machine.changer_prix_unitaire(produit, prix)
            prix_unitaire = machine.prix_unitaire(produit)
            self.assertEqual(prix, prix_unitaire[1])
            self.assertEqual({0:0, 1:prix}, prix_unitaire)

    def test_commander(self):
        machine = Distributeur()
        machine.remplir_tout_stock()
        boisson, monnaie = machine.commander((1,1,1,1,1,1), (1,1,1,1,1,1))

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

def main():
##    print(">>> machine = Distributeur()","#Creation de la machine")
##    machine = Distributeur()
##    print(">>> machine.remplir_tout_stock()","#Remplissage des stocks")
##    machine.remplir_tout_stock()
##    print(">>> machine.commande((1,1,1,1,1,1), (1,1,1,1,1,1))")
##    machine.commander((1,1,1,1,1,1), (1,1,1,1,1,1))
##    print(">>> machine.commande((0,2,1,0,1,0), (0,1,1,0,1,1))")
##    machine.commander((0,2,1,0,1,0), (0,1,1,0,1,1))
##    print(">>> machine.commande((1,0,0,0,0,0), (1,0,1,1,0,0))")
##    machine.commander((1,0,0,0,0,0), (1,0,1,1,0,0))
##    print(">>> print(machine)")
##    print(machine)
##    print(">>> machine = maintenance(machine)")
##    machine = maintenance(machine)
##    print(">>> print(machine)")
##    print(machine)
##    print(">>> machine = mise_en_service(machine)")
##    machine = mise_en_service(machine)
##    print(">>> print(machine)")
##    print(machine)
    pass
if __name__ == "__main__":
    main()
    unittest.main()
