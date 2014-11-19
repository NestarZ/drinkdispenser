#!/bin/python3
try:
    #permet de lancer le fichier mère (distributeur.py)
    from data import ingredient
except ImportError:
    #permet de lancer ce fichier en stand-alone
    import ingredient
    
class MetaBoisson(type):
    def __str__(cls):
        return cls.__name__
    
# BOISSONS 
class Boisson(metaclass=MetaBoisson):
    """Classe mère de toutes les boissons"""
    #Je met les ingredients nécessaires et optionnels
    #de la boisson dans deux tuples (ps:voir les enfants)
    ingredients_de_base = tuple()
    ingredients_optionnels = tuple()
    
    def __str__(self):
        """Permet d'afficher le type de la boisson"""
        #Lorsque j'affiche ou je demande de convertir
        #ma boisson en chaine de caractère, l'element
        #affiché sera le nom de la boisson (le nom de la classe).
        #print(Boisson) => Boisson
        #print(Cafe) => Cafe
        #a = The; print(a) => The
        with_lait = ingredient.Lait in self.goblet and not ingredient.Lait in type(self).ingredients_de_base
        with_sucre = ingredient.Sucre in self.goblet and not ingredient.Sucre in type(self).ingredients_de_base
        dose_sucre = self.goblet.count(ingredient.Sucre)
        return "Et voici un {}{}{}{}!!".format(
            type(self).__name__,
            " avec du lait" if with_lait else '',
            " et" if with_lait and with_sucre else '',
            " avec {} morceaux de sucre".format(
                dose_sucre) if with_sucre else '')
    
    def __init__(self):
        self.goblet = list()
        
    def ajouter_ingredient(self, ingredient, quantite):
        for q in range(quantite):
            self.goblet.append(type(ingredient))
    
    @classmethod
    def is_ingredients(cls, ingredients):
        """Vérifie si les ingrédients correspond à la boisson"""
        #Est-ce que les ingrédients en parametre sont dans les
        #ingredients de base ou optionnels de la boisson ?
        _ingredients = [type(i) for i in ingredients]
        for ingredient in _ingredients:
            if not (ingredient in cls.ingredients_de_base or
            ingredient in cls.ingredients_optionnels):
                return False
        #Est-ce que les ingredients de base de la boisson
        #sont dans les ingredients en parametre ?
        for ingredient in cls.ingredients_de_base:
            if not ingredient in _ingredients:
                return False
        #Si oui je retourne la boisson
        return cls
    
class The(Boisson):
    """Boisson Thé définie par ses ingrédients"""
    #Un Thé nécessite du thé comme ingrédient obligatoire (de base)
    #on peut aussi y rajouter du lait ou du sucre.
    #Tout les thés partageront ainsi les même ingrédients nécessaires
    #ou optionnels à sa réalisation
    ingredients_de_base = (ingredient.The,)
    ingredients_optionnels = (ingredient.Lait,
                              ingredient.Sucre)

class Cafe(Boisson):
    """Boisson Café définie par ses ingrédients"""
    #Un Café nécessite du Café comme ingrédient obligatoire (de base)
    #on peut aussi y rajouter du lait ou du sucre.
    #Tout les cafés partageront ainsi les même ingrédients nécessaires
    #ou optionnels à sa réalisation
    ingredients_de_base = (ingredient.Cafe,)
    ingredients_optionnels = (ingredient.Lait,
                              ingredient.Sucre)

class Chocolat(Boisson):
    """Boisson Chocolat définie par ses ingrédients"""
    #Un Café nécessite du Chocolat comme ingrédient obligatoire
    #(de base) on peut aussi y rajouter du lait ou du sucre.
    #Tout les chocolats partageront ainsi les même ingrédients nécessaires
    #ou optionnels à sa réalisation
    ingredients_de_base = (ingredient.Chocolat,)
    ingredients_optionnels = (ingredient.Lait,
                              ingredient.Sucre)

class Capuccino(Boisson):
    """Boisson Capuccino définie par ses ingrédients"""
    #Un Capuccino nécessite du Chocolat et du Café comme ingrédient
    #obligatoire (de base) on peut aussi y rajouter du sucre MAIS PAS de lait
    #Tout les capuccino partageront ainsi les même ingrédients nécessaires
    #ou optionnels à sa réalisation
    ingredients_de_base = (ingredient.Chocolat,
                           ingredient.Cafe)
    ingredients_optionnels = (ingredient.Sucre,)

class Macciato(Boisson):
    """Boisson Macciato définie par ses ingrédients"""
    #Un Macciato nécessite du Chocolat, du Café et du Lait comme
    #ingrédient obligatoire (de base) on peut aussi y rajouter du sucre.
    #Tout les macciato partageront ainsi les même ingrédients nécessaires
    #ou optionnels à sa réalisation
    ingredients_de_base = (ingredient.Chocolat,
                           ingredient.Cafe,
                           ingredient.Lait)
    ingredients_optionnels = (ingredient.Sucre,)
