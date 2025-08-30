# -*- coding: utf-8 -*-
"""
Algoritmos de Busca Local (Descida) para refinar soluções para o TSP.
Tradução do código original de Marcone Jamilson Freitas Souza.

NOTA: Várias funções no código C++ original estavam incompletas. A lógica
foi preenchida com base no nome e propósito do algoritmo. A avaliação de
vizinhança também foi otimizada para maior eficiência.
"""
import time
import random
from util import calcula_fo
from arquivos import limpa_arquivo, imprime_fo

def avalia_troca(n: int, s: list, d: list[list[float]], i: int, j: int) -> float:
    """
    Calcula de forma EFICIENTE a variação no custo (delta) ao trocar as cidades nas posições i e j.
    Esta função substitui a lógica ineficiente de 'calcula_delta' do C++.
    Um delta < 0 significa melhora.
    """
    # Garante que i seja o menor índice
    if i > j:
        i, j = j, i

    # Cidades atuais nas posições i e j
    cidade_i, cidade_j = s[i], s[j]

    # Vizinhas de i e j no tour
    # O operador % n garante o comportamento circular do tour
    antes_i, depois_i = s[(i - 1 + n) % n], s[(i + 1) % n]
    antes_j, depois_j = s[(j - 1 + n) % n], s[(j + 1) % n]
    
    # Caso especial: i e j são adjacentes no tour
    if j == i + 1 or (i == 0 and j == n - 1):
        # Arestas a remover: (antes_i, i), (j, depois_j)
        # Arestas a adicionar: (antes_i, j), (i, depois_j)
        custo_removido = d[antes_i][cidade_i] + d[cidade_j][depois_j]
        custo_adicionado = d[antes_i][cidade_j] + d[cidade_i][depois_j]
        return custo_adicionado - custo_removido

    # Caso geral: i e j não são adjacentes
    # Arestas a remover: (antes_i, i), (i, depois_i), (antes_j, j), (j, depois_j)
    # Arestas a adicionar: (antes_i, j), (j, depois_i), (antes_j, i), (i, depois_j)
    custo_removido = d[antes_i][cidade_i] + d[cidade_i][depois_i] + \
                     d[antes_j][cidade_j] + d[cidade_j][depois_j]
                     
    custo_adicionado = d[antes_i][cidade_j] + d[cidade_j][depois_i] + \
                       d[antes_j][cidade_i] + d[cidade_i][depois_j]
    
    return custo_adicionado - custo_removido

def encontra_melhor_vizinho_swap(n: int, s: list, d: list[list[float]]) -> tuple[int, int, float]:
    """
    Explora toda a vizinhança de troca (swap) e retorna o melhor movimento.
    Retorna: (melhor_i, melhor_j, delta_do_melhor_movimento)
    """
    melhor_delta = float('inf')
    melhor_i, melhor_j = -1, -1

    for i in range(n):
        for j in range(i + 1, n):
            delta = avalia_troca(n, s, d, i, j)
            if delta < melhor_delta:
                melhor_delta = delta
                melhor_i, melhor_j = i, j
    
    return melhor_i, melhor_j, melhor_delta

def descida_best_improvement(n: int, s: list, d: list[list[float]]) -> tuple[list, float]:
    """
    Aplica a busca local de Descida com a estratégia Best Improvement.
    A cada iteração, avalia toda a vizinhança e aplica a melhor melhora encontrada.
    Repete até que nenhum vizinho seja melhor que a solução atual (ótimo local).

    NOTA: O laço principal deste algoritmo estava faltando no C++ e foi implementado.
    """
    s_atual = s.copy()
    fo = calcula_fo(n, s_atual, d)
    iter = 0
    
    limpa_arquivo("DescidaBI.txt")
    inicio_cpu = time.perf_counter()
    imprime_fo("DescidaBI.txt", time.perf_counter() - inicio_cpu, fo, iter)

    while True:
        melhor_i, melhor_j, melhor_delta = encontra_melhor_vizinho_swap(n, s_atual, d)
        
        if melhor_delta < -1e-9:  # Usar uma pequena tolerância para melhora
            # Aplica a troca
            s_atual[melhor_i], s_atual[melhor_j] = s_atual[melhor_j], s_atual[melhor_i]
            fo += melhor_delta
            iter += 1
            imprime_fo("DescidaBI.txt", time.perf_counter() - inicio_cpu, fo, iter)
        else:
            # Atingiu um ótimo local, nenhum vizinho melhora a solução
            break
            
    imprime_fo("DescidaBI.txt", time.perf_counter() - inicio_cpu, fo, iter)
    return s_atual, fo

def descida_first_improvement(n: int, s: list, d: list[list[float]]) -> tuple[list, float]:
    """
    Aplica a busca local de Descida com a estratégia First Improvement.
    Explora a vizinhança em ordem aleatória e aplica a *primeira* melhora que encontrar.
    Repete até que uma varredura completa da vizinhança não encontre melhora.

    NOTA: O laço principal deste algoritmo estava faltando no C++ e foi implementado.
    """
    s_atual = s.copy()
    fo = calcula_fo(n, s_atual, d)
    iter = 0
    
    limpa_arquivo("DescidaFI.txt")
    inicio_cpu = time.perf_counter()
    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo, iter)
    
    melhorou = True
    while melhorou:
        melhorou = False
        indices = list(range(n))
        random.shuffle(indices) # Explora a vizinhança em ordem aleatória

        for i_idx in range(n):
            if melhorou: break
            for j_idx in range(i_idx + 1, n):
                i, j = indices[i_idx], indices[j_idx]
                delta = avalia_troca(n, s_atual, d, i, j)

                if delta < -1e-9:
                    s_atual[i], s_atual[j] = s_atual[j], s_atual[i]
                    fo += delta
                    melhorou = True
                    iter += 1
                    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo, iter)
                    break # Sai do laço interno e reinicia a busca
    
    imprime_fo("DescidaFI.txt", time.perf_counter() - inicio_cpu, fo, iter)
    return s_atual, fo


def descida_randomica(n: int, s: list, d: list[list[float]], iter_max: int) -> tuple[list, float]:
    """
    Esta função não estava implementada no código C++ original.
    """
    print("Algoritmo 'Descida Randômica' não implementado.")
    # Retorna a solução inicial sem modificação
    return s, calcula_fo(n, s, d)