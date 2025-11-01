import sys
from descida import calcula_delta
from util import calcula_fo

def eh_tabu(pos1, pos2, listaTabu):
    """
    Verifica se o movimento (pos1, pos2) está na lista tabu.
    A listaTabu contém pares [i, j].
    """
    return [pos1, pos2] in listaTabu or [pos2, pos1] in listaTabu


def melhor_vizinho_BT(n, s, d, fo, fo_star, iterAtual, listaTabu):
    fo_melhor_viz = sys.maxsize
    melhor_i, melhor_j = -1, -1

    for i in range(n - 1):
        for j in range(i + 1, n):
            delta1 = calcula_delta(n, s, d, i, j)

            # faz o movimento temporariamente
            s[i], s[j] = s[j], s[i]

            delta2 = calcula_delta(n, s, d, i, j)
            fo_viz = fo - delta1 + delta2

            # verifica se é tabu
            tabu = eh_tabu(i, j, listaTabu)

            # critério de aspiração: aceita tabu se melhora o melhor global
            if (not tabu or fo_viz < fo_star) and fo_viz < fo_melhor_viz:
                fo_melhor_viz = fo_viz
                melhor_i, melhor_j = i, j

            # desfaz o movimento
            s[i], s[j] = s[j], s[i]

    return fo_melhor_viz, melhor_i, melhor_j


def busca_tabu(n, s, d, tamanho_max_list, BTmax):
    iterBT = 0
    MelhorIter = 0
    s_star = s.copy()  # copia da melhor solução
    listaTabu = []
    tam_corrente = tamanho_max_list

    fo_star = fo = calcula_fo(n, s, d)

    print(f"Iniciando Busca Tabu com fo = {fo:.2f}")

    while iterBT - MelhorIter < BTmax:
        iterBT += 1
        fo_viz, melhor_i, melhor_j = melhor_vizinho_BT(n, s, d, fo, fo_star, iterBT, listaTabu)

        # adiciona movimento tabu
        listaTabu.append([melhor_i, melhor_j])

        # mantém tamanho máximo da lista tabu
        while len(listaTabu) > tam_corrente:
            listaTabu.pop(0)

        # realiza o movimento
        s[melhor_i], s[melhor_j] = s[melhor_j], s[melhor_i]
        fo = fo_viz

        # atualiza melhor solução global
        if fo < fo_star:
            MelhorIter = iterBT
            s_star = s.copy()
            fo_star = fo
            print(f"Iter {iterBT}: Novo fo_star = {fo_star:.3f}")

    print("\nBusca Tabu finalizada.")
    print(f"Melhor solução encontrada: fo_star = {fo_star:.3f}")

    return fo_star, s_star
