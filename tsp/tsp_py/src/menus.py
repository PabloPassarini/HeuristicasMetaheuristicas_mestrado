def menu_principal() -> int:
    while True:
        print("""
******************* Menu Principal *************************
ATENÇÃO: Necessário gerar solução inicial antes de refinar
        1. Gerar solução inicial
        2. Descida com Best Improvement
        3. Descida randômica
        4. Descida com Primeiro de Melhora (First Improvement)
        5. Multi-Start
        6. Simulated Annealing
        7. Busca Tabu
        8. ILS (Iterated Local Search)
        9. GRASP
       10. VND (Variable Neighborhood Descent)
       11. VNS (Variable Neighborhood Search)
       12. Algoritmos Genéticos
       13. LAHC (Late Acceptance Hill-Climbing)
       14. Algoritmos Meméticos
       15. Colônia de Formigas
        0. Sair
************************************************************""")
        try:
            escolha = int(input("        Escolha: "))
            if 0 <= escolha <= 15:
                return escolha
            else:
                print("\n!!! Opção inválida. Por favor, escolha um número entre 0 e 15. !!!")
        except ValueError:
            print("\n!!! Entrada inválida. Por favor, digite apenas números. !!!")

def menu_solucao_inicial() -> int:
    while True:
        print("""
************ Geração da Solução Inicial ****************
        1. Gulosa (Vizinho mais próximo)
        2. Parcialmente gulosa (Vizinho mais próximo)
        3. Gulosa (Inserção Mais Barata)
        4. Parcialmente gulosa (Inserção Mais Barata)
        5. Aleatória
************************************************************""")
        try:
            escolha = int(input("        Escolha: "))
            if 1 <= escolha <= 5:
                return escolha
            else:
                print("\n!!! Opção inválida. Por favor, escolha um número entre 1 e 5. !!!")
        except ValueError:
            print("\n!!! Entrada inválida. Por favor, digite apenas números. !!!")

def menu_grasp() -> int:
    while True:
        print("""
******************* Menu GRASP *************************
        1. Vizinho Mais Próximo
        2. Inserção Mais Barata
************************************************************""")
        try:
            escolha = int(input("        Escolha: "))
            if 1 <= escolha <= 2:
                return escolha
            else:
                print("\n!!! Opção inválida. Por favor, escolha 1 ou 2. !!!")
        except ValueError:
            print("\n!!! Entrada inválida. Por favor, digite apenas números. !!!")

def menu_ag() -> int:
    while True:
        print("""
**************** Menu Algoritmos Genéticos **********************
        1. Operador OX (Order Crossover)
        2. Operador ERX (Edge Recombination Crossover)
************************************************************""")
        try:
            escolha = int(input("        Escolha: "))
            if 1 <= escolha <= 2:
                return escolha
            else:
                print("\n!!! Opção inválida. Por favor, escolha 1 ou 2. !!!")
        except ValueError:
            print("\n!!! Entrada inválida. Por favor, digite apenas números. !!!")