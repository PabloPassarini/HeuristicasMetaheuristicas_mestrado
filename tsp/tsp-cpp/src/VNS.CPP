#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include "Construcao.h"
#include "Util.h"
#include "Descida.h"
#include "VNS.h"

float VNS(int n, vector<int> &s, float **d, int VNS_max, int r){

   // cria variaveis auxiliares - implementar

   fo = calcula_fo(n,s,d);
   printf("Iter VNS = %3d \t  fo_star = %10.4f \n",iter,fo);
  
   // loop principal do VNS
   while (iter - MelhorIter < VNS_max){
     iter++;
     k = 1; // comeca pela vizinhanca 1

     // loop das vizinhancas
     while (k <= r){
       // Escolher vizinho s' qualquer na k-esima vizinhanca de s
       // Realizar a busca local no vizinho gerado
       // Verificar se melhorou a solucao s''
          // se sim, atualiza s e reinicia o contador de vizinhancas
          // caso contrario, incrementa o contador de vizinhancas
      
   }
   return fo;
}

float gera_um_vizinho_qualquer(int n,
                                 int *s,
                                 float **d,
                                 float fo,
                                 int k)
{
  float fo_viz;
  
  switch(k){
    case 1:
      // executaca vizinhanca 1
    break;
    case 2:
      // executaca vizinhanca 2
    break;
    case 3:
      // executaca vizinhanca 3
    break;
  }

  return fo_viz;

}// fim gera_k_vizinhos_aleatorios

// Gera um vizinho qualquer usando o movimento de troca
float vizinho_troca_qualquer(int n, vector<int> &s, float **d, float fo)
{//Metodo vizinho_aleatorio usado nas descidas, aqui alterado para retornar o vizinho gerado

    float fo_viz = fo;
    int i, j, aux;
    float delta1, delta2;

    //sorteia a posição para troca
    j = rand() % n;
    do{
        i = rand() % n;
    }while (i == j);

    delta1 = calcula_delta(n,s,d,i,j);

    // Faz o movimento
    swap(s[i], s[j]);

    delta2 = calcula_delta(n,s,d,i,j);

    // calcula o no fo
    fo_viz = fo - delta1 + delta2;

    // retornar a distancia do  vizinho, a solucao s eh retornada por referencia
    return fo_viz;

}//vizinho_troca_qualquer


// Gera um vizinho qualquer usando o movimento de re-inserir 
// um cliente em outra posicao da rota
float vizinho_reinsercao1_qualquer(int n,
                             vector<int> *s, 
                             float **d, 
                             float fo){
  double fo_viz;

  //implementar


  return fo_viz;
}

// Gera um vizinho qualquer usando o movimento de re-inserir 
// dois clientes consecutivos em outra posicao da rota
float vizinho_reinsercao2_qualquer(int n,
                             vector<int> *s, 
                             float **d, 
                             float fo){
  double fo_viz;

  //implementar

  
  return fo_viz;
}

