
def get_val(string):
    parts = string.split(':')
    value = parts[1].strip()
    return value

def read_data(local):
    with open(local, 'r') as file:
        data = file.readlines()


    optimal_value = None
    energy_consumption = None
    energy_capacity = None
    capacity = None
    demands = []
    coordinates = []
    stations = []

    flag = 0
    for line in data:
        aux = line.replace('\n','')
        if flag == 0:
            if 'OPTIMAL_VALUE' in aux:
                optimal_value = get_val(aux)
            elif 'ENERGY_CONSUMPTION' in aux:
                energy_consumption = float(get_val(aux))
            elif 'ENERGY_CAPACITY' in aux:
                energy_capacity = float(get_val(aux))
            elif 'CAPACITY' in aux:
                capacity = int(get_val(aux))
            elif 'VEHICLES' in aux:
                vehicles = int(get_val(aux))
 
        if 'NODE_COORD_SECTION' == aux.strip():
            flag = 1
            continue
        if 'DEMAND_SECTION' == aux.strip():
            flag = 2
            continue
        if 'STATIONS_COORD_SECTION' == aux.strip():
            flag = 3  
            continue 
        if 'EOF' == aux.strip() or aux.strip() == 'DEPOT_SECTION':
            break

        if flag == 1:
            
            parts = aux.split(' ')
            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            coordinates.append((node_id, x, y))
        elif flag == 2:
            parts = aux.split(' ')
            node_id = int(parts[0])
            demand = int(parts[1])
            demands.append((node_id, demand))
        elif flag == 3:
            
            parts = aux.split(' ')
            node_id = int(parts[0])
            stations.append(node_id)
    mat_d = matriz_distancias(coordinates)
    return optimal_value, energy_consumption, energy_capacity, capacity, demands, coordinates, stations, vehicles, mat_d

def matriz_distancias(coordinates):
    n = len(coordinates)
    dist_matrix = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i != j:
                x1, y1 = coordinates[i][1], coordinates[i][2]
                x2, y2 = coordinates[j][1], coordinates[j][2]
                dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                dist_matrix[i][j] = dist

    return dist_matrix


def calcula_distance(d, p1, p2):
    return d[p1][p2]

def calcula_fo_first_version(s, vns_args, max_available_vehicles):
    
    # calculo da distancia total
    distance = 0.0
    for route in s:
        for i in range(1, len(route)):
            p1 = route[i]
            p2 = route[i - 1]

            distance += calcula_distance(vns_args['mat_d'], p1-1, p2-1)    


    # calculo da penalizacao por violacao de capacidade energetica
    energia_rota = calcula_gast_ener(s, vns_args)
    total_energy_violation = 0.0
    for rota in energia_rota:
        total_energy_violation += rota[2]
    
    
    # Calculo por veiculo extra
    total_vehicle_violation = max(0, vns_args['vehicles'] - max_available_vehicles)

    
    demanda_rota = calcula_demanda(s, vns_args)
    total_demand_violation = 0.0
    for rota in demanda_rota:
        total_demand_violation += rota[1]
    
    return distance*vns_args['alpha0'] + total_energy_violation*vns_args['alpha1'] + total_vehicle_violation*vns_args['alpha2'] + total_demand_violation*vns_args['alpha3'], distance 


def calcula_demanda(s, vns_args):
    demands_dict = {c: d for c, d in vns_args['demands']}
    capacidade = vns_args['capacity']
    total = list()
    for rota in s:
        de = 0
        violacao = 0
        for p in rota:
            if not(p in vns_args['stations']):
                de += demands_dict[p]
       
        if de > capacidade:
            violacao = de - capacidade
        total.append((de, violacao))
    
    return total

def calcula_gast_ener(s, vns_args):
    station = vns_args['stations']
    mat_d = vns_args['mat_d']
    total = list()
    for rota in s:
        recarga = 0
        energia_total = 0
        violacao = 0
        energia_rota = 0
        for p in range(1, len(rota)):
            a = rota[p-1]
            b = rota[p]
            energia_total += mat_d[a-1][b-1]*vns_args['energy_consumption']
            energia_rota += mat_d[a-1][b-1]*vns_args['energy_consumption']
            if energia_rota > vns_args['energy_capacity']:
                violacao += abs(vns_args['energy_capacity'] - energia_rota)

            if rota[p] in station:
                recarga += 1
                energia_rota = 0
        total.append((recarga, energia_total, violacao))
    return total
