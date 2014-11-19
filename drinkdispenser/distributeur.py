# ==============================================================================
"""Distributeur de boissons chaudes"""
# ==============================================================================
__author__ = "Medeville Marion and Rhouzlane Elias"
__version__ = "1.0"
__date__ = "2014-15-11"
# ==============================================================================
#!/bin/python3
from copy import copy
import unittest
from data import boisson, ingredient

class Distributeur():
    """Distributeur de boissons chaudes, nécessite des pièces de monnaie européennes"""
    
    #Tout les distributeurs partagent la même liste de pièce accepté
    #ansi que le même dictionnaire d'erreur
    erreur = \
    {
        1 : "La monnaie doit être un tuple",
        2 : "Vous devez entrer une valeur pour chaque pièce.",
        3 : "La consommation doit être un tuple",
        4 : "La commande doit être un tuple à valeur pour chaque ingrédient.",
        5 : "La commande doit être un tuple binaire."
    }
    monnaie_acceptee = ["2Euros", "1Euro", "50Cents", "20Cents", "10Cent", "5Cent"]
    
    def __str__(self):
        #print(Distributeur()) => Distributeur en mode usine
        return "Distributeur en mode usine"
    
    def __init__(self):
        """Construit le distributeur et intégre ses composantes (ingredients, stock, tarifs, caisse)"""
        self.ingredients = {"Cafe": ingredient.Cafe(),
                       "Sucre": ingredient.Sucre(),
                       "Lait": ingredient.Lait(),
                       "Chocolat": ingredient.Chocolat(),
                       "Thé": ingredient.The()}
        self.boissons = {"Cafe": boisson.Cafe,
                    "Capuccino": boisson.Capuccino,
                    "Macciato": boisson.Macciato,
                    "Chocolat": boisson.Chocolat,
                    "Thé": boisson.The}
        self.caisse = tuple(0 for v in Distributeur.monnaie_acceptee)
        self.historique = None

    # Methode Misc.
    @property
    def tarifs(self):
        """Récupère et affiche les prix de chaque ingrédient sous forme de dictionnaire"""
        return {key: ingredient.prix for key, ingredient in self.ingredients.items()}

    @property
    def max_stock(self):
        """Récupère et affiche le stock max de chaque ingrédient sous forme de dictionnaire"""
        return {key: ingredient.max_stock for key, ingredient in self.ingredients.items()}

    @property
    def stock(self):
        """Récupère et affiche le stock max de chaque ingrédient sous forme de dictionnaire"""
        return {key: ingredient.stock for key, ingredient in self.ingredients.items()}

    #Methodes du mode maintenance
    def changer_prix_unitaire(self, item, prix):
        """Change le prix unitaire d'un ingrédient"""
        self.ingredients[item].prix = prix

    def prix_unitaire(self, item):
        """Retourne le prix unitaire d'un ingrédient"""
        return self.ingredients[item].prix

    def set_max_stock(self, item, max_stock):
        """Determine le stock maximum d'un ingrédient"""
        self.ingredients[item].max_stock = max_stock

    def reset(self):
        """Remet la machine dans son état sortie d’usine (ne réinitialise pas l’historique)"""
        hitorique = self.historique; self.__init__(); self.historique = hitorique

    def vider_caisse(self):
        """Vide la caisse : Met à zero le nombre de chaque pièce"""
        self.caisse = tuple(0 for v in self.caisse)

    def get_stock(self, item):
        """Retourne le stock d'un ingrédient"""
        return self.ingredients[item].stock

    def get_all_stock(self):
        """Retourne le stock de tout les ingrédients"""
        return {key: ingredient.stock for key, ingredient in self.ingredients.items()}

    def remplir_stock(self, item):
        """Remplit au maximum le stock d'un ingrédient"""
        self.ingredients[item].stock = self.ingredients[item].max_stock

    def remplir_tout_stock(self):
        """Remplit au maximum le stock de tout les ingrédients"""
        for ingredient in self.ingredients.values():
            ingredient.stock = ingredient.max_stock

    def ajouter_stock(self, niveau):
        """Remplit le stock d'un ingrédient jusqu'à un certain niveau"""
        if niveau in range(self.ingredients[item].stock, self.ingredients[item].max_stock+1):
            self.ingredients[item].stock = niveau 

    def hitorique(self):
        """Affiche l'historique du distributeur"""
        return self.historique

    #Methodes du mode fonctionnement
    def verifier_commande(self, cmd):
        """Vérifie puis formate le tuple binaire pour l'adapter à la machine"""
        assert isinstance(cmd, tuple), Distributeur.erreur[3]
        assert len(cmd) == len(self.ingredients)+1, Distributeur.erreur[4]
        assert not False in (isinstance(i, int) and i in range(0,2) for i in cmd), Distributeur.erreur[5]
        return True
    
    def formater_commande(self, cmd):
        """Vérifie puis formate le tuple binaire pour l'adapter à la machine"""
        sucre = int('{}{}'.format(cmd[0], cmd[1]), 2)
        is_the = cmd[3] == 1
        return {self.ingredients["Sucre"]: sucre,
                self.ingredients["Lait"]: cmd[2],
                self.ingredients["Thé"]: cmd[3],
                self.ingredients["Cafe"]: cmd[4] if not is_the else 0,
                self.ingredients["Chocolat"]: cmd[5] if not is_the else 0}
    
    def get_ingredients(self, cmd):
        """Récupère (seulement) les ingrédients commandés et les retournent"""
        return {nom:produit for nom, produit in self.ingredients.items() if cmd[produit] > 0}
    
    def verifier_monnaie(self, monnaie):
        """Vérifie que la machine peut bien encaisser le paiement"""
        assert isinstance(monnaie, tuple), Distributeur.erreur[1]
        assert len(monnaie) == len(Distributeur.monnaie_acceptee), Distributeur.erreur[2]
        return True

    def verifier_rendu_monnaie_possible(self, monnaie, prix):
        return True
    
    def correspondance_boisson(self, ingredients):
        """Recherche une correspondance entre la commande et une boisson, renvoi la boisson si trouvé"""
        #Pour chaque boisson, si une boisson correspond aux
        #ingrédients que je veux utiliser, alors je la retourne
        for boisson in self.boissons.values():
            if boisson.is_ingredients(ingredients.values()):
                return boisson
        return False

    def get_prix_boisson(self, cmd):
        return sum(ing.get_prix(value) for ing, value in cmd.items())
    
    def verifier_stock_suffisant(self):
        """Verifie que les stocks sont sufisamment remplit pour satisfaire la commande"""
        #Pour chaque ingrédient si le stock est inférieur à la
        #demande je retourne faux
        for key, ingredient in self.ingredients.items():
            if ingredient.stock <= self.consommation[key]:
                return False
        return True
    
    def preparer_commande(self, ingredients, cmd, boisson):
        """Utilise les ingrédients nécessaires et demandés pour concevoir la boisson désirée"""
        #Utilise chaque ingrédient demandé pour concocter ma boisson
        boisson = boisson()
        for ingredient in ingredients.values():
            ingredient.utiliser(cmd[ingredient])
            boisson.ajouter_ingredient(ingredient, cmd[ingredient])
        print("Préparation de la commande")
        print("="*5,boisson,"="*5,"\n")
            
    def rendre_monnaie(self, monnaie):
        return monnaie
    
    def commander(self, monnaie, commande):
        """Recoit, vérifie et lance la commande"""
        #Je vérifie d'abord si la monnaie respecte les contraintes
        #du distributeur, si oui alors monnaie_accepte sera Vrai
        #sinon il sera Faux
        commande_acceptee = self.verifier_commande(commande)
        if commande_acceptee:
            _order = self.formater_commande(commande)
            ingredients = self.get_ingredients(_order)
            monnaie_acceptee = self.verifier_monnaie(monnaie)
            if monnaie_acceptee:
                #Si la monnaie est bonne, alors je régarde si je peux
                #trouver une boisson qui correspond à la commande
                #si oui, alors je récupère cette boisson
                boisson = self.correspondance_boisson(ingredients)
                if boisson:
                    #Si j'ai récupéré une boisson, alors je calcul
                    #le prix de ma commande
                    prix = self.get_prix_boisson(_order)
                    print("Prix({})={}C".format('+'.join(ingredients.keys()), prix))
                    #et je regarde si le distributeur peut me rendre
                    #la monnaie (si besoin est)
                    rendu_monnaie_possible = self.verifier_rendu_monnaie_possible(monnaie, prix)
                    if rendu_monnaie_possible:
                        #si je peux rendre la monnaie (si besoin)
                        #alors je prépare la commande et je la propose
                        #au client
                        return self.preparer_commande(ingredients, _order, boisson)
        #Si une de toutes ces vérifications n'est pas valide
        #alors je rend la monnaie
        print("Impossible. Rend la monnaie.")
        return self.rendre_monnaie(monnaie)
    
def maintenance(distributeur):
    assert isinstance(distributeur, Distributeur), "Erreur : Le parametre n'est pas un distributeur."
    if not isinstance(distributeur, DistributeurMaintenance):
        return DistributeurMaintenance(distributeur)
    return distributeur

def mise_en_service(distributeur):
    assert isinstance(distributeur, Distributeur), "Erreur : Le parametre n'est pas un distributeur."
    if not isinstance(distributeur, DistributeurFonctionnement):
        return DistributeurFonctionnement(distributeur)
    return distributeur

# MACHINE
class DistributeurFonctionnement(Distributeur):
    exception = lambda fct : Exception('Action {} indisponnible en mode fonctionnement'.format(fct))
    state = "Distributeur en mode fonctionnement"
    def __new__(cls, other):
        """Change la classe d'un objet distributeur en classe DistributeurFonctionnement"""
        assert isinstance(other, Distributeur), "Seul un distributeur peut être basculé en mode fonctionnement."
        other.__class__ = DistributeurFonctionnement
        return other
    def __init__(self, other=None):
        pass
    def __str__(self):
        return DistributeurFonctionnement.state
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
    def ajouter_stock(self, niveau):
        raise DistributeurFonctionnement.exception('ajout_stock')
    def hitorique(self):
        raise DistributeurFonctionnement.exception('hitorique')

class DistributeurMaintenance(Distributeur):
    exception = lambda fct : Exception('Action {} indisponnible en mode maintenance'.format(fct))
    state = "Distributeur en mode maintenance"
    def __new__(cls, other):
        """Change la classe d'un objet Distributeur en classe DistributeurMaintenance"""
        assert isinstance(other, Distributeur), "Seul un distributeur peut être basculé en mode maintenance."
        other.__class__ = DistributeurMaintenance
        return other
    def __init__(self, other=None):
        pass
    def __str__(self):
        return DistributeurMaintenance.state
    def verifier_commande(self, cmd):
        raise DistributeurFonctionnement.exception('verifier_commande')
    def formater_commande(self, cmd):
         raise DistributeurFonctionnement.exception('formater_commande')   
    def get_ingredients(self, cmd):
        raise DistributeurFonctionnement.exception('get_ingredients')    
    def verifier_monnaie(self, monnaie):
        raise DistributeurFonctionnement.exception('verifier_monnaie')
    def verifier_rendu_monnaie_possible(self, monnaie, prix):
        raise DistributeurFonctionnement.exception('verifier_rendu_monnaie_possible')    
    def correspondance_boisson(self, ingredients):
        raise DistributeurFonctionnement.exception('correspondance_boisson')
    def get_prix_boisson(self, cmd):
        raise DistributeurFonctionnement.exception('get_prix_boisson')    
    def verifier_stock_suffisant(self):
        raise DistributeurFonctionnement.exception('verifier_stock_suffisant')    
    def preparer_commande(self, ingredients, cmd, boisson):
        raise DistributeurFonctionnement.exception('preparer_commande')            
    def rendre_monnaie(self, monnaie):
        raise DistributeurFonctionnement.exception('rendre_monnaie')    
    def commander(self, monnaie, commande):
        raise DistributeurFonctionnement.exception('commander')    
            
if __name__ == "__main__":
    print(">>> machine = Distributeur()","#Creation de la machine")
    machine = Distributeur()
    print(">>> machine.remplir_tout_stock()","#Remplissage des stocks")
    machine.remplir_tout_stock()
    print(">>> machine.commande((1,1,1,1,1,1), (1,1,1,1,1,1))")
    machine.commander((1,1,1,1,1,1), (1,1,1,1,1,1))
    print(">>> machine.commande((0,2,1,0,1,0), (0,1,1,0,1,1))")
    machine.commander((0,2,1,0,1,0), (0,1,1,0,1,1))
    print(">>> machine.commande((1,0,0,0,0,0), (1,0,1,1,0,0))")
    machine.commander((1,0,0,0,0,0), (1,0,1,1,0,0))
    print(">>> print(machine)")
    print(machine)
    print(">>> machine = maintenance(machine)")
    machine = maintenance(machine)
    print(">>> print(machine)")
    print(machine)
    print(">>> machine = mise_en_service(machine)")
    machine = mise_en_service(machine)
    print(">>> print(machine)")
    print(machine)
