//
// Created by Puca Penna on 13/09/2018.
//
#include <cmath>
#include <iostream>
#include <ctime>
#include "SA.h"
#include "Util.h"
#include "Descida.h"
#include "Arquivos.h"

using namespace std;

float SA(int n, std::vector<int> &s, float **d, float alpha, 
         float SAmax, double temp_inicial, double temp_final)
{
    float fo, fo_viz, fo_star;
    int melhor_i, melhor_j, aux;
    float delta, x;
    int iterT = 0;

    clock_t inicio_CPU, fim_CPU;

    limpa_arquivo((char*)"SA.txt");
    inicio_CPU = fim_CPU = clock();

    double temp = temp_inicial;

    vector<int> s_star;
    s_star = s;
    fo = fo_star = fo_viz = calcula_fo(n, s, d);

/* implementar o loop do SA */
  
    s = s_star;

    fim_CPU = clock();
    imprime_fo((char*)"SA.txt", (fim_CPU - inicio_CPU)/CLOCKS_PER_SEC,fo,iterT);

    return fo_star;
}

float temperaturaInicial(int n, std::vector<int> &s, float **d, 
                         float beta, float gama, float SAmax, 
                         double temp_inicial)
{
    double temp = temp_inicial;
    int melhor_i, melhor_j;
    bool continua = true;
    float fo_viz, fo, fo_star;
    int aceitos;
    double delta;
    double x;

    fo = fo_star = fo_viz = calcula_fo(n, s, d);

    while(continua){
        aceitos = 0;
        for (int iterT = 1; iterT <= SAmax; iterT++){
            fo_viz = vizinho_aleatorio(n, s, d, fo, &melhor_i, &melhor_j);
            delta = fo_viz - fo;
            if (delta < 0)
                aceitos++;
            else{
                x = randomico(0,1);
                if ( x < exp(-delta/temp))
                    aceitos++;
            }
        }

        if(aceitos >= gama * SAmax)
            continua = false;
        else
            temp = beta * temp;

    }

    return temp;
}
