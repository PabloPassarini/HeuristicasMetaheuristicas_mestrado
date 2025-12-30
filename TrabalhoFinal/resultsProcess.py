import pandas as pd


def calcula_gap(lit, vns): #Calculo do gap entre as metodologias da literatura com o do vns
    return ((vns - lit)/lit)*100



instancias_p = [

    ('E-n29-k4-s7.evrp', 383, 383),
    ('E-n30-k3-s7.evrp', 577, 582),
    ('E-n35-k3-s5.evrp', 527, 530),
    ('E-n37-k4-s4.evrp', 865, 865),
    ('E-n60-k5-s9.evrp', 585, 544),
    ('F-n49-k4-s4.evrp', 740, 769)
]
instancias_g = [
    ('E-n89-k7-s13.evrp', 724, 0),
    ('E-n112-k8-s11.evrp', 860, 0),
    ('M-n110-k10-s9.evrp', 914, 0),
    ('M-n126-k7-s5.evrp', 1099, 0),
    ('M-n163-k12-s12.evrp', 1109 ,0)
]

colunas = ['instancia', 'capacidade_carga', 'capacidade_energia', 't_avg',
       'fo(best)', 'media_d', 'distancia(best)', 'caminho(best)',
       'demanda_rotas(melhor)', 'violacao_demanda(melhor)',
       'N_recargas(melhor)', 'energia_gasta_rotas(melhor)',
       'N_violacao_energia(melhor)']
resultados = pd.read_csv(r'F:\Projetos\Programacao\HeuristicasMetaheuristicas_mestrado\TrabalhoFinal\Resultados\resultados.csv', sep=';', encoding='utf8', decimal='.')

for r in resultados.values.tolist():
    for inst in instancias_g:
        if inst[0] == r[0]:
            #print(f'{r[0]} & {str(inst[1])} & {str(inst[2])} & {str(round(r[6], 2))} & {str(round(r[5], 2))} & {str(round(calcula_gap(inst[1], r[6]), 1))} & & {str(round(calcula_gap(inst[2], r[6]), 1))} & {str(r[3])} \\\ ')
            print(f'{r[0]} & {str(inst[1])} & {str(round(r[6], 2))} & {str(round(r[5], 2))} & {str(round(calcula_gap(inst[1], r[6]), 1))} & {str(r[3])} \\\ ')
