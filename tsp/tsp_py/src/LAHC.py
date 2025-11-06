from util import calcula_fo
from random import randint

def LAHC(n, s, d, l, m):
    fp = [calcula_fo(n, s, d)] * l
    s_star = s.copy()
    fo_star = calcula_fo(n, s, d)
    p,r = 0,0

    while r < m:
        i = randint(0, len(s)-1)
        j = randint(0, len(s)-1)
        while i == j: 
            j = randint(0, len(s)-1)  
        
        s_ll = s.copy()
        s_ll[i], s_ll[j] = s_ll[j], s_ll[i]

        fo_s = calcula_fo(n, s, d)
        fo_ll = calcula_fo(n, s_ll, d)
        if fo_ll < fo_star or fo_ll <= fp[p]:
            s = s_ll
            if fo_ll < fo_s:
                r = 0

            if fo_ll < fo_star:
                s_star = s.copy()
                fo_star = fo_s
        
        fp[p] = fo_s
        p = (p + 1) % l
        r += 1
    return fo_star, s_star