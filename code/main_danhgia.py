from MOTLBO import *
from MOEAD import *
from NSGA2 import *


from graph_network import *
from graph_sfc_set import *

from Solution import *

TIMELIMIT = 600


name_folder = "nsf_urban_0"

request = 10

network = Network("./code/dataset/" + name_folder + "/input.txt")
sfc_set = SFC_SET("./code/dataset/" + name_folder + "/request" + str(request) + ".txt")
sfc_set.create_global_info(network)
network.create_constraints_and_min_paths(sfc_set)

sol_mau = Solution(network, sfc_set)
############################-MOTLBO-##############################
# sol_mau.name_folder_output = "./code/danhgia/lua_tham_so/motlbo/"
# N_POP_MOTLBO = 100
# GEN_MOTLBO = 1000
# NUM_REMOVE_MOTLBO = 20
# RATE_CROSS_MOTLBO = [0.5, 0.6, 0.7, 0.8, 0.9]

# for i in RATE_CROSS_MOTLBO:
#     motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, TIMELIMIT, NUM_REMOVE_MOTLBO, i, sol_mau)
#     motlbo.run()

# ############################-MOEAD-##############################
# sol_mau.name_folder_output = "./code/danhgia/lua_tham_so/moead/"
# N_POP_MOEAD = 10

# GEN_MOEAD = 1000
# K = 3

# moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, TIMELIMIT, K, sol_mau)
# moead.run()

# # ############################-NSGA2-##################################
sol_mau.name_folder_output = "./code/danhgia/lua_tham_so/nsga2/"
N_POP_NSGA2 = 100
GEN_NSGA2 = 50
NUM_REMOVE_NSGA2 = 20
RATE_CROSS_NSGA2 = [0.5, 0.6, 0.7, 0.8, 0.9]
RATE_MUTAION_NSGA2 = [0.5, 0.6, 0.7, 0.8, 0.9]

for i in RATE_CROSS_NSGA2:
    nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, TIMELIMIT, NUM_REMOVE_NSGA2, i, RATE_MUTAION_NSGA2, sol_mau)
    nsga2.run()
