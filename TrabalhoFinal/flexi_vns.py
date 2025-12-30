import random
import time
import copy
from math import inf

# =========================
# Utilities
# =========================
def build_node_index_map(coordinates):
    """coordinates: list of tuples (node_id, x, y)"""
    return {node[0]: idx for idx, node in enumerate(coordinates)}

def clone_routes(routes):
    return [r.copy() for r in routes]

# ensure each route starts/ends at depot and remove consecutive duplicates
def normalize_routes(routes, depot_id=1):
    normalized = []
    for r in routes:
        # keep only real nodes (allow stations/customers)
        middle = [p for p in r if p != depot_id]
        seq = [depot_id] + middle + [depot_id]
        # compress consecutive duplicates
        comp = [seq[0]]
        for x in seq[1:]:
            if x != comp[-1]:
                comp.append(x)
        normalized.append(comp)
    return normalized

# =========================
# Initial constructive (greedy nearest-insertion per vehicle)
# =========================
def construcao_solucao_inicial(demands, capacity, vehicles, depot_id=1, mat_d=None, node_to_idx=None, seed=None):
    """
    Greedy: assign customers to vehicles one by one, inserting at cheapest position that fits capacity.
    Returns list of routes (each start/end depot).
    """
    if seed is not None:
        random.seed(seed)

    dem = {c: d for c, d in demands}
    customers = [c for c, d in demands if c != depot_id]
    unassigned = customers.copy()
    random.shuffle(unassigned)

    routes = [[depot_id, depot_id] for _ in range(vehicles)]
    loads = [0]*vehicles

    # try to greedily place each customer into best vehicle & best insertion position
    for c in unassigned[:]:
        best = None
        best_cost = float('inf')
        for v in range(vehicles):
            if loads[v] + dem[c] > capacity:
                continue
            r = routes[v]
            # try all insertion positions between nodes
            for pos in range(1, len(r)):  # insert before r[pos]
                if mat_d is not None and node_to_idx is not None:
                    a = r[pos-1]; b = r[pos]
                    cost = mat_d[node_to_idx[a]][node_to_idx[c]] + mat_d[node_to_idx[c]][node_to_idx[b]] - mat_d[node_to_idx[a]][node_to_idx[b]]
                else:
                    cost = 0
                if cost < best_cost:
                    best_cost = cost
                    best = (v, pos)
        if best is not None:
            v, pos = best
            routes[v].insert(pos, c)
            loads[v] += dem[c]
            unassigned.remove(c)
    # if some customers left (rare), distribute round-robin (they may create infeasible routes that repair will try fix)
    if unassigned:
        idx = 0
        while unassigned:
            c = unassigned.pop(0)
            routes[idx].insert(-1, c)
            loads[idx] += dem[c]
            idx = (idx + 1) % vehicles

    # normalize
    routes = normalize_routes(routes, depot_id)
    return routes

# =========================
# Evaluation (energy-aware, penalized)
# =========================
INF_FO = 1e18

def evaluate_solution(routes, mat_d, node_to_idx, demands, capacity,
                      energy_capacity, energy_consumption, stations,
                      alpha_dist=1.0, alpha_energy=1000.0, alpha_dv=10000.0, alpha_load=10000.0,
                      depot_id=1):
    """
    Returns (fo_penalized, stats)
    stats: dict with 'feasible' flag, 'total_dist', 'energy_violation' (sum deficits),
           'load_violation' (sum loads over capacity), 'dummy_vehicles' (vh),
           'routes_info' (list per route)
    """
    dem = {c: d for c, d in demands}
    total_dist = 0.0
    energy_violation = 0.0
    load_violation = 0.0
    vh = 0
    routes_info = []
    feasible = True

    # structural check
    for r in routes:
        if len(r) < 2 or r[0] != depot_id or r[-1] != depot_id:
            # invalid structure -> penalize heavily
            return INF_FO, {'feasible': False, 'reason': 'structure'}

    for r in routes:
        carga = sum(dem.get(p, 0) for p in r if p != depot_id)
        if carga > capacity:
            load_violation += (carga - capacity)
            vh += 1
            feasible = False

        energia = energy_capacity
        dist_r = 0.0
        energy_violation_route = 0.0

        for a, b in zip(r[:-1], r[1:]):
            ia = node_to_idx[a]; ib = node_to_idx[b]
            d = mat_d[ia][ib]
            dist_r += d
            consumo = d * energy_consumption
            energia -= consumo
            # if energy negative before arrival -> deficit
            if energia < -1e-9:
                energy_violation_route += abs(energia)
                feasible = False
            # if b is a station, recharge upon arrival
            if b in stations:
                energia = energy_capacity

        total_dist += dist_r
        energy_violation += energy_violation_route
        routes_info.append({'route': r, 'dist': dist_r, 'load': carga, 'energy_violation': energy_violation_route})

    fo = alpha_dist * total_dist + alpha_energy * energy_violation + alpha_dv * vh + alpha_load * load_violation

    stats = {
        'feasible': feasible,
        'total_dist': total_dist,
        'energy_violation': energy_violation,
        'load_violation': load_violation,
        'dummy_vehicles': vh,
        'routes_info': routes_info
    }
    return (fo, stats) if feasible else (fo, stats)

# =========================
# Station repair (greedy insert)
# =========================
def best_station_between(u, v, stations, node_to_idx, mat_d):
    """Return station id minimizing added distance for u->st->v"""
    best_st = None
    best_add = float('inf')
    iu = node_to_idx[u]; iv = node_to_idx[v]
    direct = mat_d[iu][iv]
    for st in stations:
        is_ = node_to_idx[st]
        add = mat_d[iu][is_] + mat_d[is_][iv] - direct
        if add < best_add:
            best_add = add
            best_st = st
    return best_st, best_add

def repair_insert_stations(routes, mat_d, node_to_idx, energy_capacity, energy_consumption, stations, depot_id=1):
    """
    For each route, traverse forward; when next edge can't be traversed with remaining energy,
    insert the best station between the two nodes. Do not backtrack. Returns (new_routes, inserted_flag).
    """
    new_routes = []
    inserted = False
    for r in routes:
        seq = r.copy()
        # ensure start and end depot
        if seq[0] != depot_id:
            seq.insert(0, depot_id)
        if seq[-1] != depot_id:
            seq.append(depot_id)

        i = 0
        # energy from previous recharge (start at depot)
        while i < len(seq)-1:
            # compute energy available at node seq[i] by simulating since last recharge/depot
            # find last recharge index
            last_recharge = i
            for k in range(i, -1, -1):
                if seq[k] in stations or seq[k] == depot_id:
                    last_recharge = k
                    break
            energia = energy_capacity
            for k in range(last_recharge, i):
                ia = node_to_idx[seq[k]]; ib = node_to_idx[seq[k+1]]
                energia -= mat_d[ia][ib] * energy_consumption

            a = seq[i]; b = seq[i+1]
            ia = node_to_idx[a]; ib = node_to_idx[b]
            need = mat_d[ia][ib] * energy_consumption
            if energia >= need - 1e-9:
                i += 1
                continue
            # need station
            st, add = best_station_between(a, b, stations, node_to_idx, mat_d)
            if st is None:
                # can't repair this edge -> skip insertion and move forward (prevents infinite loop)
                i += 1
                continue
            seq.insert(i+1, st)
            inserted = True
            # do not increment i so we will re-evaluate edge a->st next loop
        # compress duplicates
        comp = [seq[0]]
        for x in seq[1:]:
            if x != comp[-1]:
                comp.append(x)
        new_routes.append(comp)
    return new_routes, inserted

# =========================
# Neighborhood operators (they return candidate solution even if infeasible)
# =========================
def op_relocate(routes, args):
    # move single customer from route a pos i to route b pos j
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    R = len(routes)
    for a in range(R):
        for i in range(1, len(routes[a])-1):
            node = routes[a][i]
            for b in range(R):
                for j in range(1, len(routes[b])):
                    if a == b and j in (i, i+1):
                        continue
                    new = clone_routes(routes)
                    new[a].pop(i)
                    new[b].insert(j, node)
                    return normalize_routes(new, depot_id)
    return None

def op_swap(routes, args):
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    R = len(routes)
    for a in range(R):
        for b in range(a+1, R):
            for i in range(1, len(routes[a])-1):
                for j in range(1, len(routes[b])-1):
                    new = clone_routes(routes)
                    new[a][i], new[b][j] = new[b][j], new[a][i]
                    return normalize_routes(new, depot_id)
    return None

def op_relocate2(routes, args):
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    R = len(routes)
    for a in range(R):
        if len(routes[a]) < 4: continue
        for i in range(1, len(routes[a])-2):
            seg = routes[a][i:i+2]
            for b in range(R):
                for j in range(1, len(routes[b])):
                    if a == b and j in (i, i+1, i+2): continue
                    new = clone_routes(routes)
                    new[a].pop(i); new[a].pop(i)
                    new[b][j:j] = seg
                    return normalize_routes(new, depot_id)
    return None

def op_intra_relocate(routes, args):
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    for r in range(len(routes)):
        if len(routes[r]) <= 3: continue
        for i in range(1, len(routes[r])-1):
            for j in range(1, len(routes[r])-1):
                if i == j: continue
                new = clone_routes(routes)
                node = new[r].pop(i)
                new[r].insert(j, node)
                return normalize_routes(new, depot_id)
    return None

def op_intra_swap(routes, args):
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    for r in range(len(routes)):
        if len(routes[r]) <= 3: continue
        for i in range(1, len(routes[r])-2):
            for j in range(i+1, len(routes[r])-1):
                new = clone_routes(routes)
                new[r][i], new[r][j] = new[r][j], new[r][i]
                return normalize_routes(new, depot_id)
    return None

def op_insert_station(routes, args):
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    new, inserted = repair_insert_stations(routes, mat_d, node_to_idx, energy_capacity, energy_consumption, stations, depot_id)
    if inserted:
        return normalize_routes(new, depot_id)
    return None

def op_remove_station(routes, args):
    # try to remove a station occurrence (first-found) - do not attempt combinatorial removals
    mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id = args
    for ri, r in enumerate(routes):
        for i in range(1, len(r)-1):
            if r[i] in stations:
                new = clone_routes(routes)
                new[ri].pop(i)
                return normalize_routes(new, depot_id)
    return None

# operator list
NEIGHBORHOODS = [op_relocate, op_swap, op_relocate2, op_intra_relocate, op_intra_swap, op_insert_station, op_remove_station]

# =========================
# Shaking: apply k random moves (more aggressive than single)
# =========================
def shaking(routes, k, args):
    S = clone_routes(routes)
    ops = NEIGHBORHOODS
    # try up to k*3 random modifications to diversify more
    for _ in range(max(1, k*3)):
        op = random.choice(ops)
        res = op(S, args)
        if res is not None:
            S = res
    return normalize_routes(S, args[-1])

# =========================
# RVND: try neighborhoods until no improvement (first-improvement style)
# returns (new_routes, fo, stats)
# =========================
def rvnd(routes, args, eval_fn):
    # args: (mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id)
    S = clone_routes(routes)
    alphas = args[7]
    fo_S, stats_S = eval_fn(S, *args[0:7], *alphas, depot_id=args[-1])
    improved = True
    while improved:
        improved = False
        order = NEIGHBORHOODS.copy()
        random.shuffle(order)
        for op in order:
            cand = op(S, args)
            if cand is None:
                continue
            fo_cand, stats_cand = eval_fn(cand, *args[0:7], *alphas, depot_id=args[-1])
            # accept if strictly better (penalized FO lower)
            if fo_cand < fo_S - 1e-9:
                S = cand
                fo_S = fo_cand
                stats_S = stats_cand
                improved = True
                break
    return S, fo_S, stats_S

# =========================
# Full VNS (classic)
# =========================
def vns_evrp_classic(instance_data,
                     iterMax=200,
                     maxTime=60.0,
                     Kmax=5,
                     seed=None,
                     require_feasible=True,
                     alpha_dist=1.0,
                     alpha_energy=1000.0,
                     alpha_dv=10000.0,
                     alpha_load=10000.0):
    """
    Main VNS entry for EVRP classic.
    - require_feasible: if True, final best_solution returned will be feasible (only accept feasible replacements).
      If False, algorithm may accept penalized improvements.
    """
    if seed is not None:
        random.seed(seed)

    mat_d = instance_data['mat_d']
    coordinates = instance_data['coordinates']
    node_to_idx = build_node_index_map(coordinates)
    demands = instance_data['demands']
    stations = instance_data['stations']
    vehicles = instance_data['vehicles']
    energy_capacity = instance_data['energy_capacity']
    energy_consumption = instance_data['energy_consumption']
    capacity = instance_data['capacity']
    depot_id = instance_data.get('depot_id', 1)

    alphas = (alpha_dist, alpha_energy, alpha_dv, alpha_load)
    # args pack used by operators and rvnd: (mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id)
    args = (mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alphas, depot_id)

    # initial solution (greedy)
    if 'initial_solution' in instance_data and instance_data['initial_solution'] is not None:
        S0 = normalize_routes(instance_data['initial_solution'], depot_id)
    else:
        S0 = construcao_solucao_inicial(demands, capacity, vehicles, depot_id, mat_d, node_to_idx, seed=seed)
        S0 = normalize_routes(S0, depot_id)

    # attempt repair (insert stations) to make initial feasible if possible
    S_rep, inserted = repair_insert_stations(S0, mat_d, node_to_idx, energy_capacity, energy_consumption, stations, depot_id)
    if inserted:
        S0 = normalize_routes(S_rep, depot_id)

    fo0, stats0 = evaluate_solution(S0, mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alpha_dist, alpha_energy, alpha_dv, alpha_load, depot_id)
    best_penalized = clone_routes(S0)
    best_penalized_fo = fo0
    best_penalized_stats = stats0

    best_feasible = None
    best_feasible_fo = inf
    best_feasible_stats = None
    if stats0.get('feasible', False):
        best_feasible = clone_routes(S0)
        best_feasible_fo = fo0
        best_feasible_stats = stats0

    t0 = time.time()
    iter_count = 0

    while iter_count < iterMax and (time.time() - t0) < maxTime:
        k = 1
        while k <= Kmax and (time.time() - t0) < maxTime:
            # shaking
            S_prime = shaking(best_penalized, k, args)
            # repair stations before local search
            S_prime_rep, ins = repair_insert_stations(S_prime, mat_d, node_to_idx, energy_capacity, energy_consumption, stations, depot_id)
            if ins:
                S_prime = normalize_routes(S_prime_rep, depot_id)

            # local search (RVND)
            S_local, fo_local, stats_local = rvnd(S_prime, args, lambda *a, **kw: evaluate_solution(*a, **kw))

            # ensure stats_local is obtained
            fo_local, stats_local = evaluate_solution(S_local, mat_d, node_to_idx, demands, capacity, energy_capacity, energy_consumption, stations, alpha_dist, alpha_energy, alpha_dv, alpha_load, depot_id)

            # acceptance criteria
            accept = False
            # prefer feasible solutions
            if stats_local.get('feasible', False):
                # if we previously had no feasible best_feasible, accept any feasible
                if best_feasible is None:
                    accept = True
                else:
                    # compare by penalized FO but only accept if improving best_feasible_fo
                    if fo_local < best_feasible_fo - 1e-9:
                        accept = True
            else:
                # not feasible
                if not require_feasible:
                    # allow penalized acceptance (improving penalized FO)
                    if fo_local < best_penalized_fo - 1e-9:
                        accept = True

            # always update best_penalized if improved (helps exploration)
            if fo_local < best_penalized_fo - 1e-9:
                best_penalized = clone_routes(S_local)
                best_penalized_fo = fo_local
                best_penalized_stats = stats_local

            if accept:
                # if feasible and better than best_feasible, update best_feasible
                if stats_local.get('feasible', False):
                    if best_feasible is None or fo_local < best_feasible_fo - 1e-9:
                        best_feasible = clone_routes(S_local)
                        best_feasible_fo = fo_local
                        best_feasible_stats = stats_local
                    # when accept because feasible, also move current search point
                    best_penalized = clone_routes(S_local)
                    best_penalized_fo = fo_local
                    best_penalized_stats = stats_local
                else:
                    # accepted an infeasible (only possible if require_feasible False)
                    best_penalized = clone_routes(S_local)
                    best_penalized_fo = fo_local
                    best_penalized_stats = stats_local
                k = 1
            else:
                k += 1

        iter_count += 1

    elapsed = time.time() - t0

    result = {
        'initial_solution': S0,
        'initial_fo': fo0,
        'initial_stats': stats0,
        'best_penalized_solution': best_penalized,
        'best_penalized_fo': best_penalized_fo,
        'best_penalized_stats': best_penalized_stats,
        'best_feasible_solution': best_feasible,
        'best_feasible_fo': best_feasible_fo if best_feasible is not None else None,
        'best_feasible_stats': best_feasible_stats,
        'time': elapsed,
        'iterations': iter_count
    }
    return result
