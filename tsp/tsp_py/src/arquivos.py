import math
from pathlib import Path

def retorna_arq(nomearq: str):
    base_dir = Path(__file__).resolve().parent.parent 
    nomearq = base_dir / 'data' / nomearq
    return nomearq


def le_arq_matriz(nomearq: str, n: int) -> list[list[float]]:
    vet_x = [0] * n
    vet_y = [0] * n
    
    try:
        with open(nomearq, 'r') as arquivo:
            for linha in arquivo:
                if not linha.strip(): 
                    continue
                partes = linha.split()
                i, x, y = int(partes[0]), int(partes[1]), int(partes[2])
                if 0 <= i < n:
                    vet_x[i] = x
                    vet_y[i] = y
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo de dados '{nomearq}' não foi encontrado.")
    except (ValueError, IndexError) as e:
        raise IOError(f"Erro ao processar o arquivo '{nomearq}'. Verifique o formato. Erro: {e}")

    distancia = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dist = math.sqrt((vet_x[i] - vet_x[j])**2 + (vet_y[i] - vet_y[j])**2)
            distancia[i][j] = dist
            distancia[j][i] = dist
            
    return distancia

def obter_parametros_pcv(nomearq: str) -> tuple[int, float]:
    try:
        with open(nomearq, 'r') as arquivo:
            linha = arquivo.readline()
            partes = linha.split()
            num_cidades = int(partes[0])
            melhor_fo_literatura = float(partes[1])
            return num_cidades, melhor_fo_literatura
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo de informações '{nomearq}' não foi encontrado.")
    except (ValueError, IndexError) as e:
        raise IOError(f"Erro ao processar o arquivo '{nomearq}'. Verifique o formato. Erro: {e}")



def imprime_fo(nomearq: str, tempo: float, fo: float, iteracao: int):
    """
    Adiciona uma linha de resultado em um arquivo de log.
    Formato: tempo    iteracao    fo
    """
    try:
        with open(nomearq, 'a') as arquivo: # 'w' para modo write (sobrescrever)
            arquivo.write(f"{tempo:8.5f}\t  {iteracao:4d}\t  {fo:7.2f}\n")
    except IOError:
        print(f"Não foi possível escrever no arquivo '{nomearq}'.")

def imprime_fo_viz(nomearq: str, tempo: float, fo: float, iteracao: int, viz_i: int, viz_j: int):
    """
    Adiciona uma linha de resultado (incluindo vizinhança) em um arquivo de log.
    Formato: tempo    iteracao    viz_i   viz_j    fo
    """
    try:
        with open(nomearq, 'a') as arquivo:
            arquivo.write(f"{tempo:8.5f}\t  {iteracao:4d}\t  {viz_i:d}\t {viz_j:d}\t {fo:7.2f}\n")
    except IOError:
        print(f"Não foi possível escrever no arquivo '{nomearq}'.")

def le_arq_vetor(nomearq: str, n: int) -> list[int]:
    """
    Lê um arquivo no formato 'índice, valor' e retorna uma lista.
    Assume que a lista deve ter tamanho 'n' e posições não especificadas
    no arquivo permanecem como 0.
    """
    vetor = [0] * n
    try:
        with open(nomearq, 'r') as arquivo:
            for linha in arquivo:
                partes = linha.split(',')
                j = int(partes[0].strip())
                valor = int(partes[1].strip())
                if 0 <= j < n:
                    vetor[j] = valor
        return vetor
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{nomearq}' não foi encontrado.")

def le_arq_vetor_denso(nomearq: str) -> list[int]:
    """
    Lê um arquivo com um valor por linha e retorna uma lista com esses valores.
    """
    vetor = []
    try:
        with open(nomearq, 'r') as arquivo:
            for linha in arquivo:
                valor = int(linha.strip())
                vetor.append(valor)
        return vetor
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{nomearq}' não foi encontrado.")

def limpa_arquivo(nomearq: str):
    try:
        with open(nomearq, 'w') as arquivo:
            pass 
    except IOError:
        print(f"Não foi possível limpar o arquivo '{nomearq}'.")