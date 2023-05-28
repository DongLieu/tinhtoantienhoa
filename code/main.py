from MOTLBO import *
from MOEAD import *
from NSGA2 import *

NAME_FOLDER = "nsf_uniform_1"
REQUEST = 10

N_POP = 100
GEN = 100
NUM_REMOVE = 20

# motlbo = MOTLBO(N_POP, GEN, NUM_REMOVE, NAME_FOLDER, REQUEST)
# motlbo.run()

# moead = MOEAD(N_POP, GEN, NAME_FOLDER, REQUEST)
# moead.run()

nsga2 = NSGA2(N_POP, GEN, NUM_REMOVE,NAME_FOLDER, REQUEST)
nsga2.initialize_population()

nsga2.pop[1] = nsga2.pop[0] 
nsga2.evaluate_population()

# print(nsga2.pop[0].x)
print(nsga2.fitness[0])
print(nsga2.fitness[1])
print(nsga2._trung_fit(0, 1))

