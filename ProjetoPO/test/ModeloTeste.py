import numpy as np
from pulp import *

#Dados objetivos
nArmazem = 2
nProducao = 2

custoArmazem = np.array([
    [1,4],
    [3,2]
])
#Definindo Modelo
model = LpProblem("Modelo-de-Teste",LpMinimize)

#Indices Variaveis
indiceVariaveis = [str(i)+str(j) for j in range(1, nArmazem+1) for i in range(1, nProducao+1)]
indiceVariaveis.sort()
print("Indices de x: ",indiceVariaveis,"\n")

#Variaveis de Decisao
xVar = LpVariable.matrix("X", indiceVariaveis, cat = "Integer", lowBound= 0 )
xVar = np.array(xVar).reshape(2,2)
print("X: ",xVar,"\n")

#Funcao Objetivo
obj_func = lpSum(xVar*custoArmazem)
print("Funcao objetivo: ",obj_func,"\n")

#Modelo
model +=  obj_func
print(model)

#Restrições

    #Somatoria <= 80 
for i in range(nProducao):
    model += lpSum(xVar[i][j] for j in range(nProducao))<=80, "Restricao de Producao"+str(i)
print(model)