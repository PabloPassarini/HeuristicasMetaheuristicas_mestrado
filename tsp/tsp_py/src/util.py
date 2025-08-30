# -*- coding: utf-8 -*-
"""
Funções utilitárias para o problema do Caixeiro Viajante.
Tradução do código original de Marcone Jamilson Freitas Souza
"""

import random
import math

# As funções de criação e liberação de memória (cria_vetor, cria_matriz,
# libera_vetor, libera_matriz) do C++ não são necessárias em Python.
# A alocação e liberação de memória são gerenciadas automaticamente.
# Listas e listas de listas são criadas diretamente quando necessário.

def imprime_rota(s: list):
    """
    Imprime a rota da solução de forma formatada.
    Ex: 0 -> 5 -> 3 -> ... -> 0
    """
    if not s:
        print("Solução vazia.")
        return
    # 'map(str, s)' converte todos os itens da lista para string
    # ' -> '.join(...) junta os elementos com a seta
    rota_str = " -> ".join(map(str, s))
    print(f"{rota_str} -> {s[0]}")

def imprime_vetor(s: list):
    """Imprime o conteúdo de um vetor (lista) com seus índices."""
    for i, valor in enumerate(s):
        print(f"s[{i}] = {valor}")

def calcula_fo(n: int, s: list, distancia: list[list]) -> float:
    """
    Calcula a função objetivo (distância total do percurso).
    """
    dist_percorrida = 0.0
    for i in range(n - 1):
        dist_percorrida += distancia[s[i]][s[i+1]]
    
    # Adiciona a distância do último de volta ao primeiro
    dist_percorrida += distancia[s[n-1]][s[0]]
    return dist_percorrida

def randomico(min_val: float, max_val: float) -> float:
    """
    Gera um número de ponto flutuante aleatório entre min_val e max_val.
    """
    if min_val == max_val:
        return min_val
    return random.uniform(min_val, max_val)

def atualiza_vetor(s: list) -> list:
    """
    Cria e retorna uma cópia de um vetor solução.
    No original em C++, a função modificava um ponteiro. Em Python, é mais
    seguro e comum retornar uma nova cópia.
    """
    return s.copy()

def inicializa_vetor(tam: int, valor_inicial: int = 0) -> list:
    """Cria uma lista de tamanho `tam` preenchida com `valor_inicial`."""
    return [valor_inicial] * tam

def inicializa_vetor_float(tam: int, valor_inicial: float = 0.0) -> list:
    """Cria uma lista de floats de tamanho `tam` preenchida com `valor_inicial`."""
    return [valor_inicial] * tam

def embaralha_vetor(vetor: list):
    """
    Embaralha os elementos de uma lista (in-place).
    A função `random.shuffle` é o equivalente direto e eficiente.
    """
    random.shuffle(vetor)

def insere_meio_vetor(vetor: list, valor: int, pos: int):
    """
    Insere um valor em uma posição específica de uma lista.
    Python já tem o método `list.insert()` para isso.
    """
    vetor.insert(pos, valor)

def busca_pos_valor(vetor: list, valor: int) -> int:
    """
    Procura por um valor em uma lista e retorna seu índice.
    Retorna -1 se não encontrar, para simular o comportamento de busca em C.
    """
    try:
        return vetor.index(valor)
    except ValueError:
        return -1

def foi_inserida(vetor: list, cidade: int) -> bool:
    """
    Verifica se uma cidade já foi inserida na solução.
    O operador `in` do Python é a forma mais eficiente e legível.
    """
    return cidade in vetor

def calcula_desvio_padrao(fo_pop: list[float]) -> float:
    """
    Calcula o coeficiente de variação (desvio padrão / média) das FOs da população.
    Nota: O `statistics` ou `numpy` são os módulos padrão para isso em Python,
          mas aqui a implementação manual foi mantida para fidelidade ao original.
    """
    n = len(fo_pop)
    if n < 2:
        return 0.0

    media = sum(fo_pop) / n
    if media == 0:
        return 0.0
        
    somatorio = sum([(fo - media) ** 2 for fo in fo_pop])
    
    # A fórmula original usa (n-1), que é o desvio padrão amostral.
    desvio = math.sqrt(somatorio / (n - 1))
    
    # A última linha do código C++ calcula o Coeficiente de Variação, não o desvio padrão puro.
    coeficiente_variacao = desvio / media
    return coeficiente_variacao

def atualiza_arestas(arestas: list[list], prox_cid: int):
    """
    Atualiza a matriz de arestas.
    (Esta função parece ser específica para o algoritmo ERX de Algoritmos Genéticos)
    """
    for i in range(len(arestas)):
        # O primeiro elemento arestas[i][0] guarda a contagem de arestas válidas
        arestas_validas = []
        for j in range(1, len(arestas[i])):
            if arestas[i][j] == prox_cid:
                # Se encontramos a cidade a ser removida, não a adicionamos
                # à nova lista e decrementamos o contador.
                arestas[i][0] -= 1
            elif arestas[i][j] != -1:
                arestas_validas.append(arestas[i][j])
        
        # Preenche o resto da linha com -1
        padding = [-1] * (len(arestas[i]) - 1 - len(arestas_validas))
        arestas[i][1:] = arestas_validas + padding