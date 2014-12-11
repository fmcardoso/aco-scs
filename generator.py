#!/usr/bin/python3
import string
import random
import math
from random import randint

def generate(fragmentsDir, genomeDir, id, genomeSize = 1000, fragmentMinSize = 35, fragmentMaxSize = 50, coverage = 2):

    random.seed(1234 * id)
    # queremos uma cobertura de 10 vezes pelo menos
    numFragments = math.ceil((genomeSize / fragmentMinSize) * coverage)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Gera sequência
    genome = id_generator(genomeSize, "ACTG")

    # Escreve sequência
    file = open(genomeDir + str(id) + ".txt", "w+")
    file.write(genome)
    file.close()

    file = open(fragmentsDir + str(id) + ".txt", "w+")

    print("Tamanho Sequência Original:", len(genome))

    added = []

    for i in range (0, numFragments):
        index = randint(0, genomeSize - fragmentMaxSize)
        fragment = genome[index:index+randint(fragmentMinSize, fragmentMaxSize)]
        if (fragment not in added):
            file.write(fragment + "\n")
            added.append(fragment)
    file.close()
