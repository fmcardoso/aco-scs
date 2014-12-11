#!/usr/bin/python3
import generator
import aco_scs
import scs_greedy
import os
#import matplotlib.pyplot as plt

fragmentsDir = "gen/fragments/"
seqDir = "gen/sequences/"
resultsDir = "gen/results/"
seqSize = 1000
fragmentSize = 50

# Inicia os framentos
# Descomentar para gerar as sequências
for i in range(1, 10):
	generator.generate(fragmentsDir, seqDir, i, seqSize, fragmentSize)

from os import listdir
from os.path import isfile, join

# Gera arquivo de output
import time
ts = time.time()

import datetime
st = str(seqSize) + "-" + str(fragmentSize) #datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

acoData = ""
scsData = ""

acoVector = []
scsVector = []

csvFileName = "results/csvFile"

# Remove o arquivo de saída caso exista
os.remove(resultsDir + str(st) + ".txt") if os.path.exists(resultsDir + str(st) + ".txt") else None

with open(resultsDir + str(st) + ".txt", "a") as outputFile:
	# Lista os arquivos de fragmentos
	fragFiles = [ f for f in listdir(fragmentsDir) if isfile(join(fragmentsDir,f)) ]

	for frag in fragFiles:
		outputFile.write("\n-----------------------------------\n")
		outputFile.write("Execução " + frag)
		outputFile.write("\n-----------------------------------\n")
		acoS = aco_scs.solve(fragmentsDir + frag, outputFile)
		scsS = scs_greedy.solve(fragmentsDir + frag, outputFile)
		acoVector.append(acoS / seqSize)
		scsVector.append(scsS /seqSize)
		acoData = acoData + str(acoS) + " "
		scsData = scsData + str(scsS) + " "


with open(resultsDir + str(st) + ".csv", "a") as outputFile:
	outputFile.write(acoData + "\n")
	outputFile.write(scsData + "\n")

#plt.plot(acoVector, linewidth=2)
#plt.plot(scsVector, linewidth=2)
#plt.ylabel('Resultado/Tamanho Original')
#plt.xlabel('Tamanho Sequências')
#plt.savefig(resultsDir + str(st) + ".png")


