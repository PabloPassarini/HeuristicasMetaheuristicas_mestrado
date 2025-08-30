# -*- coding: utf-8 -*-
"""
Algoritmos construtivos para gerar soluções iniciais para o TSP.
Tradução do código original de Marcone Jamilson Freitas Souza.

NOTA: Algumas funções no código C++ original estavam incompletas. A lógica
foi preenchida com base no nome e propósito do algoritmo.
"""

import random
import sys

def constroi_solucao_aleatoria(n: int) -> list[int]:
    """
    Constrói uma solução completamente aleatória (uma permutação das cidades).
    """
    s = list(range(n))
    random.shuffle(s)
    return s

def constroi_solucao_gulosa_vizinho_mais_proximo(n: int, d: list[list[float]]) -> list[int]:
    """
    Constrói uma solução via heurística do Vizinho Mais Próximo.
    Começa na cidade 0 e, a cada passo, avança para a cidade mais próxima
    ainda não visitada.

    NOTA: O laço principal deste algoritmo estava faltando no código C++ original
    e foi implementado aqui.
    """
    s = [0]  # Solução começa na cidade 0
    nao_visitadas = set(range(1, n)) # Usar um 'set' é mais eficiente para remover

    cidade_atual = 0
    while nao_visitadas:
        dist_mais_proxima = float('inf')
        cidade_mais_proxima = -1

        # Encontra a cidade mais próxima entre as não visitadas
        for proxima_cidade in nao_visitadas:
            if d[cidade_atual][proxima_cidade] < dist_mais_proxima:
                dist_mais_proxima = d[cidade_atual][proxima_cidade]
                cidade_mais_proxima = proxima_cidade
        
        # Adiciona a cidade mais próxima à solução
        s.append(cidade_mais_proxima)
        nao_visitadas.remove(cidade_mais_proxima)
        cidade_atual = cidade_mais_proxima
        
    return s

def constroi_solucao_gulosa_insercao_mais_barata(n: int, d: list[list[float]]) -> list[int]:
    """
    Constrói uma solução via heurística de Inserção Mais Barata.
    1. Cria um sub-tour inicial com 3 cidades (usando Vizinho Mais Próximo).
    2. A cada passo, encontra a cidade não visitada 'k' e a aresta '(i, j)' no tour
       que minimiza o custo de inserção: dist(i,k) + dist(k,j) - dist(i,j).
    3. Insere 'k' entre 'i' e 'j' e repete até que todas as cidades estejam no tour.
    """
    if n < 3:
        # Para menos de 3 cidades, o algoritmo não se aplica; retorna uma solução simples
        return list(range(n))

    # --- 1. Construir sub-tour inicial com 3 cidades ---
    s = [0]
    nao_visitadas = list(range(1, n))
    
    cidade_atual = 0
    for _ in range(2): # Adiciona as duas próximas cidades mais próximas
        dist_mais_proxima = float('inf')
        cidade_mais_proxima = -1
        idx_remover = -1

        for i, proxima_cidade in enumerate(nao_visitadas):
            if d[cidade_atual][proxima_cidade] < dist_mais_proxima:
                dist_mais_proxima = d[cidade_atual][proxima_cidade]
                cidade_mais_proxima = proxima_cidade
                idx_remover = i
        
        s.append(cidade_mais_proxima)
        nao_visitadas.pop(idx_remover)
        cidade_atual = cidade_mais_proxima

    # --- 2. Inserir as cidades restantes ---
    while nao_visitadas:
        melhor_custo_insercao = float('inf')
        melhor_cidade_a_inserir = -1
        melhor_posicao_insercao = -1
        idx_remover = -1

        # Para cada cidade k não visitada
        for k_idx, cidade_k in enumerate(nao_visitadas):
            # Encontra a melhor posição para inseri-la no tour atual
            for i in range(len(s)):
                cidade_i = s[i]
                cidade_j = s[(i + 1) % len(s)] # Pega a próxima cidade, fechando o ciclo

                custo = d[cidade_i][cidade_k] + d[cidade_k][cidade_j] - d[cidade_i][cidade_j]

                if custo < melhor_custo_insercao:
                    melhor_custo_insercao = custo
                    melhor_cidade_a_inserir = cidade_k
                    melhor_posicao_insercao = i + 1
                    idx_remover = k_idx
        
        # Insere a melhor cidade na melhor posição
        s.insert(melhor_posicao_insercao, melhor_cidade_a_inserir)
        nao_visitadas.pop(idx_remover)
        
    return s

def constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(n: int, d: list[list[float]], alpha: float) -> list[int]:
    """
    Constrói uma solução de forma parcialmente gulosa (estilo GRASP).
    A cada passo, em vez de escolher apenas o melhor candidato (vizinho mais próximo),
    cria-se uma Lista de Candidatos Restrita (LCR) com os "bons" candidatos e
    escolhe-se um deles aleatoriamente.
    
    NOTA: O laço principal e a lógica da LCR estavam faltando no código C++ original
    e foram implementados aqui.
    """
    s = [0]
    nao_visitadas = set(range(1, n))
    cidade_atual = 0
    
    while nao_visitadas:
        # Cria uma lista de candidatos (cidade, distância)
        candidatos = []
        for cidade in nao_visitadas:
            candidatos.append((cidade, d[cidade_atual][cidade]))
        
        # Ordena os candidatos pela distância
        candidatos.sort(key=lambda x: x[1])
        
        # Define o critério de corte para a LCR
        dist_min = candidatos[0][1]
        dist_max = candidatos[-1][1]
        limite_custo = dist_min + alpha * (dist_max - dist_min)
        
        # Monta a LCR com todos os candidatos dentro do limite
        lcr = []
        for cidade, dist in candidatos:
            if dist <= limite_custo:
                lcr.append(cidade)
            else:
                break # Como está ordenado, não haverá mais candidatos válidos
        
        # Escolhe aleatoriamente uma cidade da LCR
        cidade_escolhida = random.choice(lcr)
        
        s.append(cidade_escolhida)
        nao_visitadas.remove(cidade_escolhida)
        cidade_atual = cidade_escolhida
        
    return s


def constroi_solucao_parcialmente_gulosa_insercao_mais_barata(n: int, d: list[list[float]], alpha: float) -> list[int]:
    """
    Esta função não estava implementada no código C++ original.
    """
    print("Algoritmo 'Inserção Mais Barata Parcialmente Gulosa' não implementado.")
    # Retorna uma solução aleatória como fallback
    return constroi_solucao_aleatoria(n)