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

""" Escolhe o incicio mais pesado """
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

""" Cria opções de escolha """
def createChoices(start, unvisited, distM, phoM, beta):
    choices = []
    for end in unvisited:
        # Arestas de tamanho -1 não são consideradas
        if (distM[start, end] > -1):
            choices.append(Edge(start, end, (distM[start, end]  ** beta) * phoM[start, end]))
    return choices

""" Retorna melhor opção viavel da lista de candidatos """
def getFromCandidateList(clM, start, unvisited):
    for option in clM[start,:]:
        if option in unvisited:
            return option
    return -1
    
""" Efetua os passeios de cada formiga """
def antWalk(nodes, nodesSize, distM, phoM, start, phomDeposited, clM,
            beta, q0, cl):
    unvisited = list(range(0, nodesSize))

    i = start
    unvisited.remove(i)
    visited = [i]
   
    path = []
    pathSize = 0
    
    while len(unvisited) > 0:   
        j = step(i, unvisited, distM, phoM, beta, q0, clM, cl)
        
        # Verifica se não há mais caminhos válidos
        if (j < 0):
            return None, -1
        
        visited.append(j)
        unvisited.remove(j)
        localUpdateDecrease(i, j, phomDeposited, phoM)
        path.append(Edge(i, j, distM[i, j]))
        pathSize += distM[i, j]
        i = j

    return path, pathSize

""" Caminha para um vértice """
def step(start, unvisited, distM, phoM, beta, q0, clM, cl):
    q = random.random()

    if cl and q <= q0:
        end = getFromCandidateList(clM, start, unvisited)
        if end > 0:
            return end
    
    choices = createChoices(start, unvisited, distM, phoM, beta)
    
    if len(choices) == 0:
        return -1

    if q <= q0:
        return maximalChoice(choices).end
    else:
        return weighted_choice(choices).end

""" Adiciona os feromonios dada uma solução de entrada """
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

""" Update global de execução """
def globalUpdate(bestSolution, alpha, phoM):
     # Inicializa matriz de distancias
    for index, v in np.ndenumerate(phoM):
        phoM[index] = (1 - alpha) * phoM[index]
    
    for edge in bestSolution.path:
        phoM[edge.start,edge.end] += alpha * bestSolution.pathSize

""" Reduz a quantidade de feromonio de um aresta visitada """
def localUpdateDecrease(start, end, phomDeposited, phoM, alpha = 0.1):
    phoM[start, end] = (1 - alpha) * phoM[start, end] + (alpha * phomDeposited )

""" Reduz a quantidade de feromonio de todas as areastas """       
def localUpdate(path,pathSize, phomDeposited, alpha, phoM, bestPath):
     for edge in path:
        phoM[edge.start,edge.end] = (1 - alpha) * phoM[edge.start,edge.end] 
        + (alpha * phomDeposited )

""" Inicializa a lista de candidatos """
def initializeCL(nodesSize, distM):
    clM = np.zeros((nodesSize, min(15, nodesSize)))
    
    for i in range(nodesSize):
        sorted = np.argsort(distM[i,:])
       
        clM[i,:] = sorted[::-1][:min(15, nodesSize)]
    
    return clM.astype(int)

""" Optimzação local 3-opt para um caminho """
def localOptimization(path, clM, distM, nodesSize):
    optV = list(range(0, nodesSize))
    
    for i in range(1):
        j = random.choice(optV)
        
        e1 = path[j]
        k = e1.start
        l = e1.end
        q = clM[k, 0]
        
        if q != l and distM[k, l] < distM[k, q]:
            for e in path:
                if e.end == q:
                    e2 = e
                    p = e.start
                    break
           
            optV.remove(k)
            optV.remove(l)
            optV.remove(q)
            optV.remove(p)
            r = random.choice(optV)
            for e in path:
                if e.start == r:
                    s = e.end
                    e3 = e
                    break
            print(distM[k, q] + distM[p, s] + distM[r, l], distM[k, q] + distM[p, s] + distM[r, l])
            if (distM[k, q] + distM[p, s] + distM[r, l]) > ([k, l] + distM[p, q] + distM[r, s]):
                e1.end = q
                e1.length = distM[k, q]
                e2.end = s
                e2.length = distM[p, s]
                e3.end = l
                e3.length = distM[r, l]
                print("entrouuuu ")
                
                
"""
Executa colonia de formigas em busca do caminho hamiltoniano de maior peso
"""
def solve(nodes, dist, nAnts = 10, iterations = 150, initialPath = [],
          alpha=0.1, beta = 2, q0 = 0.9, cl = True):
    nodesSize = len(nodes)
    
    # Reseta a seed do random
    random.seed()
    
    # Calcula o feromonio inicial
    phomDeposited = 1500/(nodesSize)
    
    distM = np.zeros((nodesSize, nodesSize))
    phoM = np.zeros((nodesSize, nodesSize))
    phoM[:] = phomDeposited
    startList = [phomDeposited] * nodesSize
    #startList.fill(0.01)

    # Inicializa matriz de distancias
    for index, v in np.ndenumerate(distM):
        if index[0] != index[1]:
            distM[index] = dist(nodes[index[0]], nodes[index[1]])
        else:
            distM[index] = 0

    clM = initializeCL(nodesSize, distM)

    if len(initialPath) > 0:
        solution = buildSolutionByPath(initialPath, distM, phoM, startList,
                                       phomDeposited)
    else:
        solution = Solution([], 1)
        
    print("Inicialização", solution.pathSize)
    plateu = 0
    # Executa determinado numero de interações zerando os parametros
    antPaths = [None]* nAnts
    antPathsSize = [0] * nAnts
    
    be = []
    
    for j in range(iterations):
#         phoM[:] = phomDeposited
#         startList = [phomDeposited] * nodesSize

        starts = random.sample(range(nodesSize), nAnts)
        
        # Caminha com cada formiga pelo grafo
        for i in range(0, nAnts):
            path, pathSize = antWalk(nodes, nodesSize, distM, phoM, starts[i],
                                     phomDeposited, clM, beta, q0, cl)
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
                print("Novo ótimo:", pathSize)
                plateu = 0
                solution = Solution(path, pathSize)
            else:
                plateu = plateu + 1;
            
            #localOptimization(path, clM, distM, nodesSize)
            
        if plateu > iterations * nAnts /2:
            break
        
        # Atualiza os vetores do grafico
        v = 0
        for edge in solution.path:
            v = v + (distM[edge.start, edge.end]  ** beta) * phoM[edge.start, edge.end]
        
        v = v/ nodesSize
        be.append(v)
             
        globalUpdate(solution, alpha, phoM)
        
#     Plota o grafico da relação de feromonios.
#     plt.figure(1)
#     plt.plot(be, label = "be")
#     plt.show()
    
     #Converte indices para nos
    for edge in solution.path:
        edge.start = nodes[edge.start]
        edge.end = nodes[edge.end]
    
    print("Final", solution.pathSize, " plato ", plateu, "\n")
    
    return solution

    