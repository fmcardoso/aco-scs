#!/usr/bin/python3
import string
import random
from random import randint

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

file = open("fragments.txt", "w")

genome = id_generator(1000, "ACTG")
collection = [genome, genome, genome]

print(genome)

for i in collection:
  x = 0
  while (x < len(i)):
    t = randint(25,50)
    fragment = i[x:x+t]
    x = x+t
    file.write(fragment + "\n")
file.close()
