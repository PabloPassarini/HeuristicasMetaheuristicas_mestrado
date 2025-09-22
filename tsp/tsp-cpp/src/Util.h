#ifndef _UTIL_H_
#define _UTIL_H_

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

#define MAX(x,y) ((x)<(y) ? (y) : (x))

/* cria memoria para um vetor de tam posicoes */
int *cria_vetor(int tam);

/* cria memoria para um vetor de tam posicoes */
float *cria_vetor_float(int tam);

/* Cria matriz de ponteiros para inteiros com nlinhas e ncolunas */
int **cria_matriz(int nlinhas, int ncolunas);

/* Cria matriz de ponteiros para inteiros com nlinhas e ncolunas */
float **cria_matriz_float(int nlinhas, int ncolunas);

/* libera memoria de um vetor */
void libera_vetor(int *vetor);
void libera_vetor(vector<int> *vetor);

void libera_matriz(int **matriz, int nlinhas);

void libera_matriz_float(float **matriz, int nlinhas);

/* imprime a solucao */
void imprime_vetor(int &s, int n);

/* imprime a solucao */
void imprime_rota(vector<int> &s, int n);

/* calcula a funcao objetivo */
float calcula_fo(int n, vector<int> &s, float **distancia);

/* Gera numero aleatorio entre min e max */
float randomico(float min, float max);

/* atualiza a melhor solucao */
void atualiza_vetor(int *s_star, int *s, int n);

void inicializa_vetor(vector<int> *vetor, int tam);

void inicializa_vetor_float(vector<float> *vetor, int tam);

void embaralha_vetor(int *vetor, int n);
void embaralha_vetor(vector<int> *vetor, int n);

void insere_meio_vetor(int *vetor, int valor, int pos, int qde);

/* Procura a posição da cidade dada no vetor */
int busca_pos_valor(int *vetor, int cidade, int n);

/* Retorna se uma cidade já foi inserido no vetor */
int foi_inserida(int *vetor, int cidade, int n);

/* Calcula o desvio-padrão das fos da população */
float calcula_desvio_padrao(vector<float> &fo_pop, int n);

/* Atualiza a matriz de arestas */
void atualiza_arestas(int **arestas, int n, int m, int prox_cid);

/* Para ordenação crescente, verifica se a distância entre (i,j) é menor que (i, i+1)*/
//inline bool ordena_dist_crescente (float i, float j, vector<int> *s, float **d)
//{
//    return ( d[s->at(i)][s->at(j)] < d[s->at(i)][s->at(i+1)] );
//}


struct ordena_dist_crescente {
    float **d;      //matriz de distancia
    int index;      //ultima cidade da solucao
    bool operator() (int i,int j) {
        return ( d[index][i] < d[index][j]);
    }
} ;

#endif