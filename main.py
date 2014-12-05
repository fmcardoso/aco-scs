#!/usr/bin/python3
import generator
import aco_scs

fragmentsDir = "gen/fragments/"
seqDir = "gen/sequences/"
resultsDir = "gen/results/"

# Inicia os framentos
# Descomentar para gerar as sequências
for i in range(1, 10):
	generator.generate(fragmentsDir, seqDir, i)



from os import listdir
from os.path import isfile, join

# Gera arquivo de output
import time
ts = time.time()

import datetime
st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')

with open(resultsDir + str(st) + ".txt", "a") as outputFile:
	# Lista os arquivos de fragmentos
	fragFiles = [ f for f in listdir(fragmentsDir) if isfile(join(fragmentsDir,f)) ]

	for frag in fragFiles:
		outputFile.write("\n-----------------------------------\n")
		outputFile.write("Execução " + frag)
		outputFile.write("\n-----------------------------------\n")
		aco_scs.solve(fragmentsDir + frag, outputFile)
