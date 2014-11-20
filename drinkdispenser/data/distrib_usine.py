#!/bin/python3
# -*- coding: utf-8 -*-
try:
    from .ingredient import Cafe, Sucre, Lait, Chocolat, The
    from .boite import Boite
    from . import boisson
except (ImportError, SystemError) as e:
    print("Lancement du fichier distrib_usine en stand-alone")
    from ingredient import Cafe, Sucre, Lait, Chocolat, The
    from boite import Boite
    import boisson
    
# MACHINE MODE USINE

class Distributeur:

    """Distributeur de boissons chaudes, necessite des pieces de monnaie europeennes"""

    # Tout les distributeurs partagent la meme liste de monnaie acceptee
    # ansi que le meme dictionnaire d'erreur

    erreur = {
        1: 'La monnaie doit etre un tuple',
        2: 'Vous devez entrer une valeur pour chaque piece.',
        3: 'La consommation doit etre un tuple',
        4: 'La commande doit etre un tuple a valeur pour chaque boite.',
        5: 'La commande doit etre un tuple binaire.',
        }
    
    monnaie_acceptee = [
        '2Euros',
        '1Euro',
        '50Cents',
        '20Cents',
        '10Cent',
        '5Cent',
        ]

    def __str__(self):

        # machine = Distributeur()
        # print(machine) => Distributeur en mode usine

        return 'Distributeur en mode usine'

    def __init__(self):
        """Construit le distributeur et integre ses composantes
        (boites, stock, tarifs, caisse)"""
        print("Creation d'un distributeur")
        # self.ingredients contient des definitions de chaque ingredient que le
        # distributeur est censé geré.

        self.__ingredients = {
            Cafe.nom: Cafe,
            Sucre.nom: Sucre,
            Lait.nom: Lait,
            Chocolat.nom: Chocolat,
            The.nom: The,
            }

        # self.boites contient des boites (vides) de chaque ingredient que
        # le distributeur est cense gere, ainsi, boite.Lait() correspond a
        # une boite de Lait (vide car les stock ne sont pas initialement remplis)
        # et par exemple la fonction self.boites["Lait"].utiliser(1)
        # me permet de recuperer une dose de Lait de la boite. Et la fonction
        # self.boites["Lait"].ajouter_stock(20) rajoute 20 doses de lait
        # dans la boite de Lait (self.boites["Lait"]).
        
        self.__boites = {ingredient.nom: Boite(ingredient)
                       for ingredient in self.ingredients.values()}
        
        # self.boissons contient les definitions des boissons que le distributeur
        # est cense gere. Par le mot "definition" je veux dire que ce
        # ne sont pas des boissons "physiques" qui sont dans ce dictionnaire.
        # Ils s'agit en fait la recette de la boisson.
        # Si (par exemple) je veux creer deux cafes differents a partir de la recette,
        # je dois faire:
        # recette_du_cafe = self.boissons['Cafe']
        # cafe1 = recette_du_cafe()
        # cafe2 = recette_du_cafe()
        # cafe1 et cafe2 seront donc deux unites distinctes physiquement presentes
        # mais vides en fait cafe1.goblet est vide (resp. cafe2)
        # et si je veux remplir mon cafe je dois faire
        # cafe1.ajouter([Cafe, Sucre])
        # si l'ingredient est conforme a la definition d'un cafe
        # alors l'ingredient sera rajouté dans le goblet,
        # sinon une erreur sera levé.

        self.__boissons = {
            boisson.Cafe.nom: boisson.Cafe,
            boisson.Capuccino.nom: boisson.Capuccino,
            boisson.Macciato.nom: boisson.Macciato,
            boisson.Chocolat.nom: boisson.Chocolat,
            boisson.The.nom: boisson.The,
            }

        # Caisse de monnaie : n-tuple qui correspond à la liste de monnaie_acceptee
        
        self.__caisse = tuple(0 for v in Distributeur.monnaie_acceptee)

        # Historique des commandes envoyées à la machine et les actions
        # qui ont suivies
        
        self.__historique = None

    # Protection des variables en lecture seule pour l'utilisateur
    
    @property
    def caisse(self):
        return self.__caisse
    
    @property
    def historique(self):
        return self.__historique
    
    @property
    def boissons(self):
        return self.__boissons

    @property
    def boites(self):
        return self.__boites
    
    @property
    def ingredients(self):
        return self.__ingredients
    
    # Methodes partagées

    
    @property
    def tarifs(self):
        """Recupere et affiche le prix des elements de
        chaque boite sous forme de dictionnaire"""
        
        return {key: boite.prix_unitaire for key, boite
                in self.boites.items()}

    @property
    def stocks(self):
        """Recupere et affiche chaque boite
        sous forme de dictionnaire"""
        
        return {key: boite for key, boite in self.boites.items()}


    # Methodes du mode maintenance


    def changer_prix_unitaire(self, item, prix):
        """Change le prix unitaire d'un boite"""

        self.boites[item].prix_unitaire = prix


    def prix_unitaire(self, item):
        """Retourne le prix unitaire d'un boite"""

        return self.boites[item].prix_unitaire


    def set_max_stock(self, item, max_stock):
        """Determine le stock maximum d'un boite"""

        self.boites[item].max_stock = max_stock


    def reset(self):
        """Remet la machine dans son etat sortie d'usine
       (ne reinitialise pas l'historique)"""

        hitorique = self.__historique
        self.__init__()
        self.__historique = hitorique


    def vider_caisse(self):
        """Vide la caisse : Met a zero le nombre de chaque piece"""

        self.__caisse = tuple(0 for v in Distributeur.monnaie_acceptee)
        

    def get_stock(self, item):
        """Retourne le stock d'un boite"""

        return self.boites[item]

    def get_stock_size(self, item):
        """Retourne la taille du stock restant d'une boite"""

        return self.boites[item].taille

    def get_stock_max(self, item):
        """Retourne la taille maximum d'une boite"""

        return self.boites[item].taille_max

    def get_all_stock(self):
        """Retourne le stock de tout les boites"""
        
        return {key: boite for key, boite in self.boites.items()}

    def remplir_stock(self, item):
        """Remplit au maximum le stock d'un boite"""

        self.boites[item].recharger_boite(self.ingredients[item],
                                        self.boites[item].taille_max)


    def remplir_tout_stock(self):
        """Remplit au maximum le stock de tout les boites"""

        for boite in self.boites.values():
            boite.recharger_boite(boite.type_dingredient_acceptee,
                                  boite.taille_max)


    def ajouter_stock(self, quantite):
        """Remplit le stock d'un boite jusqu'a un certain niveau"""

        if quantite in range(self.boites[item].taille,
                             self.boites[item].taille_max + 1):
            self.boites[item].recharger_boite(self.ingredients[item],
                    quantite)


    def hitorique(self):
        """Affiche l'historique du distributeur"""

        return self.historique

    #Methodes du mode fonctionnement
    def verifier_commande(self, cmd):
        """Verifie puis formate le tuple binaire pour l'adapter a la machine"""

        assert isinstance(cmd, tuple), Distributeur.erreur[3]
        assert len(cmd) == len(self.boites) + 1, Distributeur.erreur[4]
        assert not False in (isinstance(i, int) and i in range(0, 2)
            for i in cmd), Distributeur.erreur[5]
        return True


    def formater_commande(self, cmd):
        """Verifie puis formate le tuple binaire pour l'adapter a la machine"""

        sucre = int('{}{}'.format(cmd[0], cmd[1]), 2)
        is_the = cmd[3] == 1
        return {
            self.boites[Sucre.nom]: sucre,
            self.boites[Lait.nom]: cmd[2],
            self.boites[The.nom]: cmd[3],
            self.boites[Cafe.nom]: (cmd[4] if not is_the else 0),
            self.boites[Chocolat.nom]: (cmd[5] if not is_the else 0),
            }

    def get_boites(self, cmd):
        """Recupere (seulement) les ingredients commandes et les retournent"""
        return {nom: boite for nom, boite in
                self.boites.items() if cmd[boite] > 0}


    def get_types_ingredient(self, boites):
        return [boite.type_dingredient_acceptee for boite in
                boites.values()]


    def verifier_monnaie(self, monnaie):
        """Verifie que la machine peut bien encaisser le paiement"""

        assert isinstance(monnaie, tuple), Distributeur.erreur[1]
        assert len(monnaie) == len(Distributeur.monnaie_acceptee), \
            Distributeur.erreur[2]
        return True


    def verifier_rendu_monnaie_possible(self, monnaie, prix):
        return monnaie


    def correspondance_boisson(self, type_des_ingredients):
        """Recherche une correspondance entre la commande
        et une boisson, renvoi la boisson si trouve"""

        # Pour chaque boisson, si une boisson correspond aux
        # boites que je veux utiliser, alors je la retourne

        for boisson in self.boissons.values():
            if boisson.is_ingredients(type_des_ingredients):
                return boisson
        return False


    def get_prix_boisson(self, cmd):
        return sum(ing.get_prix_unitaire(value) for (ing, value) in
                   cmd.items())


    def verifier_stock_suffisant(self):
        """Verifie que les stocks sont sufisamment remplit
        pour satisfaire la commande"""

        # Pour chaque boite si le stock est inferieur a la
        # demande je retourne faux

        for (key, boite) in self.boites.items():
            if boite.taille <= self.consommation[key]:
                return False
        return True

    def preparer_commande(
        self,
        boites_a_utiliser,
        cmd,
        boisson,
        ):
        """Utilise les boites necessaires et demandes pour
        concevoir la boisson desiree"""

            # Utilise chaque boite demande pour concocter ma boisson

        print('\nPreparation de la commande')
        boisson = boisson()
        for boite in boites_a_utiliser.values():
            ingredients = boite.tirer(cmd[boite])
            boisson.ajouter(ingredients)
        print('Preparation terminee')
        print('=' * 5, boisson, '=' * 5, '\n')


    def rendre_monnaie(self, monnaie):
        return monnaie


    def commander(self, monnaie, commande):
        """Recoit, verifie et lance la commande"""

            # Je verifie d'abord si la monnaie respecte les contraintes
            # du distributeur, si oui alors monnaie_accepte sera Vrai
            # sinon il sera Faux

        commande_acceptee = self.verifier_commande(commande)
        if commande_acceptee:
            monnaie_acceptee = self.verifier_monnaie(monnaie)
            if monnaie_acceptee:

                    # Si la monnaie est bonne, alors je regarde si je peux
                    # trouver une boisson qui correspond a la commande
                    # si oui, alors je recupere cette boisson

                _order = self.formater_commande(commande)
                boites_a_utiliser = self.get_boites(_order)
                types_dingredient = \
                    self.get_types_ingredient(boites_a_utiliser)
                boisson = self.correspondance_boisson(types_dingredient)
                if boisson:

                        # Si j'ai recupere une boisson, alors je calcul
                        # le prix de ma commande

                    prix = self.get_prix_boisson(_order)
                    print('Prix({})={}C'.format('+'.join(boites_a_utiliser.keys()),
                            prix))

                        # et je regarde si le distributeur peut me rendre
                        # la monnaie (si besoin est)

                    rendu_monnaie_possible = \
                        self.verifier_rendu_monnaie_possible(monnaie, prix)
                    if rendu_monnaie_possible:

                            # si je peux rendre la monnaie (si besoin)
                            # alors je prepare la commande et je la propose
                            # au client

                        return self.preparer_commande(boites_a_utiliser,
                                _order, boisson), rendu_monnaie_possible

            # Si une de toutes ces verifications n'est pas valide
            # alors je rend la monnaie

        print('Impossible. Rend la monnaie.')
        return self.rendre_monnaie(monnaie)

