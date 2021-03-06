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

class TestDistributeur(unittest.TestCase):

    def test_unicite(self):
        m1 = Distributeur()
        m2 = Distributeur()
        self.assertNotEqual(m1, m2)

    def test_creation(self):
        m = Distributeur(tarifs={'café':20}, stocks_size={'thé':600})
        self.assertEqual(m.prix_unitaire('café')[1], 20)
        self.assertEqual(m.get_stock_max('café'), 100)
        self.assertEqual(m.get_stock_max('thé'), 600)
        m = Distributeur(stocks_size=700)
        for produit in m.ingredients:
            self.assertEqual(m.get_stock_max(produit), 700)

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

    def test_max_stock(self):
        m = Distributeur()
        self.assertEqual(m.get_stock_max("thé"), 100)  # 100 valeur par défaut

    def test_set_max_stock(self):
        m = Distributeur()
        m.set_max_stock("thé", 200)
        self.assertEqual(m.get_stock_max("thé"), 200)

    def test_stock(self):
        m = Distributeur()
        self.assertEqual(m.get_stock_size("thé"), 0)

    def test_ajouter_stock(self):
        m = Distributeur()
        m.ajouter_stock("thé", 20)
        self.assertEqual(m.get_stock_size("thé"), 20)

    def test_preparer_commande(self):
        m = Distributeur()
        m.remplir_tout_stock()
        order = m._Distributeur__trad((0, 1, 1, 0, 1, 0))
        from data import boisson
        t_boisson = boisson.Cafe
        from data.ingredient import Lait, Sucre, Cafe
        ingredients = (Sucre, Lait, Cafe)
        ma_boisson = m._Distributeur__preparer_commande(
            order,
            t_boisson,
            ingredients)
        self.assertIsInstance(ma_boisson, boisson.Cafe)
        for elt in ma_boisson.goblet:
            self.assertIn(type(elt), ingredients)

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
        boisson, monnaie2, monnaie1 = m.commander(
                (1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        self.assertIs(boisson, None)
        self.assertEqual(monnaie2.somme, 200)
        self.assertEqual(monnaie1.somme, 185)
        prev_somme = m.caisse.somme
        m.remplir_tout_stock()
        m.changer_prix_unitaire("thé", 10)
        m.changer_prix_unitaire("lait", 5)
        m.changer_prix_unitaire("sucre", {1: 5, 2: 15, 3: 15})
        boisson, monnaie2, monnaie1 = m.commander(
            (0, 0, 0, 0, 2, 3),
            (0, 0, 0, 1, 0, 0))
        from data.boisson import The
        self.assertIsInstance(boisson, The)
        self.assertEqual(prev_somme, m.caisse.somme - (3*5 + 2*10))
        self.assertEqual(monnaie2.somme, (3*5 + 2*10)-(1*10)) #35c - 10c
        self.assertEqual(monnaie1.somme, 0) #monnaie.somme > 2€
        
    def test_correspondance_boisson(self):
        m = Distributeur()
        boisson_cmd = m._Distributeur__trad((1, 1, 1, 1, 1, 1))
        boisson_type, supplements = m._Distributeur__match(boisson_cmd)
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
        with self.assertRaises(Exception) as cm:
            m.edition()
        with self.assertRaises(Exception) as cm:
            m.changer_prix_unitaire("thé", 10)            
            
    def test_mise_en_maintenance(self):
        m = Distributeur()
        self.assertNotIsInstance(m, DistributeurMaintenance)
        maintenance(m)
        self.assertIsInstance(m, Distributeur)
        self.assertIsInstance(m, DistributeurMaintenance)
        with self.assertRaises(Exception) as cm:
            m.commander((0, 0, 0, 0, 2, 3), (0, 0, 0, 1, 0, 0))

    def test_calcul_prix_boisson(self):
        m = Distributeur()
        m.changer_prix_unitaire("chocolat", 30)
        m.changer_prix_unitaire("café", 20)
        m.changer_prix_unitaire("lait", 5)
        m.changer_prix_unitaire("sucre", {1: 5, 2: 5, 3: 15})
        # permet de calculer le prix de la boisson
        order = m._Distributeur__trad((1, 1, 1, 0, 1, 1))
        prix = m._Distributeur__calculer_prix_boisson(order)
        self.assertEqual(prix, 30 + 20 + 5 + 15)

    def test_reset(self):
        m = Distributeur()
        prev_l = m.historique
        prev_c = m.caisse
        m.reset()
        for l in prev_l:
            self.assertIn(l, m.historique)
        for boite in m.caisse:
            self.assertIs(boite.is_empty(), True)
        for boite in m.containers.values():
            self.assertIs(boite.is_empty(), True)

    def test_trad(self):
        m = Distributeur()
        from data.ingredient import Sucre, Cafe, Chocolat, The, Lait
        trad_cmd = m._Distributeur__trad((0, 0, 0, 0, 1, 0))
        self.assertEqual(trad_cmd[Sucre], 0)
        trad_cmd = m._Distributeur__trad((0, 1, 0, 0, 1, 0))
        self.assertEqual(trad_cmd[Sucre], 1)
        trad_cmd = m._Distributeur__trad((1, 0, 0, 0, 1, 0))
        self.assertEqual(trad_cmd[Sucre], 2)
        trad_cmd = m._Distributeur__trad((1, 1, 0, 1, 1, 0))
        self.assertEqual(trad_cmd[Sucre], 3)
        self.assertEqual(trad_cmd[Cafe], 0)
        self.assertEqual(trad_cmd[Chocolat], 0)
        self.assertEqual(trad_cmd[The], 1)
        trad_cmd = m._Distributeur__trad((1, 1, 1, 0, 1, 0))
        self.assertEqual(trad_cmd[Lait], 1)
        self.assertEqual(trad_cmd[Cafe], 1)
        self.assertEqual(trad_cmd[The], 0)

    def test_statistiques(self):
        m = Distributeur()
        m.remplir_tout_stock()
        m.changer_prix_unitaire("café", 10)
        m.changer_prix_unitaire("chocolat", 5)
        m.changer_prix_unitaire("thé", 10)
        m.changer_prix_unitaire("lait", 5)
        m.changer_prix_unitaire("sucre", {1: 5, 2: 5, 3: 15})
        m.commander((1, 1, 1, 1, 1, 1), (1, 1, 1, 1, 1, 1))
        self.assertEqual(m.stats.nb_vendu["Thé"], 1)
        self.assertEqual(m.stats.conso_ingredient["thé"], 1)
        self.assertEqual(m.stats.conso_ingredient["sucre"], 3)
        self.assertEqual(m.stats.conso_ingredient["lait"], 1)
        self.assertEqual(m.stats.conso_ingredient["chocolat"], 0)
        self.assertEqual(m.stats.conso_ingredient["café"], 0)
        self.assertEqual(m.stats.mean_sucre["Thé"], 3)
        m.commander((1, 1, 1, 1, 1, 1), (1, 0, 0, 1, 0, 1))
        self.assertEqual(m.stats.nb_vendu["Thé"], 2)
        self.assertEqual(m.stats.conso_ingredient["thé"], 2)
        self.assertEqual(m.stats.conso_ingredient["sucre"], 5)
        self.assertEqual(m.stats.conso_ingredient["lait"], 1)
        self.assertEqual(m.stats.conso_ingredient["chocolat"], 0)
        self.assertEqual(m.stats.conso_ingredient["café"], 0)
        self.assertEqual(m.stats.mean_sucre["Thé"], 2)
        self.assertEqual(m.stats.with_lait["Thé"], 1)
        self.assertEqual(m.stats.prop_with_lait["Thé"], 50)
        self.assertEqual(m.stats.prop_with_sucre["Thé"], 100)
        m.commander((2, 0, 0, 0, 0, 0), (0, 1, 1, 0, 1, 1))
        self.assertEqual(m.stats.nb_vendu["Macciato"], 1)
        self.assertEqual(m.stats.with_lait["Macciato"], 1)
        self.assertEqual(m.stats.prop_with_lait["Macciato"], 100)
        m.commander((2, 0, 0, 0, 0, 0), (0, 0, 1, 0, 1, 1))
        self.assertEqual(m.stats.nb_vendu["Macciato"], 2)
        self.assertEqual(m.stats.with_lait["Macciato"], 2)
        self.assertEqual(m.stats.mean_sucre["Macciato"], 1)
        self.assertEqual(m.stats.prop_with_lait["Macciato"], 100)
        self.assertEqual(m.stats.prop_with_sucre["Macciato"], 50)


def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), \
        "Le parametre n'est pas un distributeur."
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
    print("Création d'une machine, accessible par la variable \"m\"")
    m = Distributeur()
    print("Lancement des tests sur la machine")
    a = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(TestDistributeur))
    if a.wasSuccessful():
        print("Succès des tests")
        print("Mise en mode maintenance de la machine")
        print("="*30)
        maintenance(m)
        print("Voici la liste des commandes disponnibles en fonctionnement et/ou maintenance")
        print("\n".join([x for x in dir(m) if x[0] != '_']))
        print("-"*30)
        print("mise_en_service(m) permet de mettre en service votre machine")
        print("maintenance(m) permet de mettre en maintenance votre machine")
    else:
        print("Les tests ont échoués")
    
    
