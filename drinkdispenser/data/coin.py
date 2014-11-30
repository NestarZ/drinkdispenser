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
    values = (200, 100, 50, 10, 5)
    
    def __str__(self):
        return str(
            tuple(
                (self[m.value].taille if m.value in self.code else 0)
                for m in CoinsManager.types))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return self._boites.__iter__()

    def __len__(self):
        return self._boites.__len__()

    def __getitem__(self, i):
        assert i in self.code, "Aucune pièce de cette valeur"
        return self._boites[self.code.index(i)]

    def get_dict(self):
        return {n.value: b for n, b in zip(self._tuple, self._boites)}

    def insert_cointype(self, i, v):
        self.check(v)
        self._tuple.insert(i, v)
        self._boites.isert(i, BoitePiece(v))

    def check(self, v):
        assert isinstance(v, MetaCoin)

    def vider(self):
        for boite in self._boites:
            boite.vider()

    def add(self, t):
        assert len(t) == len(self)
        for i, boite in enumerate(self._boites):
            boite.recharger(boite.taille + t[i])

    def mix(self, coins):
        assert len(coins) == len(self)
        for boite in self._boites:
            boite.recharger(
                boite.taille + coins[boite.type_ditem.value].taille)

    def change(self, t):
        assert len(t) == len(self)
        return tuple(
            boite.tirer(t[i]) for i,
            boite in enumerate(self._boites))

    def calcul_change(self, monnaie, smax):
        _change, _used = getSol(smax, monnaie, self.code, len(self))
        return CoinsStocker.new(_change, self.code), CoinsStocker.new(_used, self.code)

    def do_change(self, val):
        if val <= self.somme:
            _change, _used = getSol(val, self.montant, self.code, len(self))
            self.change(_used)
            return CoinsStocker.new(_used, self.code)

    @property
    def code(self):
        return tuple(coin.value for coin in self._tuple)

    @property
    def montant(self):
        return tuple(v.taille for v in self._boites)

    @property
    def somme(self):
        return sum(
            n * coin.value for n,
            coin in zip(
                self.montant,
                self._tuple))

class CoinsStocker(CoinsManager):
    """ Gere de la monnaie avec des boites à taille maximum """
    
    def __init__(self, _tuple):
        for elt in _tuple:
            assert elt in [c.value for c in CoinsManager.types], "Cette valeur ne correspond à aucune pièce"
        self._tuple = [coin for coin in CoinsManager.types if coin.value in _tuple]
        self._boites = tuple(BoitePiece(coin, _tuple[coin.value]) for coin in CoinsManager.types if coin.value in _tuple)
    @classmethod
    def new(cls, montant, code):
        """ Permet de créer une boite sans souis de la taille """
        c = cls({value: 100000 for value in code})
        c.add(montant)
        return c
