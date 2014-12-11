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


def weighted_choice(choices):
    total = sum(e.length for e in choices)
    r = random.uniform(0, total)
    upto = 0
    for e in choices:
        if upto + e.length > r:
            return e
        upto += e.length
    assert False, "Shouldn't get here"
   
def createChoices(start, unvisited, distM):
    choices = []
    for end in unvisited:
        choices.append(Edge(start, end, distM[start, end]))
    return choices
    
def antWalk(nodes, nodesSize, distM):
    unvisited = list(range(0, nodesSize))
    
    i = random.choice(unvisited)
    unvisited.remove(i)
    j = random.choice(unvisited)
    unvisited.remove(j)
    
    visited = [i, j]
   
    path = [Edge(nodes[i], nodes[j], distM[i, j])]
    pathSize = distM[i, j]
    
    while len(unvisited) > 0:
        i = j
        j = step(j, unvisited, distM)
        visited.append(j)
        unvisited.remove(j)
        path.append(Edge(nodes[i], nodes[j], distM[i, j]))
        pathSize += distM[i, j]

    return path, pathSize

def step(start, unvisited, distM):
    return weighted_choice(createChoices(start, unvisited, distM)).end

def solve(nodes, dist, nAnts = 1000):
    nodesSize = len(nodes)
    
    distM = np.zeros((nodesSize, nodesSize))
    
    for index, v in np.ndenumerate(distM):
        distM[index] = dist(nodes[index[0]], nodes[index[1]])

    solution = False
    for i in range(0, nAnts):
        path, pathSize = antWalk(nodes, nodesSize, distM)
        if not solution or solution.pathSize < pathSize:
            solution = Solution(path, pathSize)
    
    print(solution.pathSize)
    
    return solution

    