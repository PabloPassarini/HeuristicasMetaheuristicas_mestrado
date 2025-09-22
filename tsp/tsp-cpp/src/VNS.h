//
// Created by Puca Penna on 10/10/19.
//
#ifndef _PCV_C_VNS_H_
#define _PCV_C_VNS_H_

#include <vector>
using namespace std;

float VNS(int n, vector<int> &s, 
          float **d, 
          int VNS_max, // numero maximo de iteracoes
          int r); // numero total de vizinhancas

// gera um vizinho qualquer usando a vizinhanca k
float gera_um_vizinho_qualquer( int n,
                                vector<int> &s,
                                float **d,
                                float fo,
                                int k);

// Gera um vizinho qualquer usando o movimento de troca
float vizinho_troca_qualquer(int n,
                             vector<int> *s, 
                             float **d, 
                             float fo);

// Gera um vizinho qualquer usando o movimento de re-inserir 
// um cliente em outra posicao da rota
float vizinho_reinsercao1_qualquer(int n,
                             vector<int> *s, 
                             float **d, 
                             float fo);

// Gera um vizinho qualquer usando o movimento de re-inserir 
// dois clientes consecutivos em outra posicao da rota
float vizinho_reinsercao2_qualquer(int n,
                             vector<int> *s, 
                             float **d, 
                             float fo);

 #endif