import numpy as np
from pulp import *

#Dados objetivos

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

#Variaveis de Decisao

#Funcao Objetivo

#Modelo

#Restrições