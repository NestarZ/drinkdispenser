#!/bin/python3
# -*- coding: utf-8 -*-
try:
    from .coin import Coins, Coin200, Coin100, Coin50, Coin20, Coin10, Coin5
    from .ingredient import Cafe, Sucre, Lait, Chocolat, The
    from .boite import BoitePiece, BoiteProduit
    from .stats import Stats
    from . import boisson
    from . import get_change
except (ImportError, SystemError) as e:
    print("Lancement du fichier distrib_usine en stand-alone")
    from coin import Coins, Coin200, Coin100, Coin50, Coin20, Coin10, Coin5
    from ingredient import Cafe, Sucre, Lait, Chocolat, The
    from boite import BoitePiece, BoiteProduit
    from stats import Stats
    import boisson
    import get_change

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

    monnaie_acceptee = Coins(Coin200, Coin100, Coin50, Coin20, Coin10, Coin5)
    monnaie_container = Coins(Coin50, Coin20, Coin10, Coin5)
    somme_maximum = Coin200.value

    def __str__(self):

        # machine = Distributeur()
        # print(machine) => Distributeur en mode usine

        return 'Distributeur en mode usine'

    def __init__(self, debug=False):
        """Construit le distributeur et integre ses composantes
        (boites, stock, tarifs, caisse)"""
        self.debug = debug
        if self.debug:
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

        # self.containers contient des boites (vides) de chaque ingredient que
        # le distributeur est cense gere, ainsi, boite.Lait() correspond a
        # une boite de Lait (vide car les stock ne sont pas initialement remplis)
        # et par exemple la fonction self.containers["Lait"].utiliser(1)
        # me permet de recuperer une dose de Lait de la boite. Et la fonction
        # self.containers["Lait"].ajouter_stock(20) rajoute 20 doses de lait
        # dans la boite de Lait (self.containers["Lait"]).

        self.__product_containers = {ingredient.nom: BoiteProduit(ingredient)
                                     for ingredient in self.ingredients.values()}

        self.__change_containers = Coins(Coin50, Coin20, Coin10, Coin5)

        self.__containers = self.__change_containers.get_dict()
        self.__containers.update(self.__product_containers)

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
            boisson.The.nom: boisson.The
        }

        # Caisse de monnaie : n-tuple qui correspond à la liste de
        # monnaie_acceptee

        self.__caisse = Coins(Coin200, Coin100, Coin50, Coin20, Coin10, Coin5)

        # Historique des commandes envoyées à la machine et les actions
        # qui ont suivies

        self.__historique = list()
        self.__stats = Stats(self.__ingredients, self.__boissons)
        self.commande_en_cours = False

    def mode(name):
        def hist_decorate(func):
            def func_wrapper(self, *args, **kwargs):
                self.historique.append({func: (args, kwargs)})
                return func(self, *args, **kwargs)
            return func_wrapper
        return hist_decorate

    # Protection des variables en lecture seule pour l'utilisateur
    @property
    def stats(self):
        return self.__stats

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
    def containers(self):
        return self.__containers

    @property
    def product_containers(self):
        return self.__product_containers

    @property
    def change_containers(self):
        return self.__change_containers

    @property
    def ingredients(self):
        return self.__ingredients

    # Methodes partagées

    @property
    def tarifs(self):
        """Recupere et affiche le prix des elements de
        chaque boite sous forme de dictionnaire"""

        return {key: boite.prix_unitaire for key, boite
                in self.product_containers.items()}

    @property
    def stocks(self):
        """Recupere et affiche chaque boite
        sous forme de dictionnaire"""

        return {key: boite for key, boite in self.containers.items()}

    # Methodes du mode maintenance
    @mode("maintenance")
    def changer_prix_unitaire(self, item, prix):
        """Change le prix unitaire d'un boite"""

        self.product_containers[item].prix_unitaire = prix

    @mode("maintenance")
    def prix_unitaire(self, item):
        """Retourne le prix unitaire d'un boite"""

        return self.product_containers[item].prix_unitaire

    @mode("maintenance")
    def set_max_stock(self, item, max_stock):
        """Determine le stock maximum d'un boite"""

        self.containers[item].max_stock = max_stock

    @mode("maintenance")
    def reset(self):
        """Remet la machine dans son etat sortie d'usine
       (ne reinitialise pas l'historique)"""

        hitorique = self.__historique
        self.__init__()
        self.__historique = hitorique

    @mode("maintenance")
    def vider_caisse(self):
        """Vide la caisse : Met a zero le nombre de chaque piece"""

        self.__caisse.vider()

    @mode("maintenance")
    def get_stock(self, item):
        """Retourne le stock d'un boite"""

        return self.containers[item]

    @mode("maintenance")
    def get_stock_size(self, item):
        """Retourne la taille du stock restant d'une boite"""

        return self.containers[item].taille

    @mode("maintenance")
    def get_stock_max(self, item):
        """Retourne la taille maximum d'une boite"""

        return self.containers[item].taille_max

    @mode("maintenance")
    def get_all_stock(self):
        """Retourne le stock de tout les boites"""

        return {key: boite for key, boite in self.containers.items()}

    @mode("maintenance")
    def remplir_stock(self, item):
        """Remplit au maximum le stock d'un boite"""
        assert item in self.containers, "Container inexistant : {}".format(item)
        self.containers[item].recharger(self.containers[item].taille_max)

    @mode("maintenance")
    def remplir_tout_stock(self):
        """Remplit au maximum le stock de tout les boites"""

        for boite in self.containers.values():
            boite.recharger(boite.taille_max)

    @mode("maintenance")
    def ajouter_stock(self, quantite):
        """Remplit le stock d'un boite jusqu'a un certain niveau"""

        if quantite in range(self.containers[item].taille,
                             self.containers[item].taille_max + 1):
            self.containers[item].recharger(quantite)

    @mode("maintenance")
    def hitorique(self):
        """Affiche l'historique du distributeur"""

        return self.historique

    @mode("maintenance")
    def statistiques(self):
        return self.stats.display_all()

    # Methodes du mode fonctionnement
    def __verifier_commande(self, cmd):
        """Verifie puis formate le tuple binaire pour l'adapter a la machine"""

        assert isinstance(cmd, tuple), Distributeur.erreur[3]
        assert len(cmd) == len(self.product_containers) + \
            1, Distributeur.erreur[4]
        assert not False in (isinstance(i, int) and i in range(0, 2)
                             for i in cmd), Distributeur.erreur[5]
        return True

    def __formater_commande(self, cmd):
        """Verifie puis formate le tuple binaire pour l'adapter a la machine"""

        sucre = int('{}{}'.format(cmd[0], cmd[1]), 2)
        is_the = cmd[3] == 1
        return {
            self.ingredients[Sucre.nom]: sucre,
            self.ingredients[Lait.nom]: cmd[2],
            self.ingredients[The.nom]: cmd[3],
            self.ingredients[Cafe.nom]: (cmd[4] if not is_the else 0),
            self.ingredients[Chocolat.nom]: (cmd[5] if not is_the else 0),
        }

    def __get_boites(self, cmd):
        """Retourne les boites d'ingredients commandés"""
        return {
            nom: boite for nom,
            boite in self.product_containers.items() if cmd[
                self.ingredients[nom]] > 0}

    def __verifier_monnaie(self, monnaie):
        """Verifie que la machine peut bien encaisser le paiement"""

        assert isinstance(monnaie, tuple), Distributeur.erreur[1]
        assert len(monnaie) == len(Distributeur.monnaie_acceptee), \
            Distributeur.erreur[2]
        code = Distributeur.monnaie_acceptee.code
        maxi = Distributeur.somme_maximum
        if get_change.trad(monnaie, code) > maxi:
            _, sol = get_change.getSol(maxi, monnaie, code, len(monnaie))
            if get_change.trad(sol, code) <= maxi:
                return _, sol
            else:
                return monnaie, None
        return None, monnaie

    def montant_change_container(self):
        return tuple(val for val, boite in self.change_containers.items())

    def __verifier_rendu_monnaie_possible(self, prix):
        somme = self.change_containers.somme
        if somme >= prix:
            code = self.change_containers.code
            montant = self.change_containers.montant
            _, sol = get_change.getSol(prix, montant, code, len(montant))
            if get_change.trad(sol, code) == prix:
                print(_, sol)
                return _, sol
        print("Pas assez de pièce dans les containers")
        return None, None

    def __correspondance_boisson(self, order):
        """Recherche une correspondance entre la commande
        et une boisson, renvoi la boisson si trouve"""

        # Pour chaque boisson, si une boisson correspond aux
        # boites que je veux utiliser, alors je la retourne
        order = [ing for ing, quantity in order.items() if quantity > 0]
        for boisson in self.boissons.values():
            if boisson.is_ingredients(order):
                return boisson

    def __get_prix_boisson(self, order):
        return sum(
            self.containers[
                ing.nom].get_prix_unitaire(value) for ing,
            value in order.items())

    def __verifier_stock_suffisant(self):
        """Verifie que les stocks sont sufisamment remplit
        pour satisfaire la commande"""

        # Pour chaque boite si le stock est inferieur a la
        # demande je retourne faux

        for (key, boite) in self.containers.items():
            if boite.taille <= self.consommation[key]:
                return False
        return True

    def __encaisser(self, mtoContainer):
        pass

    def __preparer_commande(
        self,
        order,
        boisson_type,
    ):
        """Utilise les boites necessaires et demandes pour
        concevoir la boisson desiree"""

        # Utilise chaque boite demande pour concocter ma boisson

        if self.debug:
            print('\nPreparation de la commande')
        self.stats.nb_vendu[boisson_type] += 1
        boisson = boisson_type()
        for ingredient_type, quantity in order.items():
            if ingredient_type == Sucre:
                self.stats.dose_sucre[boisson_type].append(quantity)
            if ingredient_type == Lait and not Lait in boisson.ingredients_de_base:
                self.stats.with_lait[boisson_type] += quantity
            self.stats.conso_ingredient[ingredient_type] += quantity
            ingredients = self.containers[ingredient_type.nom].tirer(quantity)
            boisson.ajouter(ingredients)
        if self.debug:
            print('Preparation terminee')
            print("{}{}{}".format('=' * 5, boisson, '=' * 5, '\n'))
        return boisson

    def __retourner_monnaie(self, *args):
        args = [arg for arg in args if arg]
        return [sum(p) for p in zip(*args)]

    @mode("fonctionnement")
    def commander(self, monnaie, commande):
        """Recoit, verifie et lance la commande"""
        _mtoReturn1 = (0 for p in monnaie)
        _mtoReturn2 = (0 for p in monnaie)
        _mtoUse = (0 for p in monnaie)
        # Je verifie d'abord si la monnaie respecte les contraintes
        # du distributeur, si oui alors monnaie_accepte sera Vrai
        # sinon il sera Faux
        self.commande_en_cours = True
        _commande_acceptee = self.__verifier_commande(commande)
        if _commande_acceptee:
            _mtoReturn1, _mtoUse = self.__verifier_monnaie(monnaie)
            if _mtoUse:

                # Si la monnaie est bonne, alors je regarde si je peux
                # trouver une boisson qui correspond a la commande
                # si oui, alors je recupere cette boisson

                order = self.__formater_commande(commande)
                boites_a_utiliser = self.__get_boites(order)
                boisson_type = self.__correspondance_boisson(order)
                if boisson_type:

                        # Si j'ai recupere une boisson, alors je calcul
                        # le prix de ma commande

                    prix = self.__get_prix_boisson(order)
                    if self.debug:
                        print(
                            'Prix({})={}C'.format(
                                '+'.join(boites_a_utiliser.keys()),
                                prix))

                    # et je regarde si le distributeur peut me rendre
                    # la monnaie (si besoin est)
                    if get_change.trad(_mtoUse, Distributeur.monnaie_acceptee.code) >= prix:
                        if self.debug: print("Vous n'avez pas assez.")
                        _mtoReturn2, _mtoContainer = \
                            self.__verifier_rendu_monnaie_possible(prix)
                        if _mtoContainer:

                                # si je peux rendre la monnaie (si besoin)
                                # alors je prepare la commande et je la propose
                                # au client
                            self.commande_en_cours = False
                            self.__encaisser(_mtoContainer)
                            return self.__preparer_commande(
                                order, boisson_type), self.__retourner_monnaie(_mtoReturn1, _mtoReturn2)

            # Si une de toutes ces verifications n'est pas valide
            # alors je rend la monnaie

        self.commande_en_cours = False
        if self.debug:
            print('Impossible. Rend la monnaie.')
        return None, self.__retourner_monnaie(monnaie)
