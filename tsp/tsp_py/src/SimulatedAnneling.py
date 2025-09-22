from util import calcula_fo
from random import randint, random
from descida import calcula_delta
from math import exp


def temperaturaInicial(n, s, d, beta, gama, SAmax, temp_incial):
    continua = True

    fo = fo_star = fo_viz = calcula_fo(n, s, d)
    while continua:
        aceitos = 0
        for iterT in range(1, SAmax+1):
            i = randint(0, n-1)
            j = randint(0, n-1)
            while i == j: 
                j = randint(0, n-1)

            delta1 = calcula_delta(n,s,d,i, j)
            s[i], s[j] = s[j], s[i]
            delta2 = calcula_delta(n, s, d, i, j)
            delta = -delta1 + delta2
            
            if delta < 0:
                aceitos += 1
            else:
                x = random()
                if (x < exp(-delta/temp_incial)): aceitos += 1
            
            s[i], s[j] = s[j], s[i]
        
        if aceitos < gama * SAmax:
            temp_incial = beta * temp_incial
        else:
            continua = False
    return temp_incial