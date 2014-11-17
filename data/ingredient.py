#!/bin/python3
# INGREDIENTS
class Ingredient():
    """Classe mère de tout les ingrédients"""
    #Un ingrédient a un stock maximum fixé par
    #défaut à 100, un stock et un prix courant
    #communs à tout les ingrédients du même type
    def __init__(self):
        self.__max_stock = 100
        self.__stock = 0
        self.__prix = 0
        
    def __str__(self):
        return type(self).__name__
    
    def get_prix(self, value):
        return self.prix[value] if isinstance(self.prix, dict) else self.prix

    @property
    #Toutes les fonctions/méthodes qui suivent agissent sur la classe
    #elle même et donc sur toutes les instances de cette classe
    #Par exemple ici, Ingredient.get_prix() me retournera
    #la variable définit un peu plus haut (__prix) soit 0.
    #Et la variable __prix ne peut être accédé en dehors
    #de la classe. Si je fait Ingredient.__prix ça ne marchera
    #pas. C'est une variable privé (accessible que dans la classe).
    def prix(self):
        """Retourne le prix de l'ingredient"""
        return self.__prix

    @property
    def stock(self):
        """Retourne le stock de l'ingredient"""
        return self.__stock

    @property
    def max_stock(self):
        """Retourne le stock max de l'ingredient"""
        return self.__max_stock

    @prix.setter
    def prix(self, value):
        """Fixe le prix de l'ingredient sous condition d'être un prix valide"""
        if isinstance(self, Sucre):
            assert isinstance(value, dict), "Le sucre a différents tarifs selon la dose. \
            Veuillez les renseigner dans un dictionnaire. exemple : {0:0,1:5,2:15,3:15}"
            assert not False in ((isinstance(v, int)
            and int(abs(v)) == v and dose in range(Sucre.doses_possibles+1)) for dose,v in value.items()), \
        "Les doses doivent être des entiers naturels."
        else:
            assert isinstance(value, int) and int(abs(value)) == value, \
            "Le prix (en centimes) doit être un entier naturel."
        #Ici je m'assure que le nouveau prix est bien positif et naturel.
        #Si ce n'est pas le cas, je lève une erreur avec le texte adéquat.
        self.__prix = value

    @stock.setter
    def stock(self, value):
        """Fixe le stock de l'ingredient sous condition d'être un stock valide"""
        assert ((isinstance(value, int) or isinstance(value, float))
                and int(abs(value)) == value
                and value <= self.max_stock), \
            "Le stock doit être un entier naturel inférieur aux stock max et supérieur à 0 (max_stock={}).".format(
                self.max_stock)
        #Même chose ici, le nouveau stock doit être inférieur
        #au stock maximum mais doit être positif et naturel.
        #Encore uen fois, si ce n'est pas le cas,
        #je lève une erreur avec le texte adéquat.
        print("Fixe le stock de {} à {}".format(self, value))
        self.__stock = value

    @max_stock.setter
    def max_stock(self, value):
        """Fixe le stock max de l'ingredient sous condition d'être un stock max valide"""
        assert isinstance(value, int) and int(abs(value)) == value, "Le stock max doit être un entier naturel."
        #Idem que set_stock mais pour le stock maximum avec d'autres
        #contraintes.
        self.__max_stock = value

    def utiliser(self, nombre):
        """Utilise l'ingrédient un nombre de fois détérminé (affecte les stock)"""
        #Cette méthode (fonction) permet de simuler l'utilisation
        #de l'ingrédient dans le processus de conception d'une boisson
        #Le paramètre nombre correspond au nombre d'utilisation
        #de l'ingrédient dans le processus. Par exemple, si je veux 3
        #Sucres, je vais réduire le stock de 3 sucres. Seulement si
        #le stock est suffisant. La verif (si le stock est suffisant
        #ne se fait toutefois pas ici, c'est la machine qui le vérifie).
        self.stock -= nombre
        
class Cafe(Ingredient):
    """Ingrédient de type café, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de café est fixé par défaut à 20Centimes
    #Toutes les doses de café (instances) issues de cette classe (Cafe)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    def __init__(self):
        super().__init__()
        self.prix = 20

class The(Ingredient):
    """Ingrédient de type thé, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de thé est fixé par défaut à 10Centimes
    #Toutes les doses de thé (instances) issues de cette classe (The)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    def __init__(self):
        super().__init__()
        self.prix = 10

class Chocolat(Ingredient):
    """Ingrédient de type chocolat, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de chocolat est fixé par défaut à 30Centimes
    #Toutes les doses de chocolat (instances) issues de cette classe (Chocolat)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    def __init__(self):
        super().__init__()
        self.prix = 30

class Lait(Ingredient):
    """Ingrédient de type lait, il a un prix, un stock et un stock maximum fixé"""
    #Le prix unitaire d'une dose de lait est fixé par défaut à 5Centimes
    #Toutes les doses de lait (instances) issues de cette classe (Lait)
    #partageront ainsi le même prix (resp. stock, stock maximum)
    def __init__(self):
        super().__init__()
        self.prix = 5

class Sucre(Ingredient):
    """Ingrédient de type sucre, il a un prix, un stock et un stock maximum fixé"""
    #Ici, le sucre peut avoir plusieurs prix, selon sa quantité
    #on a donc plusieurs possibilités (4) qui correspondent au
    #nombre de dose. Toutes les doses de sucres partageront ainsi
    #le même prix (resp. stock, stock maximum)
    doses_possibles = 3

    def __init__(self):
        super().__init__()
        self.prix = {0: 0, 1: 5, 2: 15, 3: 15}
