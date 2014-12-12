#!/usr/bin/python3
import operator
import copy
from pygraph.classes.digraph import digraph
from pygraph.algorithms.cycles import find_cycle
from levenshtein import levenshtein

class Edge:
  def __init__(self, source, target, weight):
    self.source = source
    self.target = target
    self.weight = weight
    self.valid = True

  def __repr__(self):
    return "{%s, %s, %s, %s}" % (self.source, self.target, self.weight, self.valid)

  def __str__(self):
    return "{%s, %s, %s, %s}" % (self.source, self.target, self.weight, self.valid)

class Graph:
  def __init__(self, vertexes):
    self.edges = []
    self.vertexes = vertexes
    
  def __repr__(self):
    return "{%s, %s}" % (self.edges, self.vertexes)

  def getEdge(self, x, y):
    for edge in self.edges:
      if edge.source==x and edge.target==y:
            return edge
    return None

class Solution:
  def __init__(self):
    self.vertexes = []
    self.sequence = ''
   
  def __repr__(self):
    return "{%s, %s}" % (self.sequence, self.vertexes)
 
def find_overlap(node1, node2):
  overlap = 0;
  for i in range(0, len(node2), 1):
    if (node1.endswith(node2[0:i+1])):
      overlap = i+1 # CASO EXISTA ARESTA, RETORNA O TAMANHO
  return overlap

def build_graph(nodes):
  graph = Graph(nodes)
  #print(graph.vertexes)
  edges = []
  for x in range(0, len(nodes)):
    for y in range(0, len(nodes)):
      if x!=y:
        edges.append(Edge(x, y, find_overlap(nodes[x], nodes[y])))
  graph.edges = sorted(edges, key=lambda edge: edge.weight, reverse=True)
  return graph
  
def build_graph_to_find_cycle(nodes):
  graph = digraph()

  for x in range (0, len(nodes)):
    graph.add_node(x)
  
  return graph

def hasCycle(digraph, edge):
  digraph.add_edge((edge.source,edge.target), edge.weight)
  if not find_cycle(digraph):
    return False
  else: return True

def hasCycle2(trees, edge):
    sT = False
    sS = False
    
    for t in trees:
        if edge.source in t and edge.target in t:
            return True
        elif edge.target in t:
            sT = t
        elif edge.source in t:
            sS = t
    
    if sT == False and sS == False:
        trees.append([edge.source, edge.target])
    elif sT != False and sS != False:
        sS.extend(sT)
        trees.remove(sT)
    elif sT != False:
        sT2 = [edge.source]
        trees.remove(sT)
        sT2.extend(sT)
        trees.append(sT2)
    elif sS != False:
        sS = sS.append(edge.target)
        
    return False

def join(finalSolution, graph):
  if (len(finalSolution) > 1):
    for solution in finalSolution:
      for solution2 in finalSolution:
        if (solution!=solution2):
          if solution.vertexes[-1] == solution2.vertexes[0]:
            partialSolution = Solution()
            solutionToRemove1 = solution
            solutionToRemove2 = solution2
            for x in range(0, len(solution.vertexes)):
              partialSolution.vertexes.append(solution.vertexes[x])
            for x in range(1, len(solution2.vertexes)):
              partialSolution.vertexes.append(solution2.vertexes[x])
            partialSolution.sequence = solution.sequence + solution2.sequence[len(graph.vertexes[solution.vertexes[-1]]):]
    finalSolution.remove(solutionToRemove1)
    finalSolution.remove(solutionToRemove2)
    finalSolution.append(partialSolution)
    join(finalSolution, graph)
  else: return finalSolution

def assembyFragment(path, nodes, graph):
  finalSolution = []

  for edge in path.edges:
    solution = Solution()
    solution.vertexes.append(edge.source)
    solution.vertexes.append(edge.target)
    solution.sequence += nodes[edge.source] + nodes[edge.target][edge.weight:]
    finalSolution.append(solution)

  join(finalSolution, graph)
  return finalSolution

def solve(fragFileName, outputFile, seqFileName):
    nodes = []
  
    fragFile = open(fragFileName, "r")
    fragments = fragFile.readlines()
    fragments = [x.strip('\n') for x in fragments]
    for frag in fragments:
        included = False
        for existing in nodes:
            if frag in existing:
                included = True
                break
            
        if not included:
            nodes.append(frag)
    fragFile.close()

  # XXX - VÉRTICES DO GRAFO
    # SLIDES - Peso solução otima: 3 + 3 + 4 + 4 = 14
#   nodes.append('ACTACAC')
#   nodes.append('CACTCAGGCA')
#   nodes.append('GCATTCACTA')
#   nodes.append('ACTAGAAATATA')
#   nodes.append('TATACCAGC')

    graph = build_graph(nodes)

#     print('Graph: ', graph.edges, '\n')

    path = Graph([])
    trees = []
    
    #### ENCONTRAR CAMINHO HAMILTONIANO
    for edge in graph.edges:
        for x in path.edges:
            if edge.source == x.source:
                edge.valid = False
            elif edge.target == x.target:
                edge.valid = False

        if edge.valid and hasCycle2(trees, edge):
            edge.valid = False
    
        if (edge.valid):
            path.edges.append(edge)
        if edge.source not in path.vertexes:
            path.vertexes.append(edge.source)
        if edge.target not in path.vertexes: 
            path.vertexes.append(edge.target)
        
        if len(nodes) == len(path.edges) + 1:
            break
    
 
    #### MONTAR A SEQUENCIA ORIGINAL
    assembledSequence = assembyFragment(copy.deepcopy(path), nodes, graph)
    # Tamanho da solução
    result = len(assembledSequence[0].sequence)
    
    # Distância da solução
    seqFile = open(seqFileName, "r")
    sequence = seqFile.readlines()
    dist = levenshtein.levenshteinDistance(assembledSequence[0].sequence, sequence[0])

    outputFile.write('\nGreedy: Tamanho da sequencia montada: ' + str(result))
    outputFile.write("\nnGreedy: Levenshtein Distance = " + 
    str(dist));
    return result, dist, trees
