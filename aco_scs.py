#!/usr/bin/python3

import pantspath
from levenshtein import levenshtein

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
	#nodes.append('ACTACAC')
	#nodes.append('CACTCAGGCA')
	#nodes.append('GCATTCACTA')
	#nodes.append('ACTAGAAATATA')
	#nodes.append('TATACCAGC')

	# FUNÇÃO PARA CALCULAR O TAMANHO DA ARESTA ENTRE DOIS VÉRTICES
	def dist(a, b):
		for i in range(0, len(b), 1):
			if (a.endswith(b[0:len(b) - i])):
				return  (len(b) - i) # CASO EXISTA ARESTA, RETORNA O TAMANHO
		return 0.0001 #Numero muito pequeno tendendo a zero

	world = pantspath.World(nodes, dist)
	solver = pantspath.Solver(limit = 10, beta = 6, ant_count = 100)
	solution = solver.solve(world)

	#outputFile.write("Nodes: " +  str(nodes))
	#outputFile.write("Nós visitados em ordem: " +  str(solution.tour))
	#outputFile.write("Distancia da solução: " +  str(solution.distance))
	# Escrever aqui os parâmetros utilizados em cada execução
	outputFile.write("\nParâmetros Utilizados:"  +
		"\n\talpha: " + str(solver.alpha) +
        "\n\tbeta: " + str(solver.beta) +
        "\n\trho: " + str(solver.rho) +
        "\n\tq: " + str(solver.q) +
        "\n\tt0: " + str(solver.t0) +
        "\n\tlimit: " + str(solver.limit) +
        "\n\tant_count: " + str(solver.ant_count) +
        "\n\telite: " + str(solver.elite))


	# Construi a SCS
	scs = ""
	for edge in solution.path:
		# Adiciono o prefixo de cada no do caminho da solução
		f = edge.start
		# Não considero o utlimo nó pois ele vai ser o primeiro
		end = edge.end
		scs = scs + f[0:len(f) - int(edge.length)]
		#print("Aresta", f[0:len(f) - (100 - edge.length)])

	# Adiciono o sufixo da ultima palavra
	scs = scs + end

	# Tamanho solução
	result = len(scs)
	
	# Distancia da solução
	seqFile = open(seqFileName, "r")
	sequence = seqFile.readlines()
	dist = levenshtein.levenshteinDistance(scs, sequence[0])

	outputFile.write("\nACO: SCS Solution Size: " + str(result) + "\n")
	#outputFile.write("\nSCS Solution:" + scs + "\n")
	outputFile.write("\nACO: Levenshtein Distance = " + str(dist));

	return result, dist
