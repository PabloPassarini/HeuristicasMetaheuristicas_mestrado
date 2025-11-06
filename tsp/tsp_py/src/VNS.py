from random import randint
from descida import calcula_delta, descida_best_improvement
from util import calcula_fo


def VNS(n, s, d, VNS_max, r, fo):
    iter = 0
    melhor_iter = 0
    print(f"Iter VNS: {iter} \t fo_star: {fo}")

    while(iter - melhor_iter < VNS_max):
        iter += 1
        k = 1
        while(k<=r):
            fo_l, s_l = gera_vizinho_qualquer(n, s, d, fo, k)
            s_ll = descida_best_improvement(n, s_l, d)[0]
            fo_ll = calcula_fo(n, s_ll,d)
            if fo_ll < fo:
                s = s_ll.copy()
                fo = fo_ll
                k = 1
            else:
                k += 1
        print(f"Iter VNS: {iter} \t fo_star: {fo}")
    
    return fo, s

def gera_vizinho_qualquer(n, s, d, fo, k):
    match k:
        case 1:
            fo_viz, s_l = vizinho_reinsercao1_qualquer(n, s, d, fo)
        case 2:
            fo_viz, s_l = vizinho_troca_qualquer(n, s, d, fo)
        case 3:
            fo_viz, s_l = vizinho_reinsercao2_qualquer(n, s, d, fo)
    return fo_viz, s_l

def vizinho_troca_qualquer(n, s, d, fo):
    j = randint(0, n-1)
    i = randint(0, n-1)
    while i == j and j != i+1:
        i = randint(0, n-1)


    delta1 = calcula_delta(n, s, d, i, j)
    s[i], s[j] = s[j], s[i]
    delta2 = calcula_delta(n, s, d, i, j)

    fo_viz = fo - delta1 + delta2
    
    return fo_viz, s

def encontra_ij(n):
    j = randint(0, n-1)
    i = randint(0, n-1)
    while i == j: 
        i = randint(0, n-1)

    return i, j


def vizinho_reinsercao1_qualquer(n, s, d, fo):
    while True:
        i, j = encontra_ij(n)
        if (i == 0 and j == n-1) or (i == n-1 and j == 0):
            i, j = encontra_ij(n)
        else:
            break

    print(i, j)       
    valor = s[i]
    s.remove(valor)
    s.insert(j+1, valor)
    
    if i == n-1:
        prox_i = 0
        fo_viz = fo - (d[i-1][i] + d[i][prox_i]) + d[i-1][prox_i] - d[j][j+1] + (d[j][i] + d[i][j+1])
    elif j == n-1:
        prox_j = 0
        fo_viz = fo - (d[i-1][i] + d[i][i+1]) + d[i-1][i+1] - d[j][prox_j] + (d[j][i] + d[i][prox_j])
    else:
        fo_viz = fo - (d[i-1][i] + d[i][i+1]) + d[i-1][i+1] - d[j][j+1] + (d[j][i] + d[i][j+1])

    return fo_viz, s

def vizinho_reinsercao2_qualquer(n, s, d, fo):
    j = randint(0, n-1)
    i = randint(0, n-1)
    while i == j and j != i+1:
        i = randint(0, n-1)

    if i == n-1: i = -1
    if j == n-1: j = -1
    
    valor1 = s[i]
    valor2 = s[i+1]
    s.remove(valor1)
    s.remove(valor2)
    s.insert(j+1, valor1)
    s.insert(j+2, valor2)

    #depois implemenar a forma otimizada
    fo_viz = calcula_fo(n, s, d)
    return fo_viz, s
