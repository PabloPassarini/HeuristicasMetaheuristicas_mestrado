import time
import random

from util import calcula_fo, imprime_rota
from arquivos import obter_parametros_pcv, le_arq_matriz, retorna_arq
from construcao import (
    constroi_solucao_gulosa_vizinho_mais_proximo,
    constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo,
    constroi_solucao_gulosa_insercao_mais_barata,
    constroi_solucao_parcialmente_gulosa_insercao_mais_barata,
    constroi_solucao_aleatoria
)
from menus import menu_principal, menu_solucao_inicial, menu_ag
from descida import descida_best_improvement, descida_randomica, descida_first_improvement
from SimulatedAnneling import temperaturaInicial, SimAnn
from MultStart import MultStart
from grasp import metod_GRASP

def main():
    random.seed(int(time.time()))
    try:
        c50info = retorna_arq("c50info.txt")
        c50 = retorna_arq("c50.txt")
        n, melhor_fo_lit = obter_parametros_pcv(c50info)
        d = le_arq_matriz(c50, n)

    except FileNotFoundError as e:
        print(f"Erro ao ler arquivo de dados: {e}")
        print("Certifique-se de que os arquivos 'data/c50info.txt' e 'data/c50.txt' existem.")
        return

    s = []
    fo = 0.0

    while True:
        escolha = menu_principal()

        if escolha == 0:
            print("\n\nBye bye!!!\n\n")
            break
        
        elif escolha == 1:
            escolha_inicial = menu_solucao_inicial()
            
            if escolha_inicial == 1:
                s = constroi_solucao_gulosa_vizinho_mais_proximo(n, d)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma gulosa (Vizinho Mais Próximo):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 2:
                alpha = 0.1
                s = constroi_solucao_parcialmente_gulosa_vizinho_mais_proximo(n, d, alpha)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma parcialmente gulosa (Vizinho Mais Próximo):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 3:
                s = constroi_solucao_gulosa_insercao_mais_barata(n, d)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma gulosa (Inserção Mais Barata):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 4:
                alpha = 0.3
                s = constroi_solucao_parcialmente_gulosa_insercao_mais_barata(n, d, alpha)
                fo = calcula_fo(n, s, d)
                print(f"\nSolução construída de forma parcialmente gulosa (Inserção Mais Barata com alpha={alpha}):")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

            elif escolha_inicial == 5:
                s = constroi_solucao_aleatoria(n)
                fo = calcula_fo(n, s, d)
                print("\nSolução construída de forma aleatória:")
                imprime_rota(s)
                print(f"Função objetivo = {fo:.2f}")

        elif escolha == 2:
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
            if not s:
                print("\nÉ necessário gerar uma solução inicial primeiro (Opção 1).")
                continue
            try:
                iter_max = int(input("Digite o número máximo de iterações para a Descida Randômica: "))
            except ValueError:
                print("Entrada inválida. Usando 1000 iterações como padrão.")
                iter_max = 1000

            inicio_cpu = time.perf_counter()
            s, fo = descida_randomica(n, s, d, iter_max)
            fim_cpu = time.perf_counter()

   
            print("\nSolução obtida usando a Descida Randômica:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")

        elif escolha == 4:
            if not s:
                print("\nÉ necessário gerar uma solução inicial primeiro (Opção 1).")
                continue
            
            inicio_cpu = time.perf_counter()
            s, fo = descida_first_improvement(n, s, d)
            fim_cpu = time.perf_counter()
            
            print("\nSolução obtida usando a estratégia First Improvement do Método da Descida:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")

        elif escolha == 5:
            inicio_cpu = time.perf_counter()
            s, fo = MultStart(n, d, iter_max=100)
            fim_cpu = time.perf_counter()
            print("\nSolução obtida usando a estratégia Multi-Start:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")
        elif escolha == 6:
            inicio_cpu = time.perf_counter()
            temp_inicial = temperaturaInicial(n, s, d, beta=2, gama=0.9, SAmax=500, temp_incial=10) #temp final 0.01
            fo, s = SimAnn(n, s, d, alpha=0.95, SAmax=500, temp_inicial=temp_inicial, temp_final=0.01)
            fim_cpu = time.perf_counter()

            print("\nSolução obtida usando a estratégia Simulated Annealing:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")

        elif escolha == 7:
            print("Busca Tabu não implementado")
        elif escolha == 8:
            print("Iterated Local Search não implementado")
        elif escolha == 9:
            inicio_cpu = time.perf_counter()
            fo, s = metod_GRASP(n, s, d, 0.1, 100)
            fim_cpu = time.perf_counter()

            print("\nSolução obtida usando a estratégia GRASP:")
            imprime_rota(s)
            print(f"Função objetivo = {fo:.2f}")
            print(f"Tempo de CPU = {fim_cpu - inicio_cpu:.6f} segundos")
        elif escolha == 10:
            print("VND não implementado")
        elif escolha == 11:
            print("VNS não implementado")
        
        elif escolha == 12:
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

if __name__ == "__main__":
    main()