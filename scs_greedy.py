#!/usr/bin/python3
import operator
import copy
from pygraph.classes.digraph import digraph
from pygraph.algorithms.cycles import find_cycle
from levenshtein import levenshtein

# Classe aresta contendo a origem, o destino, o peso e uma flag indicando se ela e valida para adiocionar no caminho hamiltoniano
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

# Classe Grafo, contendo uma lista de vertices e uma lista de arestas
class Graph:
  def __init__(self, vertexes):
    self.edges = []
    self.vertexes = vertexes
    
  def __repr__(self):
    return "{%s, %s}" % (self.edges, self.vertexes)

  # Metodo para encontrar uma aresta dado origem e destino
  def getEdge(self, x, y):
    for edge in self.edges:
      if edge.source==x and edge.target==y:
            return edge
    return None

  # Metodo para buscar uma aresta dado sua origem
  def getEdgeBySource(self, x):
    for edge in self.edges:
      if edge.source==x:
            return edge
    return None  

# Funcao que determina o peso da aresta
def find_overlap(node1, node2):
  overlap = 0;
  for i in range(0, len(node2), 1):
    if (node1.endswith(node2[0:i+1])):
      overlap = i+1 # CASO EXISTA ARESTA, RETORNA O TAMANHO
  return overlap

# Funcao que controi o grafo recebendo a lista de fragmentos como parametro
def build_graph(nodes):
  vertexes = [0 for x in range(len(nodes))] 
  
  for i in range(len(nodes)):
    vertexes[i] = nodes[i]

  graph = Graph(vertexes)
  edges = []

  for x in range(0, len(nodes)):
    for y in range(0, len(nodes)):
      if x!=y:
        edges.append(Edge(x, y, find_overlap(nodes[x], nodes[y])))
  graph.edges = sorted(edges, key=lambda edge: edge.weight, reverse=True)
  return graph
  
  # Funcao que verifica se um grafo tera um ciclo caso se adiciona uma aresta. O parametro tree representa o grafo antes da adicao da aresta
def hasCycle(trees, edge):
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

# Funcao para montar a sequencia dado um caminho hamiltoniano
def assemblyFragment(path):
  aux = []
  for x in path.edges:
    aux.append(x.target)

  for edge in path.edges:
    if edge.source not in aux:
      first = edge
  
  edge = first
  
  scs = ""
  while edge != None:
    node = path.vertexes[edge.source]
    scs+=node[:len(node)-edge.weight]
    if (path.getEdgeBySource(edge.target) == None):
      scs+=path.vertexes[edge.target]

    edge = path.getEdgeBySource(edge.target)
  return scs

# Funcao para que encontra um caminho hamiltonino. O primeiro parametro representa o arquivo que contem a lista de fragmentos, o segundo 
# representa o arquivo onde serao gravados os resultados da execucao e o terceiro e o arquivo que contem os resultados do guloso e do acs para
# posterior comparacao
def solve(fragFileName, outputFile, seqFileName):
    # Montar o grafo
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

    graph = build_graph(nodes)

    path = Graph([])
    path.vertexes = [0 for x in range(len(nodes))]
    trees = []

    #### Encontrar o caminho hamiltoniano
    for edge in graph.edges:
        for x in path.edges:
            # Verifica se a origem e o destino da aresta candidata ja existem no grafo
            if edge.source == x.source:
                edge.valid = False
            elif edge.target == x.target:
                edge.valid = False

        # Verifica se a adicao da aresta ira formar ciclo no caminho
        if edge.valid and hasCycle(trees, edge):
            edge.valid = False
        
        # Se aresta passar pelos testes anteriores ela e adcionada ao caminho
        if (edge.valid):
            path.edges.append(edge)
        if graph.vertexes[edge.source] not in path.vertexes:
            path.vertexes[edge.source] = graph.vertexes[edge.source]
        if graph.vertexes[edge.target] not in path.vertexes: 
            path.vertexes[edge.target] = graph.vertexes[edge.target]
        
        if len(nodes) == len(path.edges) + 1:
            break
    
    #### Monta a sequencia baseada no caminho encontrado
    assembledSequence = assemblyFragment(copy.deepcopy(path))
    # Tamanho da solução
    result = len(assembledSequence)
    
    # # Distância da solução
    seqFile = open(seqFileName, "r")
    sequence = seqFile.readlines()
    dist = levenshtein.levenshteinDistance(assembledSequence, sequence[0])

    outputFile.write('\nGreedy: Tamanho da sequencia montada: ' + str(result))
    outputFile.write("\nnGreedy: Levenshtein Distance = " + 
    str(dist));
    return result, dist, trees
