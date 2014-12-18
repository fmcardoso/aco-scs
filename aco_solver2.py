#!/usr/bin/python3
import numpy as np
import random
import matplotlib.pyplot as plt

class Edge:
    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length
        
    def __str__(self):
        return str(self.start) + " -> " + str(self.end) 
        
class Solution:
    def __init__(self, path, pathSize):
        self.path = path
        self.pathSize = pathSize

def choose_start(startList):
    total = 0
    for i in range(len(startList)):
        total += startList[i]
    #total = sum(e.length for e in choices)
    r = random.uniform(0, total)
    upto = 0
    for i in range(len(startList)):
        if upto + startList[i] >= r:
            return i
        upto +=  startList[i]
    assert False, "Erro start!!!"
    return 0

"""
 Escolhe a aresta mais pesada em forma de roleta.
"""
def weighted_choice(choices):
    total = sum(e.length for e in choices)
    r = random.uniform(0, total)
    upto = 0
    for e in choices:
        if upto + e.length >= r:
            return e
        upto += e.length
    assert False, "Erro weighted_choice!!!"
"""
 Retorna a melhor escolha dentro das possiveis
"""
def maximalChoice(choices):
    bestV = 0
    bestE = 0
    
    for e in choices:
        if e.length >= bestV:
            bestE = e
            bestV = e.length
    
    return bestE
   
def createChoices(start, unvisited, distM, phoM, beta):
    choices = []
    for end in unvisited:
        # Arestas de tamanho -1 não são consideradas
        if (distM[start, end] > -1):
            choices.append(Edge(start, end, (distM[start, end]  ** beta) * phoM[start, end]))
    return choices
    
def antWalk(nodes, nodesSize, distM, phoM, start, phomDeposited):
    unvisited = list(range(0, nodesSize))

    i = start
    unvisited.remove(i)
    j = random.choice(unvisited)
    unvisited.remove(j)
    visited = [i, j]
   
    path = [Edge(i, j, distM[i, j])]
    pathSize = distM[i, j]
    
    while len(unvisited) > 0:
        localUpdate2(i, j, phomDeposited, phoM)
        i = j
        j = step(j, unvisited, distM, phoM)
        
        # Verifica se não há mais caminhos válidos
        if (j < 0):
            return None, -1
        
        visited.append(j)
        unvisited.remove(j)
        path.append(Edge(i, j, distM[i, j]))
        pathSize += distM[i, j]

    return path, pathSize

def step(start, unvisited, distM, phoM, beta = 2, q0 = 0.9):
    choices = createChoices(start, unvisited, distM, phoM, beta)
    
    if len(choices) == 0:
        return -1
    
    q = random.random()

    if q <= q0:
        return maximalChoice(choices).end
    else:
        return weighted_choice(choices).end

def buildSolutionByPath(initialPath, distM, phoM, startList, phomDeposited):
    solution = Solution([], 0)
    start = initialPath[0]
    
    startList[start] +=  500
    for end in initialPath:
        solution.path.append(Edge(start, end, distM[start, end]))
        solution.pathSize += distM[start, end]
        
        
        phoM[start, end] += phomDeposited * 500
        start = end
    return solution

def globalUpdate(bestSolution, alpha, phoM):
     # Inicializa matriz de distancias
    for index, v in np.ndenumerate(phoM):
        phoM[index] = (1 - alpha) * phoM[index]
    
    for edge in bestSolution.path:
        phoM[edge.start,edge.end] += alpha * bestSolution.pathSize

def localUpdate2(start, end, phomDeposited, phoM, alpha = 0.1):
    phoM[start, end] = (1 - alpha) * phoM[start, end] + (alpha * phomDeposited )
          
def localUpdate(path,pathSize, phomDeposited, alpha, phoM, bestPath):
     for edge in path:
        phoM[edge.start,edge.end] = (1 - alpha) * phoM[edge.start,edge.end] 
        + (alpha * phomDeposited )

"""
Executa colonia de formigas em busca do caminho hamiltoniano de maior peso
"""
def solve(nodes, dist, nAnts = 20, iterations = 100, initialPath = [], alpha=0.05):
    nodesSize = len(nodes)
    
    # Reseta a seed do random
    random.seed()
    
    phomDeposited = 1500/(nodesSize)
    
    distM = np.zeros((nodesSize, nodesSize))
    phoM = np.zeros((nodesSize, nodesSize))
    phoM[:] = phomDeposited
    startList = [phomDeposited] * nodesSize
    #startList.fill(0.01)

    # Inicializa matriz de distancias
    for index, v in np.ndenumerate(distM):
        distM[index] = dist(nodes[index[0]], nodes[index[1]])

    if len(initialPath) > 0:
        solution = buildSolutionByPath(initialPath, distM, phoM, startList,
                                       phomDeposited)
    else:
        solution = Solution([], 1)
        
    print("Inicialização", solution.pathSize)
    invalid = 0
    # Executa determinado numero de interações zerando os parametros
    antPaths = [None]* nAnts
    antPathsSize = [0] * nAnts
    
    be = []
    te = []
    ue = []
    
    for j in range(iterations):
#         phoM[:] = phomDeposited
#         startList = [phomDeposited] * nodesSize

        starts = random.sample(range(nodesSize), nAnts)
        
        # Caminha com cada formiga pelo grafo
        for i in range(0, nAnts):
            path, pathSize = antWalk(nodes, nodesSize, distM, phoM, starts[i], phomDeposited)
            antPaths[i] = path
            antPathsSize[i] = pathSize
        
                
        # Atualiza os feromonios
        for i in range(0, nAnts):
            path = antPaths[i]
            pathSize = antPathsSize[i]
            if pathSize > 0:
                # Calcula a pontuação de iniciação dos caminhos
                startList[path[0].start] +=  phomDeposited * pathSize     
                
                # Calula a pontuação dos feromonios da iteração         
               # localUpdate(path, pathSize, phomDeposited, alpha, phoM, solution.pathSize)

            if solution.pathSize == 0 or solution.pathSize < pathSize:
                print("Resolve Trocar =D =D =D", pathSize)
                solution = Solution(path, pathSize)
            else:
                invalid = invalid + 1;
        
        # Atualiza os vetores do grafico
        v = 0
        for edge in solution.path:
            v = v + (distM[edge.start, edge.end]  ** 2) * phoM[edge.start, edge.end]
        
        v = v/ nodesSize
        be.append(v)
             
        globalUpdate(solution, alpha, phoM)
        
    
    plt.figure(1)
    plt.plot(be, label = "be")
    plt.show()
    
     #Converte indices para nos
    for edge in solution.path:
        edge.start = nodes[edge.start]
        edge.end = nodes[edge.end]
    
    print("Final", solution.pathSize, " increment ", invalid, "\n")
    
    return solution

    