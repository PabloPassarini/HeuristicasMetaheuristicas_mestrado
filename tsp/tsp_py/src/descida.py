import random
import time
from util import calcula_fo
from arquivos import imprime_fo, limpa_arquivo

def calcula_delta(n: int, s: list, d: list[list], i: int, j: int) -> float:
    i_antes = (i - 1)
    i_depois = (i + 1)
    j_antes = (j - 1)
    j_depois = (j + 1)

    if i == 0: i_antes = n - 1 #se i for a primeira cid
    if i == n - 1: i_depois = 0
    if j == 0: j_antes = n - 1
    if j == n - 1: j_depois = 0

    delta = d[s[i_antes]][s[i]] + d[s[i]][s[i_depois]] + d[s[j_antes]][s[j]] + d[s[j]][s[j_depois]]
    return delta

def melhor_vizinho(n, s, d, fo, melhor_i=-1, melhor_j=-1):
    fo_melhor_viz = fo
    for i in range(n - 1):
        for j in range(i + 1, n):
            delta1 = calcula_delta(n, s, d, i, j)
            s[i], s[j] = s[j], s[i] #Seria o comando swap do c++
            delta2 = calcula_delta(n, s, d, i, j)

            fo_viz = fo - delta1 + delta2
            if fo_viz < fo_melhor_viz:
                fo_melhor_viz = fo_viz
                melhor_i = i
                melhor_j = j
            
            s[i], s[j] = s[j], s[i]
    return fo_melhor_viz, melhor_i, melhor_j


def descida_randomica(n, s, d, IterMax):
    Iter = 0
    IterStop = 0
    if IterMax >= 100:
        base = len(str(IterMax))-1
        Iterflag = 10**(base//2)
    else:
        Iterflag = IterMax
    

    fo = calcula_fo(n, s, d)
    inicioCPU = time.time()
    fimCPU = time.time()
    limpa_arquivo('DescidaFI.txt')
    imprime_fo('DescidaFI.txt', fimCPU - inicioCPU, fo, 0)
    while Iter < IterMax:
        Iter += 1
        IterStop += 1
        
        if IterStop == Iterflag: break
        
        i = random.randint(1, n - 2) #usar um vetor de indices para embaralhar
        j = random.randint(1, n - 2)
        
        if i != j:
            s[i], s[j] = s[j], s[i]
            fo_novo = calcula_fo(n, s, d)
            if fo_novo < fo and fo_novo > 0:
                fo = fo_novo
                IterStop = 0
            else:
                s[i], s[j] = s[j], s[i]
                IterStop += 1

        fimCPU = time.time()
        imprime_fo('DescidaFI.txt', fimCPU - inicioCPU, fo, Iter)

    
    return s, fo


def descida_first_improvement(n, s, d):
    s_atual = s.copy()
    fo_atual = calcula_fo(n, s_atual, d)  # FO inicial
    iter_melhora = 0
    
    inicio_cpu = time.perf_counter()
    limpa_arquivo("DescidaFI.txt")
    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo_atual, iter_melhora)
    
    melhorou = True
    while melhorou:
        melhorou = False
        
        # embaralha os índices das cidades (não inclui 0 e n-1)
        indices = list(range(1, n - 1))
        random.shuffle(indices)

        for i_idx in range(len(indices)):
            if melhorou:   # se já achou uma melhora, sai do loop externo também
                break
            for j_idx in range(i_idx + 1, len(indices)):
                i, j = indices[i_idx], indices[j_idx]
                
                fo_vizinho, melhor_i, melhor_j = melhor_vizinho(n, s_atual, d, fo_atual)
                if fo_atual < 0 or fo_vizinho < 0:
                    break
                if fo_vizinho < fo_atual:
                    # aplica a troca
                    s_atual[i], s_atual[j] = s_atual[j], s_atual[i]
                    fo_atual = fo_vizinho
                    
                    melhorou = True
                    iter_melhora += 1
                    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo_atual, iter_melhora)
                    break   # sai do for j_idx
    
    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo_atual, iter_melhora)
    return s_atual, fo_atual

def descida_best_improvement(n, s, d):
    
    fo = calcula_fo(n, s, d)
    melhorou = True
    iteracao = 0
    inicio_cpu = time.time()
    limpa_arquivo("DescidaBI.txt")
    while melhorou:
        melhorou = False
        
        fo_viz, i, j = melhor_vizinho(n, s, d, fo)
        if i != -1 and fo_viz < fo and i != 0:
            s[i], s[j] = s[j], s[i]  # aplica troca
            fo = fo_viz
            melhorou = True
        iteracao += 1

        fim_cpu = time.time()
        imprime_fo("DescidaBI.txt", fim_cpu - inicio_cpu, fo, iteracao)
    
    return s, fo