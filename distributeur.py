# ==============================================================================
"""Distributeur de boissons chaudes"""
# ==============================================================================
__author__ = "Medeville Marion and Rhouzlane Elias"
__version__ = "1.0"
__date__ = "2014-15-11"
# ==============================================================================
#!/bin/python3
from data import boisson, ingredient
#Limite du programme : Ne permet la création simultanée que d'un distributeur
#Sans quoi les stocks, les prix, les stocks maximums, les compositions de boisson
#et leurs statistiques seraient partagés par les différents distributeurs.
#Ce programme est donc idéal seulement s'il est appliqué à
#une seule machine.
#Pour corriger le problème il faudrait lier les stock/prix/stat de chaque
#ingrédient/boisson à chaque instance de distributeur.
class Distributeur():
    """Distributeur de boissons chaudes, nécessite des pièces de monnaie européennes"""
    #Tout les distributeurs partagent la même liste de pièce accepté
    #et ils proposent les mêmes boissons et ingrédients
    monnaie_acceptee = ["2Euros", "1Euro", "50Cents", "20Cents", "10Cent", "5Cent"]
    ingredients = {"Cafe": ingredient.Cafe,
                   "Sucre": ingredient.Sucre,
                   "Lait": ingredient.Lait,
                   "Chocolat": ingredient.Chocolat,
                   "Thé": ingredient.The}
    boissons = {"Cafe": boisson.Cafe,
                "Capuccino": boisson.Capuccino,
                "Macciato": boisson.Macciato,
                "Chocolat": boisson.Chocolat,
                "Thé": boisson.The}
    def __init__(self):
        """Construit le distributeur et intégre ses composantes (ingredients, stock, tarifs, caisse)"""
        self.boissons = Distributeur.boissons
        self.ingredients = Distributeur.ingredients
        self.caisse = tuple(0 for v in Distributeur.monnaie_acceptee)
        self.historique = None

    # Methode Misc.
    @property
    def tarifs(self):
        """Récupère et affiche les prix de chaque ingrédient sous forme de dictionnaire"""
        return {key: ingredient.get_prix() for key, ingredient in self.ingredients.items()}

    @property
    def max_stock(self):
        """Récupère et affiche le stock max de chaque ingrédient sous forme de dictionnaire"""
        return {key: ingredient.get_max_stock() for key, ingredient in self.ingredients.items()}

    #Methodes du mode maintenance
    def changer_prix_unitaire(self, item, prix):
        """Change le prix unitaire d'un ingrédient"""
        self.ingredients[item].set_prix(prix)

    def prix_unitaire(self, item):
        """Retourne le prix unitaire d'un ingrédient"""
        return self.ingredients[item].get_prix()

    def set_max_stock(self, item, max_stock):
        """Determine le stock maximum d'un ingrédient"""
        self.ingredients[item].set_max_stock(max_stock)

    def reset(self):
        """Remet la machine dans son état sortie d’usine (ne réinitialise pas l’historique)"""
        hitorique = self.historique
        self.__init__()
        self.historique = hitorique

    def vider_caisse(self):
        """Vide la caisse : Met à zero le nombre de chaque pièce"""
        self.caisse = tuple(0 for v in self.caisse)

    def get_stock(self, item):
        """Retourne le stock d'un ingrédient"""
        return self.ingredients[item].get_stock()

    def get_all_stock(self):
        """Retourne le stock de tout les ingrédients"""
        return {key: ingredient.get_stock() for key, ingredient in self.ingredients.items()}

    def remplir_stock(self, item):
        """Remplit au maximum le stock d'un ingrédient"""
        self.ingredients[item].set_stock(self.ingredients[item].get_max_stock())

    def remplir_tout_stock(self):
        """Remplit au maximum le stock de tout les ingrédients"""
        for key, ingredient in self.ingredients.items():
            ingredient.set_stock(ingredient.get_max_stock())

    def ajout_stock(self, niveau):
        """Remplit le stock d'un ingrédient jusqu'à un certain niveau"""
        self.ingredients[item].set_stock(niveau if self.ingredients[item].get_stock() <= niveau <= self.ingredients[
            item].get_max_stock() else niveau)

    def hitorique(self):
        """Affiche l'historique du distributeur"""
        return self.historique

    def edition_caisse(self):
        """
        Fournit le contenu de la caisse et la consommation de chaque ingrédient,
        ainsi que des « statistiques » sur les boissons commandées
        """
        conso_ingredients = {key: ingredient.get_max_stock() - ingredient.get_stock() for key, ingredient in
                             self.ingredients.items()}
        conso_boissons = {key: boisson.get_nb_commande() for key, boisson in self.boissons.items()}
        print(repr(conso_ingredients) + repr(conso_boissons))

    #Methodes du mode fonctionnement
    def verif_pieces(self):
        """Vérifie que la machine peut bien encaisser le paiement"""
        return True
    def correspondance_boisson(self):
        """Recherche une correspondance entre la commande et une boisson, renvoi la boisson si trouvé"""
        for boisson in self.boissons.values():
            if boisson.is_ingredients(self.ingredients_a_utiliser):
                return boisson
    def is_enough_stock(self):
        """Verifie que les stocks sont sufisamment remplit pour satisfaire la commande"""
        for key, ingredient in self.ingredients.items():
            if ingredient.get_stock() <= self.consommation[key]:
                return False
        return True
    def preparation_commande(self):
        """Utilise les ingrédients nécessaires et demandés pour concevoir la boisson désirée"""
        for key, ingredient in self.ingredients.items():
            if self.consommation[key] >= 1:
                ingredient.utiliser(self.consommation[key])
    def commande(self, tuple1, tuple2):
        """Recoit, vérifie et lance la commande"""
        self.pieces = tuple1
        self.consommation = tuple2
        boisson = self.correspondance_boisson()
        if self.verif_pieces() and boisson and self.is_enough_stock():
            print("Préparation d'un {}".format(boisson))
            self.preparation_commande()
        else: print("Impossible")
    @property
    def pieces(self):
        return self.__pieces
    @pieces.setter
    def pieces(self, value):
        assert isinstance(value, tuple), "La monnaie doit être un tuple"
        assert len(value) == len(Distributeur.monnaie_acceptee), "Vous devez entrer une valeur pour chaque pièce."
        self.__pieces = value
    @property
    def consommation(self):
        return self.__consommation
    @consommation.setter
    def consommation(self, value):
        """Vérifie puis formate le tuple binaire pour l'adapter à la machine"""
        assert isinstance(value, tuple), "La consommation doit être un tuple"
        assert (len(self.ingredients)+1 >= len(value) >= len(self.ingredients)-1 if value[3]==1 else len(value) == len(self.ingredients)+1), \
        "Vous devez entrer une valeur pour chaque conso (si thé est activé, \
        le tuple pourra ne pas contenir de valeur pour la dose de chocolat et de café."
        assert not False in (val == 0 or val == 1 for val in value), "Le tuple doit être binaire."
        sucre = int(str(value[0])+str(value[1]), 2)
        is_the = value[3] == 1
        self.__consommation = {"Sucre":sucre,
                               "Lait":value[2],
                               "Thé":value[3],
                               "Cafe":value[4] if not is_the else 0,
                               "Chocolat":value[5] if not is_the else 0}
        self.ingredients_a_utiliser = [self.ingredients[nom] for nom, value in self.__consommation.items() if value > 0]
        

def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), "Erreur : Le parametre n'est pas un distributeur."
    if not type(distributeur) is type(DistributeurMaintenance):
        return DistributeurMaintenance()
    return distributeur

def mise_en_service(distributeur):
    assert isinstance(distributeur, Distributeur), "Erreur : Le parametre n'est pas un distributeur."
    assert not isinstance(distributeur, DistributeurMaintenance), "Distributeur en maintenance ne peut être mis en service."
    if not type(distributeur) is type(DistributeurFonctionnement):
        return DistributeurFonctionnement()
    return distributeur

# MACHINE
class DistributeurFonctionnement(Distributeur):
    exception = lambda fct : Exception('Action {} indisponnible en mode Fonctionnement'.format(fct))
    def changer_prix_unitaire(self, item, prix):
        raise DistributeurFonctionnement.exception('changer_prix_unitaire')
    def prix_unitaire(self, item):
        raise DistributeurFonctionnement.exception('prix_unitaire')
    def set_max_stock(self, item, max_stock):
        raise DistributeurFonctionnement.exception('set_max_stock')
    def reset(self):
        raise DistributeurFonctionnement.exception('reset')
    def vider_caisse(self):
        raise DistributeurFonctionnement.exception('vider_caisse')
    def get_stock(self, item):
        raise DistributeurFonctionnement.exception('get_stock')
    def get_all_stock(self):
        raise DistributeurFonctionnement.exception('get_all_stock')
    def remplir_stock(self, item):
        raise DistributeurFonctionnement.exception('remplir_stock')
    def remplir_tout_stock(self):
        raise DistributeurFonctionnement.exception('remplir_tout_stock')
    def ajout_stock(self, niveau):
        raise DistributeurFonctionnement.exception('ajout_stock')
    def hitorique(self):
        raise DistributeurFonctionnement.exception('hitorique')
    def edition_caisse(self):
        raise DistributeurFonctionnement.exception('edition_caisse')

class DistributeurMaintenance(Distributeur):
    exception = lambda fct : Exception('Action {} indisponnible en mode Maintenance'.format(fct))
    def verif_pieces(self):
        raise DistributeurMaintenance.exception('verif_pieces')
    def correspondance_boisson(self):
        raise DistributeurMaintenance.exception('correspondance_boisson')
    def is_enough_stock(self):
        raise DistributeurMaintenance.exception('is_enough_stock')
    def preparation_commande(self):
        raise DistributeurMaintenance.exception('preparation_commande')
    def commande(self, tuple1, tuple2):
        raise DistributeurMaintenance.exception('commande')
    
if __name__ == "__main__":
    print(">>> machine = Distributeur()","#Creation de la machine")
    machine = Distributeur()
    print(">>> machine.remplir_tout_stock()","#Remplissage des stocks")
    machine.remplir_tout_stock()
    print(">>> machine.commande((1,1,1,1,1,1), (1,1,1,1,1,1))", "#Thé + lait + 3sucres (3.85E)")
    machine.commande((1,1,1,1,1,1), (1,1,1,1,1,1))
    print(">>> machine.commande((0,2,1,0,1,0), (0,1,1,0,1,1))", "#Macciato + 1sucre (2.1E)")
    machine.commande((0,2,1,0,1,0), (0,1,1,0,1,1))
    print(">>> machine.commande((1,0,0,0,0,0), (1,0,1,1,0,0))", "#Thé + lait + 2sucres (2.0E)")
    machine.commande((1,0,0,0,0,0), (1,0,1,1,0,0))
    print(">>> print(machine)", "#Type de la variable machine")
    print(machine)
    print(">>> machine_en_maintenance = maintenance(machine)", "#Mise en maintenance de la machine")
    machine_en_maintenance = maintenance(machine)
    print(">>> print(machine_en_maintenance)", "#Type de la variable machine_en_maintenance")
    print(machine_en_maintenance)
    print(">>> machine_en_service = mise_en_service(machine)", "#Mise en service de la machine")
    machine_en_service = mise_en_service(machine)
    print(">>> print(machine_en_service)", "#Type de la variable machine_en_service")
    print(machine_en_service)
