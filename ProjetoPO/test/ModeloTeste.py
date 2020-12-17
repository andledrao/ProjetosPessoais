import numpy as np
from pulp import *

#Dados objetivos
nArmazem = 2
nProducao = 2

custoArmazem = np.array([
    [1,4],
    [3,2]
])

