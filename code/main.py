from MOTLBO import *
from MOEAD import *
from NSGA2 import *
from ISO import *

NAME_FOLDER = "nsf_uniform_1"
REQUEST = 10

#############################-MOTLBO-##############################
# N_POP_MOTLBO = 100
# GEN_MOTLBO = 100
# NUM_REMOVE_MOTLBO = 20

# motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, NUM_REMOVE_MOTLBO, NAME_FOLDER, REQUEST)
# motlbo.run()

############################-MOEAD-##############################
N_POP_MOEAD = 20
GEN_MOEAD = 1000

moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, NAME_FOLDER, REQUEST)
moead.run()

# ############################-MOEAD-##################################
# N_POP_NSGA2 = 100
# GEN_NSGA2 = 100
# NUM_REMOVE_NSGA2 = 40

# nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, NUM_REMOVE_NSGA2, NAME_FOLDER, REQUEST)
# nsga2.run()

##########################-ISO-##################################
# N_POP_ISO = 100
# GEN_ISO = 1000
# NUM_REMOVE_ISO = 40

# iso = ISO(N_POP_ISO, GEN_ISO, NUM_REMOVE_ISO, NAME_FOLDER, REQUEST)
# iso.run()



