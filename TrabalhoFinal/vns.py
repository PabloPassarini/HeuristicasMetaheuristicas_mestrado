import random
import time, copy
from util import calcula_fo_first_version


def calculo_energia(distancia, consumo):
    return distancia * consumo

def construcao_solInicial(instancia):
    depot_id = instancia['depot_id']
    vehicles = instancia['vehicles']
    mat_d = instancia['mat_d']
    capacity = instancia['capacity']
    demands_dict = {c: d for c, d in instancia['demands']}


    random.seed(time.time())

    # Separa clientes (excluindo depósito)
    clientes = [c for c, d in instancia['demands'] if c != depot_id]
    
    unassigned = clientes.copy()
    random.shuffle(unassigned)

    # Inicializa rotas: [deposito, deposito]
    routes = [[depot_id, depot_id] for _ in range(vehicles)]
    loads = [0] * vehicles

    for c in unassigned[:]: 
        best = None
        best_cost = float('inf')

        for v in range(vehicles):
            # Verifica Capacidade
            if loads[v] + demands_dict[c] > capacity:
                continue

            r = routes[v]
            # Tenta todas as posições possíveis entre o início e o fim da rota
            for pos in range(1, len(r)):
                a = r[pos-1]
                b = r[pos]

                # Custo de inserção: (A->C + C->B) - A->B
                cost = mat_d[a-1][c-1] + mat_d[c-1][b-1] - mat_d[a-1][b-1]

                if cost < best_cost:
                    best_cost = cost
                    best = (v, pos)

        if best is not None:
            v, pos = best
            routes[v].insert(pos, c)
            loads[v] += demands_dict[c]
            unassigned.remove(c)


    while unassigned:
        c = unassigned.pop(0)
        # Encontra rota com menor carga atual
        v_menor_carga = loads.index(min(loads))
        routes[v_menor_carga].insert(-1, c)
        loads[v_menor_carga] += demands_dict[c]


    
    stations = instancia['stations']
    autonomia_max = instancia['energy_capacity']
    consumo = instancia['energy_consumption']
    
    final_routes = []

    for r in routes:
        new_route = [r[0]] # Começa com depósito
        current_energy = autonomia_max
        
        # Percorre os destinos da rota original (começando do índice 1)
        for i in range(1, len(r)):
            origin = new_route[-1] 
            dest = r[i]            
            
            # Distância e energia para ir direto
            dist_org_dest = mat_d[origin-1][dest-1]
            energy_needed = calculo_energia(dist_org_dest, consumo)
            

            buffer_safety = 0
            
            if dest != depot_id:
                # Calcula a energia necessária do DESTINO até a estação mais próxima DELE
                min_energy_escape = float('inf')
                for s in stations:
                    d_dest_s = mat_d[dest-1][s-1]
                    e_escape = calculo_energia(d_dest_s, consumo)
                    if e_escape < min_energy_escape:
                        min_energy_escape = e_escape
                buffer_safety = min_energy_escape

            # Decisão: Posso ir direto?
            # Tenho energia para ir + energia para escapar se precisar?
            if current_energy >= (energy_needed + buffer_safety):
                new_route.append(dest)
                current_energy -= energy_needed
            else:                
                best_station = None
                min_detour = float('inf')

                for s in stations:
                    # Distâncias
                    d_org_s = mat_d[origin-1][s-1]
                    d_s_dest = mat_d[s-1][dest-1]
                    
                    e_to_s = calculo_energia(d_org_s, consumo)
                    e_from_s = calculo_energia(d_s_dest, consumo)

                    # 1. Consigo chegar na estação agora?
                    reachable_now = (current_energy >= e_to_s)
                    
                    # 2. Se eu carregar lá, consigo chegar no destino?
                    reachable_dest = (autonomia_max >= e_from_s)

                    if reachable_now and reachable_dest:
                        total_dist_segment = d_org_s + d_s_dest
                        if total_dist_segment < min_detour:
                            min_detour = total_dist_segment
                            best_station = s
                
                if best_station is not None:
                    # Inserir Estação
                    new_route.append(best_station)
                    current_energy = autonomia_max 
                    

                    new_route.append(dest)
                    # Desconta energia da Estação até o Destino
                    d_s_dest = mat_d[best_station-1][dest-1]
                    current_energy -= calculo_energia(d_s_dest, consumo)
                else:
                    new_route.append(dest)
                    current_energy = -1 # Energia negativa sinaliza problema

        final_routes.append(new_route)
    return final_routes

def ajusta_rota(s, depot):
    for i in range(len(s)):
        meio = [x for x in s[i] if x != depot]
        s[i] = [depot] + meio + [depot]
    return s


def busca_vizinhanca(s, atual_fo, atual_d, viz_type, vns_args):
    n_rotas = len(s)
    id_rotas = list(range(n_rotas))
    random.shuffle(id_rotas)

    if viz_type == 'relocate':
        for a in id_rotas:
            for i in range(1, len(s[a]) - 1):

                for b in id_rotas:
                    for j in range(1, len(s[b])):

                        if a == b and j in (i, i+1): 
                            continue

                        # aplica movimento
                        op = apply_relocate(s, a, i, b, j)

                        s = ajusta_rota(s, vns_args["depot_id"])
                        fo_aux, d_aux = calcula_fo_first_version(s, vns_args, vns_args["vehicles"])


                        if fo_aux < atual_fo:  
                            return fo_aux, d_aux, True

                        # desfaz
                        undo_relocate(s, *op)
    elif viz_type == 'swap':
        for a in id_rotas:
            for b in id_rotas:
                if a == b: 
                    continue

                for i in range(1, len(s[a])-1):
                    for j in range(1, len(s[b])-1):

                        apply_swap(s, a, i, b, j)

                        fo_aux, d_aux = calcula_fo_first_version(s, vns_args, vns_args["vehicles"])

                        if fo_aux < atual_fo:
                            return fo_aux, d_aux, True

                        undo_swap(s, a, i, b, j)
    elif viz_type == 'intra_relocate':
        for r in id_rotas:
            for i in range(1, len(s[r])-1):
                for j in range(1, len(s[r])-1):
                    if i == j:
                        continue

                    op = apply_relocate(s, r, i, r, j)

                    fo_aux, d_aux = calcula_fo_first_version(s, vns_args, vns_args["vehicles"])

                    if fo_aux < atual_fo:
                        return fo_aux, d_aux, True

                    undo_relocate(s, *op)
    elif viz_type == 'intra_swap':
        for r in id_rotas:
            for i in range(1, len(s[r])-2):
                for j in range(i+1, len(s[r])-1):

                    apply_swap(s, r, i, r, j)

                    fo_aux, d_aux = calcula_fo_first_version(s, vns_args, vns_args["vehicles"])

                    if fo_aux < atual_fo:
                        return fo_aux, d_aux, True

                    undo_swap(s, r, i, r, j)

    return atual_fo, atual_d, False

def RVND(s, vns_args, max_vehicles):
    vizinhancas = ['relocate', 'swap', 'relocate2',
                   'intra_relocate', 'intra_swap',
                   'insert_station', 'remove_station']

    atual_s = ajusta_rota(s, vns_args["depot_id"])
    atual_fo, atual_d = calcula_fo_first_version(atual_s, vns_args, max_vehicles)


    while True:
        viz_list = vizinhancas[:]              # Reinicia todas as vizinhanças
        random.shuffle(viz_list)               # Passo fundamental do RVND

        melhorou_global = False                # Flag para saber se devemos repetir o ciclo completo

        # Enquanto ainda existirem vizinhanças para testar
        while viz_list:

            viz = viz_list[0]                  #
            
            # Verificação de tempo
            if time.time() - vns_args['start_time'] > vns_args['max_time']:
                return atual_fo, atual_d, atual_s

            cand_fo, cand_d, melhorou = busca_vizinhanca(
                atual_s, atual_fo, atual_d, viz, vns_args
            )

            if melhorou:
                # Atualiza solução
                atual_fo = cand_fo
                atual_d  = cand_d

                # IMPORTANTE: Reinicia TODAS as vizinhanças
                random.shuffle(viz_list)
                melhorou_global = True
                break  # Sai para reiniciar as vizinhanças do RVND

            else:
                # Remove a vizinhança que NÃO melhorou
                viz_list.pop(0)

        if not melhorou_global:
            break  # Nenhuma vizinhança melhorou → fim do RVND

    return atual_fo, atual_d, atual_s


def undo_swap(s, a, i, b, j):
    s[a][i], s[b][j] = s[b][j], s[a][i]

def apply_swap(s, a, i, b, j):
    s[a][i], s[b][j] = s[b][j], s[a][i]

def undo_relocate(s, a, i, b, j):
    node = s[b].pop(j)
    s[a].insert(i, node)

def apply_relocate(s, a, i, b, j):
    node = s[a][i]

    # Remove
    s[a].pop(i)

    # Ajuste se for mesma rota e o destino é depois da remoção
    if a == b and j > i:
        j -= 1

    # Insere
    s[b].insert(j, node)

    return (a, i, b, j)

def clone_route(route):
    return route[:]  


def shake(s, k):
    s2 = copy.deepcopy(s)
    viz = ['relocate', 'swap', 'intra_relocate', 'intra_swap']

    for _ in range(k):
        move = random.choice(viz)
        applied = False
        tentativas = 0
        while not applied and tentativas < 10:
            tentativas += 1

            a = random.randrange(len(s2))
            if move == 'relocate':
                if len(s2[a]) <= 2: 
                    continue
                i = random.randint(1, len(s2[a])-2)
                b = random.randrange(len(s2))
                j = random.randint(1, len(s2[b])-1)
                if a == b and j in (i, i+1):
                    continue
                apply_relocate(s2, a, i, b, j)
                applied = True

            elif move == 'swap':
                b = random.randrange(len(s2))
                if a == b:
                    continue
                if len(s2[a]) <= 2 or len(s2[b]) <= 2:
                    continue
                i = random.randint(1, len(s2[a])-2)
                j = random.randint(1, len(s2[b])-2)
                apply_swap(s2, a, i, b, j)
                applied = True

            elif move == 'intra_relocate':
                if len(s2[a]) <= 3:
                    continue
                i = random.randint(1, len(s2[a])-2)
                j = random.randint(1, len(s2[a])-2)
                if i == j:
                    continue
                apply_relocate(s2, a, i, a, j)
                applied = True

            elif move == 'intra_swap':
                if len(s2[a]) <= 3:
                    continue
                i = random.randint(1, len(s2[a])-3)
                j = random.randint(i+1, len(s2[a])-2)
                apply_swap(s2, a, i, a, j)
                applied = True

    return s2



def VNS(s, vns_args, k_max=5, max_vehicles=None):

    atual_s = copy.deepcopy(s)
    atual_fo, atual_d = calcula_fo_first_version(atual_s, vns_args, max_vehicles)

    k = 1
    while k <= k_max:
        s_shake = shake(atual_s, k) 

        fo_loc, d_loc, s_loc = RVND(s_shake, vns_args, max_vehicles)


        if fo_loc < atual_fo:
            atual_s = s_loc
            atual_fo = fo_loc
            atual_d  = d_loc
            k = 1 
        else:
            k += 1

    return atual_fo, atual_d, atual_s

