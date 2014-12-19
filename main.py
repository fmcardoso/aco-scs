#!/usr/bin/python3
import generator
import aco_scs
import scs_greedy
import os
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import datetime
import time
import json
import numpy as np
import plot_helper as ph

ts = time.time()

seqSize = 1000
fragmentSize = 50
coverage = 8

fragmentsDir = "gen/fragments/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"
seqDir = "gen/sequences/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"
resultsDir = "gen/results/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"
dataPath = "results/data.json"
plotPath = "results/chart"

# Cria as pastas caso não existam
if not os.path.exists(os.path.dirname(fragmentsDir)):
	os.makedirs(os.path.dirname(fragmentsDir))
if not os.path.exists(os.path.dirname(seqDir)):
	os.makedirs(os.path.dirname(seqDir))
if not os.path.exists(os.path.dirname(resultsDir)):
	os.makedirs(os.path.dirname(resultsDir))
if not os.path.exists(os.path.dirname(dataPath)):
	os.makedirs(os.path.dirname(dataPath))

# Inicia os framentos
# Descomentar para gerar as sequências
for i in range(1, 10):
	generator.generate(fragmentsDir, seqDir, i, seqSize, 
					fragmentSize-5, fragmentSize, coverage)

# Gera arquivo de output
st = str(seqSize) + "-" + str(fragmentSize) + "-" + str(coverage)

acoSizeData = ""
scsSizeData = ""

# Vetor de dados com tamanho das soluções
acoSizeVector = []
scsSizeVector = []

# Vetor de dados com distancia das soluções
acoDistVector = []
scsDistVector = []

# Calcula as soluções e as escreve em um arquivo de texto
with open(resultsDir + str(st) + ".txt", "a+") as outputFile:
	# Lista os arquivos de fragmentos
	fragFiles = [ f for f in listdir(fragmentsDir) if isfile(join(fragmentsDir,f)) ]

	for frag in fragFiles:
		outputFile.write("\n-----------------------------------\n")
		outputFile.write("Execução " + frag)
		outputFile.write("\n-----------------------------------\n")

		scsS, scsD, pathTrees = scs_greedy.solve(fragmentsDir + frag, outputFile, seqDir + frag)
		acoS, acoD = aco_scs.solve(fragmentsDir + frag, outputFile, seqDir + frag, [])
		# Utilizando o greedy como entrada
		#acoS, acoD = aco_scs.solve(fragmentsDir + frag, outputFile, seqDir + frag, pathTrees[0])

		
		# Vetores com dados de tamanho
		acoSizeVector.append(abs((acoS - seqSize)) / seqSize)
		scsSizeVector.append(abs((scsS - seqSize)) /seqSize)
		
		# Vetores com dados de distancia
		acoDistVector.append(acoD)
		scsDistVector.append(scsD)
		
		acoSizeData = acoSizeData + str(acoS) + " "
		scsSizeData = scsSizeData + str(scsS) + " "

# Escreve as soluções em um csv por garantia
with open(resultsDir + str(st) + ".csv", "a+") as outputFile:
	outputFile.write(acoSizeData + "\n")
	outputFile.write(scsSizeData + "\n")
	
# Arquivo de dados JSON
# Inicialização para caso arquivo esteja vazio.
data = json.loads('{"tam": {"aco": {"' + st + '":0}, "gdy": {"' + st + '":0}}, "dist":{"aco": {"' + st + '":0}, "gdy": {"' + st + '":0}}}')
try:
	with open(dataPath, "r") as dataFile:
		data = json.load(dataFile)
except ValueError:
	pass

# Escreve as médias de tamanho
tamData = data["tam"]
tamData["aco"][st] = np.mean(acoSizeVector)
tamData["gdy"][st] = np.mean(scsSizeVector)

# Escreve as médias de distância
distData = data["dist"]
distData["aco"][st] = np.mean(acoDistVector)
distData["gdy"][st] = np.mean(scsDistVector)

# Salva as médias da execução
with open(dataPath, 'w') as dataFile:
	json.dump(data, dataFile)

# Plota os graficos da execucao
ph.plotExecution(acoSizeVector, scsSizeVector, acoDistVector, scsDistVector,
				 resultsDir + str(st))

# Plota os graficos gerais
ph.plotAll(data, plotPath)

print("---- Fim Execução ----")


