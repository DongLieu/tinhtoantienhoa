from MOTLBO import *
from MOEAD import *

NAME_FOLDER = "nsf_uniform_1"
REQUEST = 10

N_POP = 20
GEN = 10000
NUM_REMOVE = 20

# motlbo = MOTLBO(N_POP, GEN, NUM_REMOVE, NAME_FOLDER, REQUEST)
# motlbo.run()

moead = MOEAD(N_POP, GEN, NAME_FOLDER, REQUEST)
moead.run()

# moead.initialization_weight()
# moead.neighboring_Solutions()
# moead.initialize_population()
# moead.evaluate_population

# sols,yes = moead._laighep(0)
# if yes:
#     print(yes)
#     for sol in sols:
#         print(sol.x)


