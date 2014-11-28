try:
    from .boite import BoitePiece, BoiteProduit
    from .get_change import *
except (ImportError, SystemError) as e:
    from boite import BoitePiece, BoiteProduit
    from get_change import *


class MetaCoin(type):

    def __init__(cls, *args):
        super().__init__(*args)
        cls.nom = "{} {}".format(
            cls.value if cls.value < 100 else cls.value / 100,
            "centimes" if cls.value < 100 else "euros")

    def __str__(cls):
        return cls.nom


class Coin(metaclass=MetaCoin):
    value = 0


class Coin200(Coin):
    value = 200


class Coin100(Coin):
    value = 100


class Coin50(Coin):
    value = 50


class Coin20(Coin):
    value = 20


class Coin10(Coin):
    value = 10


class Coin5(Coin):
    value = 5

class CoinsManager(object):

    types = (Coin200, Coin100, Coin50, Coin20, Coin10, Coin5)

    def __str__(self):
        return str(
            tuple(
                (self[m.value].taille if m.value in self.code else 0)
                for m in Coins.types))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self.__boites.__iter__()

    def __len__(self):
        return self.__boites.__len__()

    def __getitem__(self, i):
        assert i in self.code, "Aucune pièce de cette valeur"
        return self.__boites[self.code.index(i)]

    def get_dict(self):
        return {n.value: b for n, b in zip(self.__tuple, self.__boites)}

    def insert_cointype(self, i, v):
        self.check(v)
        self.__tuple.insert(i, v)
        self.__boites.isert(i, BoitePiece(v))

    def check(self, v):
        assert isinstance(v, MetaCoin)

    def vider(self):
        for boite in self.__boites:
            boite.vider()

    def add(self, t):
        assert len(t) == len(self)
        for i, boite in enumerate(self.__boites):
            boite.recharger(boite.taille + t[i])

    def mix(self, coins):
        assert len(coins) == len(self)
        for boite in self.__boites:
            boite.recharger(
                boite.taille + coins[boite.type_ditem.value].taille)

    def change(self, t):
        assert len(t) == len(self)
        return tuple(
            boite.tirer(t[i]) for i,
            boite in enumerate(self.__boites))

    def calcul_change(self, monnaie, smax):
        _change, _used = getSol(smax, monnaie, self.code, len(self))
        # self.add(_used)
        return Coins.new(_change, self.code), Coins.new(_used, self.code)

    def do_change(self, val):
        if val <= self.somme:
            _change, _used = getSol(val, self.montant, self.code, len(self))
            self.change(_used)
            return Coins.new(_used, self.code)

    @property
    def code(self):
        return tuple(coin.value for coin in self.__tuple)

    @property
    def montant(self):
        return tuple(v.taille for v in self.__boites)

    @property
    def somme(self):
        return sum(
            n * coin.value for n,
            coin in zip(
                self.montant,
                self.__tuple))

class CoinsStocker(CoinsManager):
    """ Gere de la monnaie avec des boites à taille maximum """
    def __init__(self, *_tuple):
        assert not False in (isinstance(_, MetaCoin) for _ in _tuple)
        self.__tuple = _tuple
        self.__boites = tuple(BoitePiece(_) for _ in _tuple)


class CoinsHandler(CoinsManager):
    """ Gere de la monnaie avec des boites à taille infinie """
    def __init__(self, montant, code):
        c = cls(*(c for c in Coins.types if c.value in code))
        c.add(montant)
        return c
