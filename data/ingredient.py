#!/bin/python3
# INGREDIENTS
class MetaIngredient(type):
    def __str__(cls):
        """Permet d'afficher le type de l'ingredient"""
        #Lorsque j'affiche ou je demande de convertir
        #mon ingredient en chaine de caractère, l'element
        #affiché sera le nom de l'ingredient (le nom de la classe).
        #print(Ingredient) => Ingredient
        #print(Sucre) => Sucre
        #a = Lait; print(a) => Lait
        return cls.__name__

class Ingredient(metaclass=MetaIngredient):
    """Classe mère de tout les ingrédients"""
    #Un ingrédient a un stock maximum fixé par
    #défaut à 100, un stock et un prix courant
    #communs à tout les ingrédients du même type
    __max_stock = 100
    __stock = 0
    __prix = 0
    
    @classmethod
    #Toutes les fonctions/méthodes qui suivent agissent sur la classe
    #elle même et donc sur toutes les instances de cette classe
    #Par exemple ici, Ingredient.get_prix() me retournera
    #la variable définit un peu plus haut (__prix) soit 0.
    #Et la variable __prix ne peut être accédé en dehors
    #de la classe. Si je fait Ingredient.__prix ça ne marchera
    #pas. C'est une variable privé (accessible que dans la classe).
    def get_prix(cls):
        """Retourne le prix de l'ingredient"""
        return cls.__prix

    @classmethod
    def get_stock(cls):
        """Retourne le stock de l'ingredient"""
        return cls.__stock

    @classmethod
    def get_max_stock(cls):
        """Retourne le stock max de l'ingredient"""
        return cls.__max_stock

    @classmethod
    def set_prix(cls, value):
        """Fixe le prix de l'ingredient sous condition d'être un prix valide"""
        assert isinstance(value, int) and int(abs(value)) == value, \
        "Le prix (en centimes) doit être un entier naturel."
        #Ici je m'assure que le nouveau prix est bien positif et naturel.
        #Si ce n'est pas le cas, je lève une erreur avec le texte adéquat.
        cls.__prix = value

    @classmethod
    def set_stock(cls, value):
        """Fixe le stock de l'ingredient sous condition d'être un stock valide"""
        assert ((isinstance(value, int) or isinstance(value, float))
                and int(abs(value)) == value
                and value <= Ingredient.get_max_stock()), \
            "Le stock doit être un entier naturel inférieur aux stock max et supérieur à 0 (max_stock={}).".format(
                Ingredient.__max_stock)
        #Même chose ici, le nouveau stock doit être inférieur
        #au stock maximum mais doit être positif et naturel.
        #Encore uen fois, si ce n'est pas le cas,
        #je lève une erreur avec le texte adéquat.
        print("Fixe le stock de {} à {}".format(cls, value))
        cls.__stock = value

    @classmethod
    def set_max_stock(cls):
        """Fixe le stock max de l'ingredient sous condition d'être un stock max valide"""
        assert isinstance(value, int) and int(abs(value)) == value, "Le stock max doit être un entier naturel."
        #Idem que set_stock mais pour le stock maximum avec d'autres
        #contraintes.
        cls.__max_stock = value

    @classmethod
    def utiliser(cls, nombre):
        """Utilise l'ingrédient un nombre de fois détérminé (affecte les stock)"""
        #Cette méthode (fonction) permet de simuler l'utilisation
        #de l'ingrédient dans le processus de conception d'une boisson
        #Le paramètre nombre correspond au nombre d'utilisation
        #de l'ingrédient dans le processus. Par exemple, si je veux 3
        #Sucres, je vais réduire le stock de 3 sucres. Seulement si
        #le stock est suffisant. La verif (si le stock est suffisant
        #ne se fait toutefois pas ici, c'est la machine qui le vérifie).
        cls.set_stock(cls.get_stock() - nombre)
        
class Cafe(Ingredient):
    """Ingrédient de type café, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de café est fixé par défaut à 20Centimes
    #Toutes les doses de café (instances) issues de cette classe (Cafe)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    __prix = 20

class The(Ingredient):
    """Ingrédient de type thé, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de thé est fixé par défaut à 20Centimes
    #Toutes les doses de thé (instances) issues de cette classe (The)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    __prix = 10

class Chocolat(Ingredient):
    """Ingrédient de type chocolat, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de chocolat est fixé par défaut à 20Centimes
    #Toutes les doses de chocolat (instances) issues de cette classe (Chocolat)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    __prix = 30

class Lait(Ingredient):
    """Ingrédient de type lait, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de lait est fixé par défaut à 20Centimes
    #Toutes les doses de lait (instances) issues de cette classe (Lait)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    __prix = 5

class Sucre(Ingredient):
    """Ingrédient de type sucre, il a un prix, un stock et un stock maximum fixé"""
    #Ici, le sucre peut avoir plusieurs prix, selon sa quantité
    #on a donc plusieurs possibilités (4) qui correspondent au
    #nombre de dose. Toutes les doses de sucres partageront ainsi
    #le même prix (resp. stock, stock maximum)
    __prix = {0: 0, 1: 5, 2: 15, 3: 15}
