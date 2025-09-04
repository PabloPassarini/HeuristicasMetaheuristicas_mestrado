import random


def constroi_solucao_aleatoria(n: int) -> list[int]:
    s = list(range(1, n))
    random.shuffle(s)
    s.insert(0, 0)  
    return s

def constroi_solucao_gulosa_vizinho_mais_proximo(n: int, d: list[list[float]]) -> list[int]:
    s = [0]  
    nao_visitadas = set(range(1, n))

    cidade_atual = 0
    while nao_visitadas:
        dist_mais_proxima = float('inf')
        cidade_mais_proxima = -1

        for proxima_cidade in nao_visitadas:
            if d[cidade_atual][proxima_cidade] < dist_mais_proxima:
                dist_mais_proxima = d[cidade_atual][proxima_cidade]
                cidade_mais_proxima = proxima_cidade
        
        s.append(cidade_mais_proxima)
        nao_visitadas.remove(cidade_mais_proxima)
        cidade_atual = cidade_mais_proxima
        
    return s

def constroi_solucao_gulosa_insercao_mais_barata(n: int, d: list[list[float]]) -> list[int]:
    if n < 3:
        return list(range(n))
    
    s = [0]
    nao_visitadas = list(range(1, n))
    
    cidade_atual = 0
    for _ in range(2): 
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


    while nao_visitadas:
        melhor_custo_insercao = float('inf')
        melhor_cidade_a_inserir = -1
        melhor_posicao_insercao = -1
        idx_remover = -1


        for k_idx, cidade_k in enumerate(nao_visitadas):
            for i in range(len(s)):
                cidade_i = s[i]
                cidade_j = s[(i + 1) % len(s)]

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
    s = [0]
    nao_visitadas = set(range(1, n))
    cidade_atual = 0
    
    while nao_visitadas:
        candidatos = []
        for cidade in nao_visitadas:
            candidatos.append((cidade, d[cidade_atual][cidade]))
        
        candidatos.sort(key=lambda x: x[1])
        
        # Define o critério de corte para a LCR
        dist_min = candidatos[0][1]
        dist_max = candidatos[-1][1]
        limite_custo = dist_min + alpha * (dist_max - dist_min)
        
        lcr = []
        for cidade, dist in candidatos:
            if dist <= limite_custo:
                lcr.append(cidade)
            else:
                break 
        cidade_escolhida = random.choice(lcr)
        
        s.append(cidade_escolhida)
        nao_visitadas.remove(cidade_escolhida)
        cidade_atual = cidade_escolhida
        
    return s


def constroi_solucao_parcialmente_gulosa_insercao_mais_barata(n: int, d: list[list[float]], alpha: float) -> list[int]:
    if n < 3:
        return list(range(n))
    
    s = [0]
    nao_visitadas = list(range(1, n))
    
    cidade_atual = 0
    for _ in range(2):
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

    while nao_visitadas:
        candidatos = []
        for k_idx, cidade_k in enumerate(nao_visitadas):
            for i in range(len(s)):
                cidade_i = s[i]
                cidade_j = s[(i + 1) % len(s)] 
                custo = d[cidade_i][cidade_k] + d[cidade_k][cidade_j] - d[cidade_i][cidade_j]
                
                # Armazena (custo, cidade a inserir, posição de inserção, índice na lista de não visitadas)
                candidatos.append((custo, cidade_k, i + 1, k_idx))
        
        if not candidatos:
            break 

        custo_min = min(candidatos, key=lambda x: x[0])[0]
        custo_max = max(candidatos, key=lambda x: x[0])[0]
        
        # Calcula o limite de custo para a LCR
        limite_custo = custo_min + alpha * (custo_max - custo_min)
        
    
        lcr = [cand for cand in candidatos if cand[0] <= limite_custo + 1e-9] 
        custo_escolhido, cidade_escolhida, pos_escolhida, idx_remover = random.choice(lcr)
        s.insert(pos_escolhida, cidade_escolhida)
        nao_visitadas.remove(cidade_escolhida)
        
    return s