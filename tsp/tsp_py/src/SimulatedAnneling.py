from util import calcula_fo
from random import randint, random
from descida import calcula_delta
from math import exp
from descida import descida_best_improvement
from arquivos import limpa_arquivo, imprime_fo

def temperaturaInicial(n, s, d, beta, gama, SAmax, temp_incial):
    continua = True

    while continua:
        aceitos = 0
        for iterT in range(1, SAmax+1):
            i = randint(1, n-1)
            j = randint(1, n-1)
            while i == j: 
                j = randint(1, n-1)
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


def SimulatedAnnealing(n, s, d, alpha, SAmax, temp_inicial, temp_final):
    s_aux = s.copy()
    
    f_aux = fo = calcula_fo(n, s, d)
    temp = temp_inicial
    
    limpa_arquivo("SA.txt")
    arq = open("SA.txt", "a")
    arq.write(f"f_aux: {f_aux:.2f}  \t Temperatura: {temp:.2f}\n")

    while temp > temp_final: #colocando temp > 0, o loop nunca acaba
        iter = 0
        while iter < SAmax:
            iter += 1
            i = randint(1, n-1)
            j = randint(1, n-1)
            while i == j: 
                j = randint(1, n-1)
            
            delta1 = calcula_delta(n,s,d,i, j)
            s[i], s[j] = s[j], s[i]
            delta2 = calcula_delta(n, s, d, i, j)
            fo_viz = fo - delta1 + delta2
            delta = -delta1 + delta2    

            if delta < 0:
                fo = fo_viz
                if fo < f_aux:
                    f_aux = fo
                    s_aux = s.copy()
                    arq.write(f"f_aux: {f_aux:.2f}  \t Temperatura: {temp:.2f}\n")
            else:
                x = random()
                if (x < exp(-delta/temp)): 
                    fo = fo_viz
                else:
                    s[i], s[j] = s[j], s[i]
        temp = alpha * temp
        iter = 0
    arq.close()
   
    return f_aux, s_aux