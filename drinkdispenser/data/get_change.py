
class stack(object):

    """ gestion de pile par liste python """

    def __init__(self):
        self.__s = list()
        self.__sz = 0

    def __str__(self):
        _str = "\n___ Stack __ \n"
        i = 0
        for x in self.__s:
            _str += "%02d: %s\n" % (i, str(x))
            i += 1
        _str += '=' * 19 + '\n'
        return _str

    def push(self, val):
        self.__s.insert(0, val)
        self.__sz += 1

    def pop(self):
        if self.__sz > 0:
            x = self.__s.pop(0)
            self.__sz -= 1
            return x

    @property
    def size(self):
        return self.__sz

    def __len__(self):
        return self.__sz

    def consult(self):
        return self.__sz[0]


def find(montant, debug=False):
    """
    cree uune pile vide et lance l'appel récursif
    """
    return getSol(200, montant, (200, 100, 50, 20, 10), len(montant), debug)


def getSol(toReach, entree, code, sz, debug=False):
    """ recherche d'une solution par gestion de pile """
    if trad(entree, code) <= toReach:
        return [0] * sz, entree
    _st = stack()
    _st.push((toReach, [], 0))
    _done = False
    while(_st.size > 0 and not _done):
        if debug:
            print(_st)
        left, pSol, idx = _st.pop()
        if left == 0:
            if debug:
                print('1', end='')
            _done = True
        if idx < sz:
            i = 0
            while i <= entree[idx]:
                if debug:
                    print('.', end='')
                nTarget = left - i * code[idx]
                if nTarget >= 0:
                    _st.push((nTarget, pSol + [i], idx + 1))
                    i += 1
                else:
                    break
    _used = pSol + [0 for _ in range(idx, sz)]
    _change = [entree[_] - _used[_] for _ in range(sz)]
    return _change, _used


def trad(m, v=(200, 100, 50, 20, 10)):
    _v = v
    _sz = len(_v)
    return sum([m[_] * _v[_] for _ in range(_sz)])

if __name__ == "__main__":
    verbose = True
    for m in(
            (1, 1, 2, 1, 1),
            (0, 1, 2, 1, 1),
            (0, 1, 1, 6, 1),
            (0, 1, 0, 6, 7),
            (0, 1, 1, 5, 0),
            (0, 0, 1, 6, 7),
            (0, 1, 1, 0, 1),
            (0, 0, 1, 8, 0),
            (0, 0, 1, 8, 1),
            (0, 1, 2, 3, 0)):
        print(m, ' ', trad(m), end=' ')
        _, _sol = find(m, verbose)
        print("rendu %03d sol> %s, val=%03d" % (trad(_), _sol, trad(_sol)))
