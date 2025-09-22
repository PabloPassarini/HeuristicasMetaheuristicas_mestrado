#ifndef _DESCIDA_H_
#define _DESCIDA_H_

#include <vector>
using namespace std;

float calcula_delta(int n, vector<int> &s, float **d, int i, int j);

/* Método da descida com estrategia best improvement */
float descida_best_improvement(int n, vector<int> &s, float **d);
float melhor_vizinho(int n, vector<int> &s, float **d, float fo, 
	                 int *melhor_i, int *melhor_j);

/* Método da descida com estrategia first improvement */
float descida_first_improvement(int n, vector<int> &s, float **d);
float vizinho_first_improvement(int n, vector<int> &s, float **d, 
	                           float fo, int *melhor_i, int *melhor_j);

/* Método da descida com estrategia aleatoria */
float descida_randomica(int n, vector<int> &s, float **d,
                        int IterMax);
float vizinho_aleatorio(int n, vector<int> &s, float **d,
                        float fo, int *melhor_i, int *melhor_j);

//float melhor_vizinho_adjacente(int n, vector<int> *s, float **d, float fo, int *melhor_i, int *melhor_j);

#endif