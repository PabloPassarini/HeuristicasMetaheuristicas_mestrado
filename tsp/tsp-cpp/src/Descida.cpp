#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <algorithm>
#include <random>
#include <utility> //funcao swap (para versao anterior a C11 usar <algorithm>)
#include "Arquivos.h"
#include "Construcao.h"
#include "Descida.h"
#include "Util.h"

using namespace std;

float calcula_delta(int n, vector<int> &s, float **d, int i, int j)
{
  int i_antes, i_depois, j_antes, j_depois;

  i_antes = i - 1;
  i_depois = i + 1;
  j_antes = j - 1;
  j_depois = j + 1;
  if (i == 0) i_antes = n-1;
  if (i == n-1) i_depois = 0;
  if (j == 0) j_antes = n-1;
  if (j == n-1) j_depois = 0;

  float delta = d[s[i_antes]][s[i]] + d[s[i]][s[i_depois]] + 
                d[s[j_antes]][s[j]] + d[s[j]][s[j_depois]];
  return  delta;


}

// Encontra o melhor vizinho utilizando o movimento de troca de posicao de duas cidades
float melhor_vizinho(int n, vector<int> &s, float **d, float fo, int *melhor_i, int *melhor_j)
{
  float fo_melhor_viz = fo;

  float fo_viz;
  for(int i=0 ; i < n - 1 ; i++){
    for(int j=i+1 ; j < n ; j++) {
      // Calcula a variacao de custo com a realizacao do movimento
      float delta1 = calcula_delta(n,s,d,i,j);

      // Faz o movimento
      swap(s[i], s[j]);

      float delta2 = calcula_delta(n,s,d,i,j);

      // Calcular a nova distancia
      fo_viz = fo - delta1 + delta2;

      // Armazenar o melhor movimento (melhor troca)
      if(fo_viz < fo_melhor_viz){
        *melhor_i = i;
        *melhor_j = j;
        fo_melhor_viz = fo_viz;
      }

      // desfaz o movimento
      swap(s[i],s[j]);
    }
  }
  // retornar a distancia do melhor vizinho
  return fo_melhor_viz;

}//melhor_vizinho

//Vizinho aleatorio usado nas descidas e algumas meta-heurisiticas
float vizinho_aleatorio(int n, vector<int> &s, float **d, float fo, int *melhor_i, int *melhor_j)
{
    float fo_viz = fo;
    int i, j;
    float delta1, delta2;


    // retornar a distancia do  vizinho
    return fo_viz;

}//vizinho_aleatorio 

/* Método da descida com estrategia best improvement */
float descida_best_improvement(int n, vector<int> &s, float **d)
{
  int melhor_i, melhor_j, iter;
  float fo_viz, fo;
  bool melhorou;
  clock_t inicio_CPU, fim_CPU;

  fo = fo_viz = calcula_fo(n, s, d);
  limpa_arquivo((char*)"DescidaBI.txt");
  inicio_CPU = fim_CPU = clock();
  iter = 0;
  imprime_fo((char*)"DescidaBI.txt", (fim_CPU - inicio_CPU)/CLOCKS_PER_SEC,fo,iter);

    /*  Implementar a descida com estrategia best improvement */



  fim_CPU = clock();
  imprime_fo((char*)"DescidaBI.txt", (fim_CPU - inicio_CPU)/CLOCKS_PER_SEC,fo,iter);
  return fo;
}//descida_best_improvement

float descida_randomica(int n, vector<int> &s, float **d, int IterMax)
{
  int iter;
  float fo, fo_viz;

  int melhor_i, melhor_j;
  clock_t inicio_CPU, fim_CPU;

  fo = calcula_fo(n,s,d);
  iter = 0;
  limpa_arquivo((char*)"DescidaRandomica.txt");
  inicio_CPU = fim_CPU = clock();

  while (iter < IterMax){
    iter ++;

  /*  Implementar a descida randômica  */


  }

  /* Implementar a impressão final (veja descida completa)*/

  return fo;
}



float vizinho_first_improvement(int n, vector<int> &s, float **d, float fo, int *melhor_i, int *melhor_j)
{
 float fo_melhor_viz = fo;
 bool melhorou = false;
 vector<int> vet;

 for (int i=0; i < n; i++) vet.push_back(i);
 //Para c++ 11
 unsigned seed = chrono::system_clock::now().time_since_epoch().count();
 default_random_engine r(seed);
 shuffle ( vet.begin(), vet.end(), r );
 //Para c++ 98
 //random_shuffle ( vet.begin(), vet.end() );

 
 // retornar a distancia do melhor vizinho
 return fo_melhor_viz;

}//melhor_vizinho


float descida_first_improvement(int n, vector<int> &s, float **d)
{
 int aux, melhor_i, melhor_j, iter;
 float fo_viz, fo;
 bool melhorou;
 clock_t inicio_CPU, fim_CPU;

 fo = fo_viz = calcula_fo(n, s, d);
 limpa_arquivo((char*)"DescidaFI.txt");
 inicio_CPU = fim_CPU = clock();
 iter = 0;
 imprime_fo((char*)"DescidaFI.txt", (fim_CPU - inicio_CPU)/CLOCKS_PER_SEC,fo,iter);

  /* Implementar a descida First Improvement armazenando, a cada iteração:
      o tempo de execução
      o valor da função de avaliação da solução corrente
      a iteração na qual a solução vizinha foi aceita
      Para fazer essa impressão, use o procedimento imprime_fo e imprime_fo_viz, 
      disponíveis em Arquivos.cpp */
 

  fim_CPU = clock();
  imprime_fo((char*)"DescidaFI.txt", (fim_CPU - inicio_CPU)/CLOCKS_PER_SEC,fo,iter);
  return fo;
}
