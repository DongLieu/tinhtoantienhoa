from MOTLBO import *
from MOEAD import *
from NSGA2 import *

NAME_FOLDER = "nsf_uniform_1"
REQUEST = 10

#############################-MOTLBO-##############################
# N_POP_MOTLBO = 100
# GEN_MOTLBO = 100
# NUM_REMOVE_MOTLBO = 20

# motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, NUM_REMOVE_MOTLBO, NAME_FOLDER, REQUEST)
# motlbo.run()

#############################-MOEAD-##############################
# N_POP_MOEAD = 20
# GEN_MOEAD = 1000

# moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, NAME_FOLDER, REQUEST)
# moead.run()

#############################-MOEAD-##################################
N_POP_NSGA2 = 100
GEN_NSGA2 = 100
NUM_REMOVE_NSGA2 = 40

nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, NUM_REMOVE_NSGA2, NAME_FOLDER, REQUEST)
nsga2.initialize_population()

nsga2.evaluate_population()
nsga2.classify_individuals_Pareto_front_layers()
nsga2.print_gen(0)

for i in nsga2.rank.values():
    print(i)

nsga2.selective()

print(len(nsga2.expulsion_set), nsga2.expulsion_set)
# sol1 =  nsga2.fitness[0]
# sol2 = nsga2.fitness[1]
# print(sol1)
# print(sol2)
# print(nsga2._distance_fit_sol(0, 1))


# for i in range(nsga2.n_pop):
#     print(i, nsga2.fitness[i])