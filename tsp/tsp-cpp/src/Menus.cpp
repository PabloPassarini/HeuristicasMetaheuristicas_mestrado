#include <cstdio>
#include <iostream>
#include "Menus.h"

using namespace std;

/* Menu principal */
int menu_principal(void)
{
  int escolha;

  do {
    cout << "\n*******************Menu Principal************************* \n"
        << "ATENCAO: Necessario gerar solucao inicial antes de refinar\n"
        << "                1. Gere solucao inicial \n"
        << "                2. Descida com Best Improvement\n"
        << "                3. Descida randomica \n"
        << "                4. Descida com Primeiro de Melhora (First Improvement) \n"
        << "                5. Multi-Start \n"
        << "                6. Simulated Annealing \n"
        << "                7. Busca Tabu \n"
        << "                8. ILS \n"
        << "                9. GRASP \n"
        << "               10. VND \n"
        << "               11. VNS \n"
        << "               12. Algoritmos Geneticos \n"
        << "               13. LAHC \n"        
        << "               14. Algoritmos Memeticos \n"
        << "               15. Colonia de Formigas \n"
        << "                0. Sair \n"
        << "                Escolha: ";
    cin >> escolha;
  } while (escolha < 0 || escolha > 14);
  return escolha;
}



/* Menu de geracao de uma solucao inicial */
int menu_solucao_inicial(void)
{
  int escolha;

  do {
    cout << "\n************Geracao da Solucao Inicial**************** \n" <<
     "                1. Gulosa (Vizinho mais proximo) \n" <<
     "                2. Parcialmente gulosa (Vizinho mais proximo) \n" <<
     "                3. Gulosa (Insercao Mais Barata) \n" <<
     "                4. Parcialmente gulosa (Insercao Mais Barata) \n" <<
     "                5. Aleatoria \n" <<
     "                escolha: ";
    cin >> escolha;
  } while (escolha < 1 || escolha > 5);
  return escolha;
}


/* Menu GRASP */
int menu_GRASP(void)
{
  int escolha;

  do {
    cout << "\n*******************Menu GRASP************************* \n"  <<
         "                1. Vizinho Mais Proximo \n" <<
         "                2. Insercao Mais Barata \n" <<
         "                Escolha: ";
    cin >> escolha;
  } while (escolha < 1 || escolha > 2);
  return escolha;
}


/* Menu Algoritmos Geneticos */
int menu_AG(void)
{
  int escolha;

  do {
    cout << "\n****************Menu Algoritmos Geneticos********************** \n" <<
            "                1. Operador OX \n" <<
            "                2. Operador ERX \n" <<
            "                Escolha: ";
    cin >> escolha;
  } while (escolha < 1 || escolha > 2);
  return escolha;
}

