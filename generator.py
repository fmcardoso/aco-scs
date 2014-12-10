#!/usr/bin/python3
import string
import random
from random import randint

def generate(fragmentsDir, genomeDir, id, genomeSize, fragmentSize):

    random.seed(1234 * id)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    # Gera sequência
    genome = id_generator(genomeSize, "ACTG")

    # Escreve sequência
    file = open(genomeDir + str(id) + ".txt", "w")
    file.write(genome)
    file.close()

    file = open(fragmentsDir + str(id) + ".txt", "w")
    collection = [genome, genome, genome]

    print("Tamanho Sequência Original:", len(genome))

    added = []

    for i in collection:
        x = 0
        while (x < len(i)):
            t = randint(fragmentSize, fragmentSize*1.2)
            fragment = i[x:x+t]
            x=x+t

            if fragment not in added:
                file.write(fragment + "\n")
                added.append(fragment)
    file.close()
