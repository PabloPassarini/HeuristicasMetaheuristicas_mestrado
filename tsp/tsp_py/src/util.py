import random
import math

def imprime_rota(s: list):
    if not s:
        print("Solução vazia.")
        return
    rota_str = " -> ".join(map(str, s))
    print(f"{rota_str} -> {s[0]}")

def imprime_vetor(s: list):
    for i, valor in enumerate(s):
        print(f"s[{i}] = {valor}")

def calcula_fo(n: int, s: list, distancia: list[list]) -> float:
    dist_percorrida = 0.0
    for i in range(n - 1):
        dist_percorrida += distancia[s[i]][s[i+1]]
    
    dist_percorrida += distancia[s[n-1]][s[0]]
    return dist_percorrida

def randomico(min_val: float, max_val: float) -> float:
    if min_val == max_val:
        return min_val
    return random.uniform(min_val, max_val)

def atualiza_vetor(s: list) -> list:
    return s.copy()

def inicializa_vetor(tam: int, valor_inicial: int = 0) -> list:
    return [valor_inicial] * tam

def inicializa_vetor_float(tam: int, valor_inicial: float = 0.0) -> list:
    return [valor_inicial] * tam

def embaralha_vetor(vetor: list):
    random.shuffle(vetor)

def insere_meio_vetor(vetor: list, valor: int, pos: int):
    vetor.insert(pos, valor)

def busca_pos_valor(vetor: list, valor: int) -> int:
    try:
        return vetor.index(valor)
    except ValueError:
        return -1

def foi_inserida(vetor: list, cidade: int) -> bool:
    return cidade in vetor

def calcula_desvio_padrao(fo_pop: list[float]) -> float:
    n = len(fo_pop)
    if n < 2:
        return 0.0

    media = sum(fo_pop) / n
    if media == 0:
        return 0.0
        
    somatorio = sum([(fo - media) ** 2 for fo in fo_pop])
    
    # A fórmula original usa (n-1), que é o desvio padrão amostral.
    desvio = math.sqrt(somatorio / (n - 1))
    coeficiente_variacao = desvio / media
    return coeficiente_variacao

def atualiza_arestas(arestas: list[list], prox_cid: int):
    for i in range(len(arestas)):
        arestas_validas = []
        for j in range(1, len(arestas[i])):
            if arestas[i][j] == prox_cid:
                arestas[i][0] -= 1
            elif arestas[i][j] != -1:
                arestas_validas.append(arestas[i][j])
        padding = [-1] * (len(arestas[i]) - 1 - len(arestas_validas))
        arestas[i][1:] = arestas_validas + padding