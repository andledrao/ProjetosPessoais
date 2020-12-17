import numpy as np
from pulp import *

#Dados objetivos
nArmazem = 2
nProducao = 2

custoArmazem = np.array([
    [1,4],
    [3,2]
])

#Indices Variaveis
indiceVariaveis = [str(i)+str(j) for j in range(1, nArmazem+1) for i in range(1, nProducao+1)]
indiceVariaveis.sort()

#Variaveis de Decisao
DV_variables = LpVariable.matrix("X", indiceVariaveis, cat = "Integer", lowBound= 0 )
print(DV_variables)