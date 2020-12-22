import numpy as np
from pulp import *

#Dados objetivos
nNo = 4
nMes = 3
nComponente = 3
nProduto = 3
nVeiculo = 2
nRota = 6

    #C do artigo
custoTransporte = np.zeros((4,4,6))
for i in range(nNo):
    for j in range(nNo):
        for r in range(nRota):
            if(i==j):
                custoTransporte[i][j][r] = np.inf
            else:
                custoTransporte[i][j][r] = 1
    #Ç do artigo

tempoSetup = np.array([[[np.inf,np.inf,np.inf],
  [1,1,1],
  [1,1,1]],

 [[1,1,1],
  [np.inf,np.inf,np.inf],
  [1,1,1]],

 [[1,1,1],
  [1,1,1],
  [np.inf,np.inf,np.inf]]])

    #hINDICE do artigo (hA,hB etc)
custoArmazenamento = np.array([1,2,3]).reshape(-1,1)
    
    #rho do artigo
tempoProcessamento = np.array([1,1,1])

    #nCauda do artigo
    #Aqui optou-se por restringir cada componente para um produto especifico e olhar únicamente para o produto
proporcaoComponenteProduto = np.array([1,2,3])
    #Imin do artigo
estoqueMin = np.array([1,1,1])

    #K do artigo
capacidadeProdutiva = np.array([100,100,100])

#Definindo Modelo
modelo = LpProblem("Modelao-Da-Massa",LpMinimize)
#Indices Variaveis
indicesX = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de X: ",indicesX)
indicesI = np.array([str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)])
# print("indices de I: ",indicesI)
indicesY = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de Y: ",indicesY)
indicesZ = [str(A)+str(b)+str(t) for A in range(1, nComponente+1) for b in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de Z: ",indicesZ)
indicesPI = [str(A)+str(t) for A in range(1, nComponente+1) for t in range(1, nMes+1)]
# print("indices de PI: ",indicesPI)
indicesW = [str(i)+str(j)+str(r) for i in range(1, nNo+1) for j in range(1, nNo+1) for r in range(1, nRota+1)]
# print("indices de W: ",indicesW)
indicesQ = [str(p)+str(r)+str(t) for p in range(1, nProduto+1) for r in range(1, nRota+1) for t in range(1, nMes+1)]
# print("indices de Q: ",indicesQ)
indicesS = [str(i)+str(r)+str(t) for i in range(1, nNo+1) for r in range(1, nRota+1) for t in range(1, nMes+1)]
# print("indices de S: ",indicesS)
indicesU = [str(i)+str(r) for i in range(1, nNo+1) for r in range(1, nRota+1)]
# print("indices de U: ",indicesU)
indicesA = [str(r)+str(v) for r in range(1,nRota+1) for v in range(1,nVeiculo+1)]
# print("indices de A: ",indicesA)
#Variaveis de Decisao
    #Quantidade produzida do item A no periodo t
xVar = LpVariable.matrix("X", indicesX, cat = "Integer", lowBound= 0 )
xVar = np.array(xVar).reshape(3,3)
print("X: ",xVar)
    #Inventário do item A no final do periodo t
iVar = LpVariable.matrix("I", indicesI, cat = "Integer", lowBound= 0 )
iVar = np.array(iVar).reshape(3,3)
print("I: ",iVar)
    #Igual a 1 se a linha tiver o setup do item A no periodo t, 0 caso contrário
yVar = LpVariable.matrix("Y", indicesY, cat = "Binary", lowBound= 0 )
yVar = np.array(yVar).reshape(3,3)
print("Y: ",yVar)
    #Igual a 1 se houver troca de setup do item A pro item B no periodo t, 0 caso contrário
zVar = LpVariable.matrix("Z", indicesZ, cat = "Binary", lowBound= 0 )
zVar = np.array(zVar).reshape(3,3,3)
print("Z: ",zVar)
    #Variável auxiliar para sequênciamento
piVar = LpVariable.matrix("PI", indicesPI, cat = "Continuous", lowBound= 0 )
piVar = np.array(piVar).reshape(3,3)
print("PI: ",piVar)
    #Igual a 1 se o arco ij for navegado pela rota R do veículo V, 0 caso contrário
wVar = LpVariable.matrix("W", indicesW, cat = "Binary", lowBound= 0 )
wVar = np.array(wVar).reshape(4,4,6)
print("W: ",wVar)
    #Quantidade do produto P despachado na rota R pelo veículo V no periodo t
qVar = LpVariable.matrix("Q", indicesQ, cat = "Integer", lowBound= 0 )
qVar = np.array(qVar).reshape(3,6,3)
print("Q: ",qVar)
    #Igual a 1 se o nó for visitado pela rota R com o veículo V no periodo t, 0 caso contrário
sVar = LpVariable.matrix("S", indicesS, cat = "Binary", lowBound= 0 )
sVar = np.array(sVar).reshape(4,6,3)
print("S: ",sVar)
    #Horário de início que o nó I é atendido pela rota R com o veículo V
uVar = LpVariable.matrix("U", indicesU, cat = "Continuous", lowBound= 0 )
uVar = np.array(uVar).reshape(4,6)
print("U: ",uVar)
aVar = LpVariable.matrix("A", indicesA, cat = "Binary", lowBound= 0 )
aVar = np.array(aVar).reshape(6,2)
print("A: ",aVar)
#Funcao Objetivo
objFunc = lpSum(custoArmazenamento*iVar)+lpSum(tempoSetup*zVar)+lpSum(custoTransporte*wVar)
# print(objFunc)
modelo+=objFunc
# print(modelo)
#Restrições

#Restrição 2 (_C1 até _C9)
for a in range(nComponente):
    for t in range(nMes):
        #Aqui optou-se por restringir cada componente para um produto especifico e olhar únicamente para o produto
        # print(iVar[a][t]+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota)))
        if(t==0):
            # print(200+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t])
            modelo+=200+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t]
        else:
            # print(iVar[a][t-1]+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t])
            modelo+=iVar[a][t-1]+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t]

#Restricao 3(_C10 até _C18)
for a in range(nComponente):
    for t in range(nMes):
        #Aqui optou-se por restringir cada componente para um produto especifico e olhar únicamente para o produto
        # print(iVar[a][t]+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota)))
        if(t==0):
            # print(200+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t])
            modelo+=200 >= lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))
        else:
            # print(iVar[a][t-1]+xVar[a][t] == lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))+iVar[a][t])
            modelo+=iVar[a][t-1] >= lpSum(proporcaoComponenteProduto[p] * qVar[p][r][t] for p in range(nProduto) for r in range(nRota))
print(modelo)

