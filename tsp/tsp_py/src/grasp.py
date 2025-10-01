from construcao import constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo
import sys
from descida import descida_best_improvement, calcula_fo, descida_first_improvement, descida_randomica

def metod_GRASP(n, s, d, alp, GRASPmax):
    fo_star = sys.maxsize
    s_star = list()
    for iter in range(GRASPmax):
        s = constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(n,d,alp)
        fo_antes = calcula_fo(n, s, d)

        s, fo = descida_best_improvement(n, s, d)
        #s, fo = descida_first_improvement(n, s, d)
        #s, fo = descida_randomica(n, s, d, 100)
        #print(f'Fo_antes: {fo_antes:.4f}  ||  Fo: {fo:.4f}')
        if fo < fo_star:
            fo_star = fo
            s_star = s
    
    return fo_star,s_star