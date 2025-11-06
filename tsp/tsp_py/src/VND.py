from descida import descida_best_improvement


def VND(n, s, d, r, fo):
    it = 0
    print(f"Iter VNS: {it} \t fo_star: {fo}")

    pare = False
    while not pare:
        k = 1
        it += 1
        s_l = s.copy()
        fo_l = fo
        
        while k<=r:
            s_ll, fo_ll = descida_best_improvement(n, s, d)
            s, fo, k = gera_vizinho_qualquer(s, fo, s_ll, fo_ll, k)
            print(f"Iter VNS: {it} \t fo_star: {fo} \t k: {k}")
        if fo <= fo_l:
            pare = True
            fo_l = fo
            s_l = s.copy()
        
        
    return fo_l, s_l




def gera_vizinho_qualquer(s, fo, s_l, fo_l, k):
    match k:
        case 1:
            s, fo, k = sequential_neighborhood_change_step(s, fo, s_l, fo_l, k)
        case 2:
            s, fo, k = pipe_neighborhood_change_step(s, fo, s_l, fo_l, k)
        case 3:
            s, fo, k = cyclic_neighborhood_change_step(s, fo, s_l, fo_l, k)
    return s, fo, k


def sequential_neighborhood_change_step(s, fo, s_l, fo_l, k):
    if fo_l < fo:
        s = s_l.copy()
        fo = fo_l
        k = 1
    else:
        k += 1
    return s, fo, k

def pipe_neighborhood_change_step(s, fo, s_l, fo_l, k):
    if fo_l < fo:
        s = s_l.copy()
        fo = fo_l
    else:
        k += 1
    return s, fo, k

def cyclic_neighborhood_change_step(s, fo, s_l, fo_l, k):
    k += 1
    if fo_l < fo:
        s = s_l.copy()
        fo = fo_l
    return s, fo, k