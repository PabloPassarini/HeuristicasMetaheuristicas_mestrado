#ifndef _AG_H_
#define _AG_H_

#include <vector>

float AG(int n,
        std::vector<int> &s,
        float **d,
        int nind,              //numero de individuos
        float max_desvio,       //desvio maximo
        double prob_crossover,  // probabilidade de crossover
        double prob_mutacao,    // probabilidade de mutacao
        int tipo_operador);     // tipo de operador utilizado

/* Esta rotina devolve o individuo escolhido pelo mecanismo da roleta russa */
int roleta(int nind, std::vector<float> &fo_pop);


/* Esta rotina devolve o individuo escolhido pelo mecanismo da roleta russa */
/* Não implementado */
int roleta_scaling(int nind, std::vector<float> &fo_pop);

/* Faz a mutacao no individuo, no caso, troca duas cidades de posicao */
void mutacao(std::vector<int> &s, int n);


/* Operador Crossover OX */
void crossover_OX(std::vector<int> &pai1,
                  std::vector<int> &pai2,
                  std::vector<int> &filho1,
                  std::vector<int> &filho2,
                  int n);

/* Operador Crossover ERX */
/* Não implementado */
void crossover_ERX(std::vector<int> &pai1,
                   std::vector<int> &pai2,
                   std::vector<int> &filho1,
                   std::vector<int> &filho2,
                   int n);


#endif


