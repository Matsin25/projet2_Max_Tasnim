from functools import reduce


def addition(x, y):
    return x + y

def somme(n):
    r = range(n + 1)
    resultat = reduce(addition, r)
    return resultat


print(somme(9))