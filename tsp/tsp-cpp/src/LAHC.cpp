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


float LAHC(int n, vector<int> &s, float **d,
           int l, int m) 
{
  int i, j, r, iter, p, aux;
  float delta1, delta2, fo, fo_viz;

  int melhor_i, melhor_j;
  clock_t inicio_CPU, fim_CPU;

  fo = calcula_fo(n,s,d);

  vector<float> F;
  for(int i = 0; i < l; i++)
    F.push_back(fo);
  vector<int> s_star(s);
  float fo_star = fo;

  limpa_arquivo((char*)"lahc.txt");
  inicio_CPU = fim_CPU = clock();

// Implementar

  s = s_star;

  return fo_star;
}


