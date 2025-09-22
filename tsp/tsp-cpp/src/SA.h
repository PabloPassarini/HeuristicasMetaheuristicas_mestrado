//
// Created by Puca Penna on 13/09/2018.
//

#ifndef _PCV_SA_H_
#define _PCV_SA_H_

#include <vector>

float SA(int n, std::vector<int> &s, float **d, 
	     float alpha, float SAmax, double temp_inicial, 
	     double temp_final);

float temperaturaInicial(int n, std::vector<int> &s, float **d, 
	                     float beta, float gama, float SAmax, 
	                     double temp_inicial);

#endif //PCV_SA_H
