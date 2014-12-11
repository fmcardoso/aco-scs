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
from cProfile import label

ts = time.time()

seqSize = 1000
fragmentSize = 60
coverage = 10

fragmentsDir = "gen/fragments/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"
seqDir = "gen/sequences/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"
resultsDir = "gen/results/" + datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y') + "/"

# Cria as pastas caso não existam
if not os.path.exists(os.path.dirname(fragmentsDir)):
	os.makedirs(os.path.dirname(fragmentsDir))
if not os.path.exists(os.path.dirname(seqDir)):
	os.makedirs(os.path.dirname(seqDir))
if not os.path.exists(os.path.dirname(resultsDir)):
	os.makedirs(os.path.dirname(resultsDir))

# Inicia os framentos
# Descomentar para gerar as sequências
for i in range(1, 10):
	generator.generate(fragmentsDir, seqDir, i, seqSize,
		fragmentSize-15, fragmentSize, coverage)

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

with open(resultsDir + str(st) + ".txt", "a+") as outputFile:
	# Lista os arquivos de fragmentos
	fragFiles = [ f for f in listdir(fragmentsDir) if isfile(join(fragmentsDir,f)) ]

	for frag in fragFiles:
		outputFile.write("\n-----------------------------------\n")
		outputFile.write("Execução " + frag)
		outputFile.write("\n-----------------------------------\n")

		acoS, acoD = aco_scs.solve(fragmentsDir + frag, outputFile, seqDir + frag)
		scsS, scsD = scs_greedy.solve(fragmentsDir + frag, outputFile, seqDir + frag)
		
		# Vetores com dados de tamanho
		acoSizeVector.append(abs((acoS - seqSize)) / seqSize)
		scsSizeVector.append(abs((scsS - seqSize)) /seqSize)
		
		# Vetores com dados de distancia
		acoDistVector.append(acoD)
		scsDistVector.append(scsD)
		
		acoSizeData = acoSizeData + str(acoS) + " "
		scsSizeData = scsSizeData + str(scsS) + " "


with open(resultsDir + str(st) + ".csv", "a+") as outputFile:
	outputFile.write(acoSizeData + "\n")
	outputFile.write(scsSizeData + "\n")

# Plota grafico de tamanhos
plt.figure(1)
plt.plot(acoSizeVector, linewidth=2, label = "Nosso")
plt.plot(scsSizeVector, linewidth=2, label = "Inimigo")
plt.legend(loc=2);
plt.ylabel('Disparidade do Tamanho')
plt.xlabel('Tamanho Sequências')
plt.savefig(resultsDir + str(st) + "-tam.png")

# Plota grafico de distância de edição
plt.figure(2)
plt.plot(acoDistVector, linewidth=2, label = "Nosso")
plt.plot(scsDistVector, linewidth=2, label = "Inimigo")
plt.legend(loc=2);
plt.ylabel('Distância de Edição')
plt.xlabel('Tamanho Sequências')
plt.savefig(resultsDir + str(st) + "-dist.png")


print("---- Fim Execução ----")


