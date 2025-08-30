# -*- coding: utf-8 -*-
"""
Técnicas Heurísticas para resolução do Problema do Caixeiro Viajante
Tradução do código original de Marcone Jamilson Freitas Souza
"""

import time
import random

# Importaremos as funções dos outros módulos que serão criados.
# Cada um destes corresponderá a um par de arquivos .h/.cpp.
from util import calcula_fo, imprime_rota
from arquivos import obter_parametros_pcv, le_arq_matriz
from construcao import (
    constroi_solucao_gulosa_vizinho_mais_proximo,
    constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo,
    constroi_solucao_gulosa_insercao_mais_barata,
    constroi_solucao_aleatoria
)
from menus import menu_principal, menu_solucao_inicial, menu_ag
from descida import descida_best_improvement

def main():
    """
    Função principal que executa o programa.
    """
    # Pega a hora do relógio como semente para números aleatórios
    random.seed(int(time.time()))

    # Obtém parâmetros, como número de cidades (n) e melhor FO da literatura
    # Nota: Em Python, é mais comum que funções retornem valores em vez de
    #       usar ponteiros para modificar variáveis externas.
    try:
        n, melhor_fo_lit = obter_parametros_pcv(r"F:\Projetos\Programacao\HeuristicasMetaheuristicas_mestrado\tsp\tsp_py\data\c50info.txt")
        # A matriz de distâncias será uma lista de listas em Python
        d = le_arq_matriz(r"F:\Projetos\Programacao\HeuristicasMetaheuristicas_mestrado\tsp\tsp_py\data\c50.txt", n)
    except FileNotFoundError as e:
        print(f"Erro ao ler arquivo de dados: {e}")
        print("Certifique-se de que os arquivos 'data/c50info.txt' e 'data/c50.txt' existem.")
        return

    s = []  # Vetor (lista) para a solução corrente
    fo = 0.0 # Função objetivo corrente

    while True:
        escolha = menu_principal()

        if escolha == 0:
            print("\n\nBye bye!!!\n\n")
            break
        
        elif escolha == 1:  # Geração de uma solução inicial
            escolha_inicial = menu_solucao_inicial()
            
            if escolha_inicial == 1: # Gulosa - Vizinho Mais Próximo
                s = constroi_solucao_gulosa_vizinho_mais_proximo(n, d)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma gulosa (Vizinho Mais Próximo):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 2: # Parcialmente Gulosa - Vizinho Mais Próximo
                alpha = 0.1
                s = constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(n, d, alpha)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma parcialmente gulosa (Vizinho Mais Próximo):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 3: # Gulosa - Inserção Mais Barata
                s = constroi_solucao_gulosa_insercao_mais_barata(n, d)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma gulosa (Inserção Mais Barata):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 4: # Parcialmente Gulosa - Inserção Mais Barata
                print("Ainda não implementado...")

            elif escolha_inicial == 5: # Aleatória
                s = constroi_solucao_aleatoria(n)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma aleatória:")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

        elif escolha == 2:  # Descida com estratégia best improvement
            if not s:
                print("\nÉ necessário gerar uma solução inicial primeiro (Opção 1).")
                continue
            
            inicio_cpu = time.perf_counter()
            s, fo = descida_best_improvement(n, s, d)
            fim_cpu = time.perf_counter()
            
            print("\nSolução obtida usando a estratégia Best Improvement do Método da Descida:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")

        elif escolha == 3:
            print("Descida Randômica não implementado")
        elif escolha == 4:
            print("Descida com Primeiro de Melhora não implementado")
        elif escolha == 5:
            print("Multi-Start não implementado")
        elif escolha == 6:
            print("Simulated Annealing não implementado")
        elif escolha == 7:
            print("Busca Tabu não implementado")
        elif escolha == 8:
            print("Iterated Local Search não implementado")
        elif escolha == 9:
            print("GRASP não implementado")
        elif escolha == 10:
            print("VND não implementado")
        elif escolha == 11:
            print("VNS não implementado")
        
        elif escolha == 12: # Algoritmos Genéticos
            escolha_ag = menu_ag()
            if escolha_ag == 1:
                print("Algoritmos Genéticos usando operador OX não implementado")
            elif escolha_ag == 2:
                print("Algoritmos Genéticos usando operador ERX não implementado")

        elif escolha == 13:
            print("LAHC não implementado")
        elif escolha == 14:
            print("Algoritmos Meméticos não implementado")
        elif escolha == 15:
            print("Colônia de Formigas não implementado")
            
        else:
            print("\nOpção inválida...\n")

    # Em Python, a memória é gerenciada automaticamente (garbage collector),
    # então não é necessário liberar a memória da matriz 'd' manualmente.

# Ponto de entrada do script em Python
if __name__ == "__main__":
    main()