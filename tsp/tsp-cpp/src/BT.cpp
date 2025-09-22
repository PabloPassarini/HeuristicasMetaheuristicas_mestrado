//
// Created by Puca Penna on 10/10/19.
//

#include <cmath>
#include <iostream>
#include <ctime>
#include <climits>
#include "Util.h"
#include "Descida.h"
#include "Arquivos.h"
#include "BT.h"

bool eh_tabu(int posicao1, int posicao2, int iterAtual, int **listaTabu)
{
    return iterAtual <= listaTabu[posicao1][posicao2];
}

float melhor_vizinho_BT(int n,
                        vector<int> &s,
                        float **d,
                        float fo,
                        int *melhor_i,
                        int *melhor_j,
                        float fo_star,
                        int iterAtual,
                        int **listaTabu)
{
    int aux;
    float fo_melhor_viz = INT_MAX; //Pode aceitar solução de piora

    float fo_viz;
    for(int i=0 ; i < n - 1 ; i++){
        for(int j=i+1 ; j < n ; j++) {
            // Calcula a variacao de custo com a realizacao do movimento
            float delta1 = calcula_delta(n,s,d,i,j);

            // Faz o movimento
            swap(s[i],s[j]);

            float delta2 = calcula_delta(n,s,d,i,j);

            // Calcular a nova distancia
            fo_viz = fo - delta1 + delta2;

            bool tabu = eh_tabu(i,j,iterAtual,listaTabu);

            /* Implementar a condição para armazenar o melhor movimento
             (melhor troca) que nao seja tab ou, se tabu, que melhore 
             a função objetivo estrela */



            // desfaz o movimento
            swap(s[i],s[j]);
        }
    }
    // retornar a distancia do melhor vizinho
    return fo_melhor_viz;
}

float BT(int n, vector<int> &s, float **d, int tamanho_maximo_lista, int BTmax)
{

    int melhor_i, melhor_j;
    int iterBT = 0;  // numero corrente de iteracoes da Busca Tabu
    int MelhorIter = 0; // Iteracao em que ocorreu a melhor solucao
    vector<int> s_star;
    float fo, fo_star;

    // cria e inicializa a lista tabu. Implementada como uma matriz de duração
    int **listaTabu;
    listaTabu = cria_matriz(n, n);
    for(int i = 0; i < n;i++)
        for(int j = 0; j < n; j++)
            listaTabu[i][j] = iterBT;

    clock_t inicio_CPU, fim_CPU;

    s_star = s;
    fo_star = fo = calcula_fo(n,s,d);

    printf("\nIniciando a Busca Tabu com fo = %8.2f\n", fo);

    inicio_CPU = fim_CPU = clock();
    limpa_arquivo((char*)"BT.txt");     // Todas as soluções
    limpa_arquivo((char*)"BT_Melhorfo.txt");  // Somente as soluções de melhora
    imprime_fo((char*)"BT.txt", (float)(fim_CPU - inicio_CPU)/CLOCKS_PER_SEC, fo, iterBT);
    imprime_fo((char*)"BT_Melhorfo.txt", (float)(fim_CPU - inicio_CPU)/CLOCKS_PER_SEC, fo_star, iterBT);

    /*
     *
     * Implementar o laço da BT
     *
     */


    fim_CPU = clock();
    imprime_fo((char*)"BT.txt", (float)(fim_CPU - inicio_CPU)/CLOCKS_PER_SEC, fo, iterBT);
    imprime_fo((char*)"BT_Melhorfo.txt", (float)(fim_CPU - inicio_CPU)/CLOCKS_PER_SEC, fo_star, iterBT);

    s = s_star;
    fo = fo_star;

    libera_matriz(listaTabu, n);

    return fo;

}