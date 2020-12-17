import numpy as np
from pulp import *

#Dados objetivos
nNo = 3
nMes = 3
nComponente = 2
nProduto = 2
nVeiculo = 2
nRota = 4

    #C do artigo
custoTransporte = np.array([
    [np.inf,1,2],
    [0.25,np.inf,4],
    [1,2,np.inf]
])

    #Ç do artigo

tempoSetup = np.array([
    [np.inf,1,1],
    [1,np.inf,1],
    [1,1,np.inf]
])

    #hINDICE do artigo (hA,hB etc)
custoArmazenamento = np.array([1,1,1])
    
    #rho do artigo
tempoProcessamento = np.array([1,1,1])

    #nCauda do artigo
proporcaoComponenteProduto = np.array([
    [1,np.inf,np.inf],
    [np.inf,1,np.inf],
    [np.inf,np.inf,1]
])
    #Imin do artigo
estoqueMin = np.array([1,1,1])

    #K do artigo
capacidadeProdutiva = np.array([100,100,100])

#Definindo Modelo
modelo = LpProblem("Modelao-Da-Massa",LpMinimize)
#Indices Variaveis
indicesX = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de X: ",indicesX)
indicesI = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de I: ",indicesI)
indicesY = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de Y: ",indicesY)
indicesZ = [str(A)+str(b)+str(t) for A in range(1, nComponente+1) for b in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de Z: ",indicesZ)
indicesPI = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de PI: ",indicesPI)
indicesW = [str(i)+str(j)+str(v)+str(r) for i in range(1, nNo+1) for j in range(1, nNo+1) for v in range(1, nVeiculo+1) for r in range(1, nRota+1)]
# print("indices de W: ",indicesW)
indicesQ = [str(p)+str(v)+str(r)+str(t) for p in range(1, nProduto+1) for v in range(1, nVeiculo+1) for r in range(1, nRota+1) for t in range(1, nMes+1)]
# print("indices de Q: ",indicesQ)
indicesS = [str(i)+str(v)+str(r)+str(t) for i in range(1, nNo+1) for v in range(1, nVeiculo+1) for r in range(1, nRota+1) for t in range(1, nMes+1)]
# print("indices de S: ",indicesS)
indicesU = [str(i)+str(v)+str(r) for i in range(1, nNo+1) for v in range(1, nVeiculo+1) for r in range(1, nRota+1)]
# print("indices de U: ",indicesU)

#Variaveis de Decisao
    #Quantidade produzida do item A no periodo t
xVar = LpVariable.matrix("X", indicesX, cat = "Integer", lowBound= 0 )
print("X: ",xVar)
    #Inventário do item A no final do periodo t
iVar = LpVariable.matrix("I", indicesI, cat = "Integer", lowBound= 0 )
print("I: ",iVar)
    #Igual a 1 se a linha tiver o setup do item A no periodo t, 0 caso contrário
yVar = LpVariable.matrix("Y", indicesY, cat = "Binary", lowBound= 0 )
print("Y: ",yVar)
    #Igual a 1 se houver troca de setup do item A pro item B no periodo t, 0 caso contrário
zVar = LpVariable.matrix("Z", indicesZ, cat = "Binary", lowBound= 0 )
print("Z: ",zVar)
    #Variável auxiliar para sequênciamento
piVar = LpVariable.matrix("PI", indicesPI, cat = "Continuous", lowBound= 0 )
print("PI: ",piVar)
    #Igual a 1 se o arco ij for navegado pela rota R do veículo V, 0 caso contrário
wVar = LpVariable.matrix("W", indicesW, cat = "Binary", lowBound= 0 )
print("W: ",wVar)
    #Quantidade do produto P despachado na rota R pelo veículo V no periodo t
qVar = LpVariable.matrix("Q", indicesQ, cat = "Integer", lowBound= 0 )
print("Q: ",qVar)
    #Igual a 1 se o nó for visitado pela rota R com o veículo V no periodo t, 0 caso contrário
sVar = LpVariable.matrix("S", indicesS, cat = "Binary", lowBound= 0 )
print("S: ",sVar)
    #Horário de início que o nó I é atendido pela rota R com o veículo V
uVar = LpVariable.matrix("U", indicesS, cat = "Continuous", lowBound= 0 )
print("U: ",uVar)
#Funcao Objetivo

#Modelo

#Restrições