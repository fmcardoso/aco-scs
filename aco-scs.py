#!/usr/bin/python3
import pantspath
import generator


# Inicia os framentos
# Descomentar para gerar
#generator.generate()

nodes = []

# Arquivo de framentos
fragFileName = "gen/fragments.txt"

fragFile = open(fragFileName, "r")
fragments = fragFile.readlines()
fragments = [x.strip('\n') for x in fragments]
for frag in fragments:
    nodes.append(frag)
fragFile.close()

# XXX - VÉRTICES DO GRAFO
# SLIDES - Peso solução otima: 3 + 3 + 4 + 4 = 14
#nodes.append('ACTACAC')
#nodes.append('CACTCAGGCA')
#nodes.append('GCATTCACTA')
#nodes.append('ACTAGAAATATA')
#nodes.append('TATACCAGC')


# FUNÇÃO PARA CALCULAR O TAMANHO DA ARESTA ENTRE DOIS VÉRTICES
# 100 - Número mágico que é maior que todas os fragmentos
def dist(a, b):
	for i in range(0, len(b), 1):
		if (a.endswith(b[0:len(b) - i])):
			return 1000 - (len(b) - i) # CASO EXISTA ARESTA, RETORNA O TAMANHO
	return 1000 #

world = pantspath.World(nodes, dist)
solver = pantspath.Solver(rho = 0.1, limit = 10, ant_count = 10)
solution = solver.solve(world)

print("Nodes: ", nodes)
print("Nós visitados em ordem: ", solution.tour)
print("Tamanho da solução: ", solution.distance)
print("Tamanho da solução: ", -(solution.distance - (1000 * len(nodes))))

# Construi a SCS
scs = ""
for edge in solution.path:
	# Adiciono o prefixo de cada no do caminho da solução
	f = edge.start
	# Não considero o utlimo nó pois ele vai ser o primeiro
	end = edge.end
	scs = scs + f[0:len(f) - (1000 - edge.length)]
	#print("Aresta", f[0:len(f) - (100 - edge.length)])

# Adiciono o sufixo da ultima palavra
scs = scs + end
print("SCS Solution:", scs)
