from construcao import constroi_solucao_aleatoria
import sys
from descida import descida_best_improvement, calcula_fo

def MultStart(n, d, iter_max):
    s_aux = list()
    f_aux = sys.maxsize
    for i in range(1, iter_max+1):
        s = constroi_solucao_aleatoria(n)
        s, fo = descida_best_improvement(n, s, d)
        if fo < f_aux:
            f_aux = fo
            s_aux = s.copy()

    return s_aux, f_aux
