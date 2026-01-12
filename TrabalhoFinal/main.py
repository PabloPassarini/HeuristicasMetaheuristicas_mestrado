from util import read_data, calcula_fo_first_version, calcula_demanda, calcula_gast_ener
import matplotlib.pyplot as plt
from vns import RVND, construcao_solInicial, VNS
import time, os
from pathlib import Path

def gerar_grafico(coord, stations, titulo, pasta, solucao=False):
    x_clientes, y_clientes = [], []
    x_st, y_st = [], []
    x_dep, y_dep = [], [] 

    titulo = titulo.split('.')[0]

    for pid, x, y in coord:

        if pid == 1:  
            x_dep.append(x)
            y_dep.append(y)

        elif pid in stations:
            x_st.append(x)
            y_st.append(y)

        else:
            x_clientes.append(x)
            y_clientes.append(y)

    plt.figure(figsize=(10,8))
    plt.scatter(x_clientes, y_clientes, color='blue', marker='o', label='Clientes')
    plt.scatter(x_st, y_st, color='green', marker='s', label='Estações')
    plt.scatter(x_dep, y_dep, color='red', marker='D', s=120, label='Depósito')

    if solucao:
        cont = 1
        for rota in solucao:
            xs, ys = [], []
            for pid in rota:
                for (p_id, px, py) in coord:
                    if p_id == pid:
                        xs.append(px)
                        ys.append(py)
                        break
            
            plt.plot(xs, ys, linewidth=2, alpha=0.7)#, label=f'Rota {cont}')
            cont += 1

    plt.title(f"Rota - {titulo}" if solucao else "Mapa da Instância")
    plt.legend()
    plt.grid(True)
    #plt.show()

    plt.savefig(
        os.path.join(pasta, f"Instance_{titulo}.png"),
        dpi=300,
        bbox_inches="tight"
    )



instancias = [

    'E-n29-k4-s7.evrp',
    'E-n30-k3-s7.evrp',
    'E-n35-k3-s5.evrp',
    'E-n37-k4-s4.evrp',
    'E-n60-k5-s9.evrp',
    'F-n49-k4-s4.evrp',
    

    'E-n89-k7-s13.evrp',
    'E-n112-k8-s11.evrp',
    'M-n110-k10-s9.evrp',
    'M-n126-k7-s5.evrp',
    'M-n163-k12-s12.evrp',
    'M-n212-k16-s12.evrp',
    'F-n80-k4-s8.evrp',
    'F-n140-k7-s5.evrp',
    'X-n147-k7-s4.evrp',
    'X-n221-k11-s9.evrp',
    'X-n360-k40-s9.evrp',
    'X-n469-k26-s10.evrp',
    'X-n577-k30-s4.evrp',
    'X-n698-k75-s13.evrp',
    'X-n759-k98-s10.evrp',
    'X-n830-k171-s11.evrp',
    'X-n920-k207-s4.evrp',
    'X-n1006-k43-s5.evrp'
]


instancias_p = [

    'E-n29-k4-s7.evrp',
    'E-n30-k3-s7.evrp',
    'E-n35-k3-s5.evrp',
    'E-n37-k4-s4.evrp', 
    'E-n60-k5-s9.evrp',
    'F-n49-k4-s4.evrp',
]
instancias_g = [
    'E-n89-k7-s13.evrp',
    'E-n112-k8-s11.evrp',
    'M-n110-k10-s9.evrp',
    'M-n126-k7-s5.evrp',
    'M-n163-k12-s12.evrp'
]

base_dir = Path(__file__).resolve().parent.parent
arquivo_Res = base_dir / 'TrabalhoFinal' / 'Resultados' / 'resultados2.csv'
caminho = base_dir / 'TrabalhoFinal' / 'e-cvrp_benchmark_instances-master' / 'E-n29-k4-s7.evrp'
opt, energy_consumption, energy_capacity, capacity, demands, coordinates, stations, vehicles, mat_d = read_data(caminho)

#gerar_grafico(coordinates, stations, 'teste', caminho)
arq = open(arquivo_Res, 'w')
arq.write('instancia;capacidade_carga;capacidade_energia;t_avg;fo(best);media_d;distancia(best);caminho(best);demanda_rotas(melhor);violacao_demanda(melhor);N_recargas(melhor);energia_gasta_rotas(melhor);N_violacao_energia(melhor)\n')
arq.close()
graficos = base_dir / 'TrabalhoFinal' / 'Resultados' 


av = 10

for instancia in instancias:
    try:
        caminho = base_dir / 'TrabalhoFinal' / 'e-cvrp_benchmark_instances-master' / instancia
        opt, energy_consumption, energy_capacity, capacity, demands, coordinates, stations, vehicles, mat_d = read_data(caminho)

        inst = {
            'mat_d': mat_d,
            'coordinates': coordinates,
            'demands': demands,
            'stations': stations,
            'vehicles': vehicles,
            'energy_capacity': energy_capacity,
            'energy_consumption': energy_consumption,
            'capacity': capacity,
            'depot_id': 1
        }

        inst['alpha0'] = 40 #distancia
        inst["alpha1"] = 30 #energia
        inst["alpha2"] = 15 #numero de veiculos
        inst["alpha3"] = 40 #demanda
        inst['max_time'] = 120
        inst['start_time'] = time.time()



        best = float('inf')
        mean_i = 0
        worst = -float('inf')

        best_fo = float('inf')
        best_dist = float('inf')
        best_s = []
        best_demanda = None
        best_energia = None

        total_time = 0
        for vezes in range(av):
            start = time.perf_counter()
            s_init = construcao_solInicial(inst)
            #gerar_grafico(coordinates, stations, "Inicial", solucao=routes)

            fo_init, d_init = calcula_fo_first_version(
                s=s_init,
                vns_args=inst,
                max_available_vehicles=inst["vehicles"]
            )
            demanda_init = calcula_demanda(s_init, inst)
            energia_init =  calcula_gast_ener(s_init, inst)

            fo_rvnd, d_rvnd, s_vnd = RVND(s_init, inst, vehicles)

            # Refinamento global forte
            fo_end, d_end, s_end = VNS(s_vnd, inst, k_max=5, max_vehicles=vehicles)

            demanda_end = calcula_demanda(s_end, inst)
            energia_end =  calcula_gast_ener(s_end, inst)

            if fo_end < best_fo:
                best_fo = fo_end
                best_dist = d_end
                best_s = s_end
                best_demanda = demanda_end
                best_energia = energia_end

            mean_i += d_end
            end = time.perf_counter()
            total_time += (end - start)
        
        arq = open(arquivo_Res, 'a')

        demanda_por_Drone = list()
        demandas_viola = list()
        for d in best_demanda:
            demanda_por_Drone.append(d[0])
            demandas_viola.append(d[1])


        n_recargas = list()
        energia_total = list()
        n_violacao = list()

        for e in best_energia:
            n_recargas.append(e[0])
            energia_total.append(e[1])
            n_violacao.append(e[2])

        arq.write(f'{str(instancia)};{str(capacity)};{str(energy_capacity)};{str(round(total_time/av, 1))};{str(best_fo)};{str(mean_i/av)};{str(best_dist)};{str(best_s)};{str(demanda_por_Drone)};{str(demandas_viola)};{str(n_recargas)};{str(energia_total)};{str(n_violacao)}\n')
        arq.close()


        gerar_grafico(coordinates, stations, instancia, graficos, solucao=best_s)

    except:
        pass

