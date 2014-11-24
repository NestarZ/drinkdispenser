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

    erreur = {
        1: 'La monnaie doit etre un tuple',
        2: 'Vous devez entrer une valeur pour chaque piece.',
        3: 'La consommation doit etre un tuple',
        4: 'La commande doit etre un tuple a valeur pour chaque boite.',
        5: 'La commande doit etre un tuple binaire.',
    }

    monnaie_acceptee = Coins(Coin200, Coin100, Coin50, Coin20, Coin10, Coin5)
    monnaie_container = Coins(Coin50, Coin20, Coin10, Coin5)
    somme_max = Coin200.value

    def __str__(self):
        return 'Distributeur en mode usine'

    def __init__(self, debug=False):
        """Construit le distributeur et integre ses composantes
        (boites, stock, tarifs, caisse)"""

        self.__ingredients = {
            Cafe.nom: Cafe,
            Sucre.nom: Sucre,
            Lait.nom: Lait,
            Chocolat.nom: Chocolat,
            The.nom: The,
        }
        self.__product_containers = {
            ingredient.nom: BoiteProduit(ingredient)
            for ingredient in self.ingredients.values()}
        self.__change_containers = Coins(Coin50, Coin20, Coin10, Coin5)
        self.__containers = self.__change_containers.get_dict()
        self.__containers.update(self.__product_containers)
        self.__boissons = {
            boisson.Cafe.nom: boisson.Cafe,
            boisson.Capuccino.nom: boisson.Capuccino,
            boisson.Macciato.nom: boisson.Macciato,
            boisson.Chocolat.nom: boisson.Chocolat,
            boisson.The.nom: boisson.The
        }
        self.__caisse = Coins(Coin200, Coin100, Coin50, Coin20, Coin10, Coin5)
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
        assert item in self.containers, "Container inexistant : {}".format(
            item)
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

    def __verifier_commande(self, cmd):
        """Verifie puis formate le tuple binaire pour l'adapter a la machine"""

        assert isinstance(cmd, tuple), Distributeur.erreur[3]
        assert len(cmd) == len(self.product_containers) + \
            1, Distributeur.erreur[4]
        assert not False in (isinstance(i, int) and i in range(0, 2)
                             for i in cmd), Distributeur.erreur[5]
        return True

    def trad(self, cmd):
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
        return self.caisse.calcul_change(monnaie, Distributeur.somme_max)

    def __verifier_rendu_monnaie_possible(self, mtoUse, prix):
        total = mtoUse.somme - prix
        return self.change_containers.do_change(total)

    def match(self, order):
        """Recherche une correspondance entre la commande
        et une boisson, renvoi la boisson si trouve"""

        # Pour chaque boisson, si une boisson correspond aux
        # boites que je veux utiliser, alors je la retourne
        order = [ing for ing, quantity in order.items() if quantity > 0]
        for boisson in self.boissons.values():
            if boisson.is_ingredients(order):
                return boisson, boisson.supplements(order)
        return None, None

    def __get_prix_boisson(self, order):
        return sum(
            self.containers[
                ing.nom].get_prix_unitaire(value) for ing,
            value in order.items())

    def __verifier_stock_suffisant(self, boites_a_utiliser, order):
        """Verifie que les stocks sont sufisamment remplit
        pour satisfaire la commande"""

        for (key, boite) in boites_a_utiliser.items():
            if boite.taille <= order[boite.type_ditem]:
                return False
        return True

    def __preparer_commande(self, order, boisson_type, supplements):
        """Utilise les boites necessaires et demandes pour
        concevoir la boisson desiree"""

        # ========== MAJ des Statistiques ==========
        self.stats.nb_vendu[boisson_type] += 1
        if Sucre in supplements:
            quantity = order[Sucre]
            self.stats.dose_sucre[boisson_type].append(quantity)
        if Lait in supplements:
            self.stats.with_lait[boisson_type] += 1
        # ========== Preparation de la boisson ========== #
        boisson = boisson_type()
        for ingredient_type, quantity in order.items():
            self.stats.conso_ingredient[ingredient_type] += quantity
            ingredients = self.containers[ingredient_type.nom].tirer(quantity)
            boisson.ajouter(ingredients)
        return boisson

    @mode("fonctionnement")
    def commander(self, monnaie=None, commande=None):
        """Recoit, verifie et lance la commande"""
        assert monnaie and commande, "Must enter two 6-uplet, (2nd must be binary)"
        print("\nenvoyé>", monnaie)
        _commande_acceptee = self.__verifier_commande(commande)
        if _commande_acceptee:
            _mtoReturn1, _mtoUse = self.__verifier_monnaie(monnaie)
            if _mtoUse:
                print("rendu1>", _mtoReturn1)
                order = self.trad(commande)
                boites_a_utiliser = self.__get_boites(order)
                if self.__verifier_stock_suffisant(boites_a_utiliser, order):
                    boisson_type, supplements = self.match(order)
                    if boisson_type:
                        prix = self.__get_prix_boisson(order)
                        if _mtoUse.somme >= prix:
                            _mtoReturn2 = \
                                self.__verifier_rendu_monnaie_possible(
                                    _mtoUse, prix)
                            code = Distributeur.monnaie_acceptee.code
                            if _mtoReturn2:
                                print("rendu2>",_mtoReturn2, "Préparation de la boisson")
                                self.caisse.mix(_mtoUse)
                                return self.__preparer_commande(
                                    order, boisson_type, supplements)
                            print("rendu2>",_mtoUse,"Stock de pièces non suffisant")
                            return None
                        print("rendu2>",_mtoUse,"Prix > à la somme des pièces entrées")
                        return None
                    print("rendu2>",_mtoUse,"Aucune boisson de ce type")
                    return None
                print("rendu2>",_mtoUse,"Stock d'ingrédient non suffisant")
                return None
        self.commande_en_cours = False
        print("rendu2>",monnaie, "Commande erronée")
        return None
