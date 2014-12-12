#!/usr/bin/python3
import numpy as np
import random

class Edge:
    def __init__(self, start, end, length):
        self.start = start
        self.end = end
        self.length = length
        
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
        if upto + startList[i] > r:
            return i
        upto +=  startList[i]
    assert False, "Erro start!!!"
    return 0

def weighted_choice(phoM, choices):
    total = 0
    for e in choices:
        total += e.length * phoM[e.start, e.end]
    #total = sum(e.length for e in choices)
    r = random.uniform(0, total)
    upto = 0
    for e in choices:
        if upto + e.length * phoM[e.start, e.end] > r:
            return e
        upto += e.length * phoM[e.start, e.end]
    assert False, "Erro weighted_choice!!!"
   
def createChoices(start, unvisited, distM):
    choices = []
    for end in unvisited:
        choices.append(Edge(start, end, distM[start, end]))
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
        visited.append(j)
        unvisited.remove(j)
        path.append(Edge(i, j, distM[i, j]))
        pathSize += distM[i, j]

    return path, pathSize

def step(start, unvisited, distM, phoM):
    return weighted_choice(phoM, createChoices(start, unvisited, distM)).end

"""
Executa colonia de formigas em busca do caminho hamiltoniano de maior peso
"""
def solve(nodes, dist, nAnts = 100, iterations = 10):
    nodesSize = len(nodes)
    
    distM = np.zeros((nodesSize, nodesSize))
    phoM = np.zeros((nodesSize, nodesSize))
    phoM[:] = 0.01
    startList = [0.01] * nodesSize
    #startList.fill(0.01)

    # Inicializa matriz de distancias
    for index, v in np.ndenumerate(distM):
        distM[index] = dist(nodes[index[0]], nodes[index[1]])

    solution = False

    # Executa determinado numero de interações zerando os parametros
    for j in range(iterations):
        phoM[:] = 0.01
        startList = [0.01] * nodesSize
        # Caminha com cada formiga pelo grafo
        for i in range(0, nAnts):
            path, pathSize = antWalk(nodes, nodesSize, distM, phoM, startList)

            # Calcula a pontuação de iniciação dos caminhos
            startList[path[0].start] +=  0.01 * pathSize / nodesSize

            # Calula a pontuação dos feromonios da iteração         
            for edge in path:
                phoM[edge.start,edge.end] += 0.01 * pathSize / nodesSize

                #Converte indices para nos
                edge.start = nodes[edge.start]
                edge.end = nodes[edge.end]
            if not solution or solution.pathSize < pathSize:
                solution = Solution(path, pathSize)
    
    print(solution.pathSize)
    
    return solution

    