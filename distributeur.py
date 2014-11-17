# ==============================================================================
"""Distributeur de boissons chaudes"""
# ==============================================================================
__author__ = "Medeville Marion and Rhouzlane Elias"
__version__ = "1.0"
__date__ = "2014-15-11"
# ==============================================================================
#!/bin/python3
from data import boisson, ingredient

class Distributeur():
    """Distributeur de boissons chaudes, nécessite des pièces de monnaie européennes"""
    
    #Tout les distributeurs partagent la même liste de pièce accepté
    erreur = \
    {
        1 : "La monnaie doit être un tuple",
        2 : "Vous devez entrer une valeur pour chaque pièce.",
        3 : "La consommation doit être un tuple",
        4 : "Vous devez entrer une valeur pour chaque conso (si thé est activé, \
            le tuple pourra ne pas contenir de valeur pour la dose de chocolat et de café",
        5 : "Le tuple doit être binaire"
    }
    monnaie_acceptee = ["2Euros", "1Euro", "50Cents", "20Cents", "10Cent", "5Cent"]
    
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
        for ingredient in ingredients.values():
            ingredient.utiliser(cmd[ingredient])
        _ingredients = [(type(ingredient), i, cmd[ingredient]) for i in range(cmd[ingredient]) for ingredient in ingredients.values()]
        print(_ingredients)
            
    def rendre_monnaie(self, monnaie):
        return monnaie
    
    def commander(self, monnaie, commande):
        """Recoit, vérifie et lance la commande"""
        #Je vérifie d'abord si la monnaie respecte les contraintes
        #du distributeur, si oui alors monnaie_accepte sera Vrai
        #sinon il sera Faux
        _order = self.formater_commande(commande)
        ingredients = self.get_ingredients(_order)
        monnaie_accepte = self.verifier_monnaie(monnaie)
        if monnaie_accepte:
            #Si la monnaie est bonne, alors je régarde si je peux
            #trouver une boisson qui correspond à la commande
            #si oui, alors je récupère cette boisson
            boisson = self.correspondance_boisson(ingredients)
            if boisson:
                #Si j'ai récupéré une boisson, alors je calcul
                #le prix de ma commande
                prix = self.get_prix_boisson(_order)
                print("Prix du {} : {} Cents".format(boisson, prix))
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
    machine.commander((1,1,1,1,1,1), (1,1,1,1,1,1))
    print(">>> machine.commande((0,2,1,0,1,0), (0,1,1,0,1,1))", "#Macciato + 1sucre (2.1E)")
    machine.commander((0,2,1,0,1,0), (0,1,1,0,1,1))
    print(">>> machine.commande((1,0,0,0,0,0), (1,0,1,1,0,0))", "#Thé + lait + 2sucres (2.0E)")
    machine.commander((1,0,0,0,0,0), (1,0,1,1,0,0))
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
