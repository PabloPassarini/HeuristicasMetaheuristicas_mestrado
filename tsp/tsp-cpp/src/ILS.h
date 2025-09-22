#ifndef _ILS_H_
#define _ILS_H_

#include <vector>
using namespace std;


float perturbacao(int n, vector<int> &s, float **d, float fo, int nivel);

float ILS(int n, vector<int> &s, float **d,
          int nivel, // nro de vezes sem melhora em um dado nivel
          int ILSmax) ;

float SmartILS(int n, vector<int> &s, float **d, 
	           int nivel, 
			   int nVezesNivel, 
			   int ILSMax);

#endif