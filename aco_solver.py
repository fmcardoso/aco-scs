#!/usr/bin/python3
import numpy as np
import random
from oauthlib.uri_validate import ALPHA

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

# Delta [0 ... 1], quando mais proximo de 0, mais ele privilegia o peso da aresta
# quanto mais proximo de 1 o contrario

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
    
def antWalk(nodes, nodesSize, distM, phoM, startList):
    unvisited = list(range(0, nodesSize))
    
    i = choose_start(startList)
    unvisited.remove(i)
    j = random.choice(unvisited)
    unvisited.remove(j)
    visited = [i, j]
   
    path = [Edge(i, j, distM[i, j])]
    pathSize = distM[i, j]
    
    while len(unvisited) > 0:
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

def step(start, unvisited, distM, phoM, beta = 0.8, q0 = 0.9):
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
    
    startList[start] +=  phomDeposited * 5
    for end in initialPath:
        solution.path.append(Edge(start, end, distM[start, end]))
        solution.pathSize += distM[start, end]
        
        
        phoM[start, end] += phomDeposited * 5
        start = end
    return solution

def finishAntWalk(phoM, startList, bestSolution, decaimento, phomDeposited):
    for edge in bestSolution.path:
        phoM[edge.start,edge.end] += phomDeposited
        startList[edge.start] += phomDeposited
    
    for index, v in np.ndenumerate(phoM):
        phoM[index] = max(v / decaimento, phomDeposited)
        
    for start in startList:
        start = max(start / decaimento, phomDeposited)
        
"""
Executa colonia de formigas em busca do caminho hamiltoniano de maior peso
"""
def solve(nodes, dist, nAnts = 100, iterations = 10, initialPath = [],
          phomDeposited = 1, decaimento = 1.05):
    nodesSize = len(nodes)
    
    # Reseta a seed do random
    random.seed()
    
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
    for j in range(iterations):
        phoM[:] = phomDeposited
        startList = [phomDeposited] * nodesSize
        
        finishAntWalk(phoM, startList, solution, 1,
                          phomDeposited)  
        # Caminha com cada formiga pelo grafo
        for i in range(0, nAnts):
            path, pathSize = antWalk(nodes, nodesSize, distM, phoM, startList)
            
            if pathSize > 0:
                # Calcula a pontuação de iniciação dos caminhos
                startList[path[0].start] +=  phomDeposited * pathSize     
                
                # Calula a pontuação dos feromonios da iteração         
                for edge in path:
                    phoM[edge.start,edge.end] += phomDeposited * pathSize 
    
                if solution.pathSize == 0 or solution.pathSize < pathSize:
                    print("Resolve Trocar =D =D =D", pathSize)
                    solution = Solution(path, pathSize)
            else:
                invalid = invalid + 1;
                
            finishAntWalk(phoM, startList, solution, decaimento,
                          phomDeposited)
    
     #Converte indices para nos
    for edge in solution.path:
        edge.start = nodes[edge.start]
        edge.end = nodes[edge.end]
    
    print("Final", solution.pathSize, " increment ", invalid, "\n")
    
    return solution

    