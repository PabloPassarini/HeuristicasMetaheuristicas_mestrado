from descida import descida_best_improvement
from random import randint, random

def ILS(n, s, d, n_nivel, ILSmax):

    s, fo = descida_best_improvement(n, s, d)
    iter = 0
    MelhorIter = 0
    nivel = 1

    while iter - MelhorIter < ILSmax:
        
        cont = 0
        while cont < n_nivel:
            maxTrocas = nivel + 1
            nTrocas = 0
            
            s_ll = s.copy()
            fo_ll = fo
            while nTrocas < maxTrocas:
                i = randint(0, n-1)
                j = randint(0, n-1)
                while i == j: 
                    j = randint(0, n-1)
                nTrocas += 1
                s_ll[i], s_ll[j] = s_ll[j], s_ll[i]
            s_ll, fo_ll = descida_best_improvement(n, s_ll, d)
            if fo_ll < fo:
                s = s_ll
                fo = fo_ll
                cont = 0
                MelhorIter = iter
                print("Novo melhor: ", fo)
            else:
                cont += 1
        nivel += 1
        iter += 1
        print("Nível subiu para: ", nivel)
    return fo, s

