
from MOTLBO import *
from MOEAD import *
from NSGA2 import *


from graph_network import *
from graph_sfc_set import *

from Solution import *

miens = ["conus"]#["cogent", "nsf" ,

vungs = ["uniform"]

requests = [30]

TIMELIMIT = 600

i_s = [1, 0, 3, 4]

for mien in miens:
    for vung in vungs:

        for request in requests:
            for i in i_s:
                name_folder = mien+"_"+vung+"_"+str(i)

                network = Network("./code/dataset/" + name_folder + "/input.txt")
                sfc_set = SFC_SET("./code/dataset/" + name_folder + "/request" + str(request) + ".txt")
                sfc_set.create_global_info(network)
                network.create_constraints_and_min_paths(sfc_set)

                sol_mau = Solution(network, sfc_set)
                sol_mau.name_folder_output = "./code/output/" + name_folder + "/request" + str(request)
            #  ############################-MOTLBO-##############################
            #     N_POP_MOTLBO = 100
            #     GEN_MOTLBO = 1000
            #     NUM_REMOVE_MOTLBO = 20
            #     RATE_CROSS_MOTLBO = 0.8

            #     motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, TIMELIMIT, NUM_REMOVE_MOTLBO, RATE_CROSS_MOTLBO, sol_mau)
            #     motlbo.run()

                # ############################-MOEAD-##############################
                N_POP_MOEAD = 20

                GEN_MOEAD = 1000
                K = 3

                moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, TIMELIMIT, K, sol_mau)
                moead.run()

                # # # ############################-NSGA2-##################################
                # N_POP_NSGA2 = 50
                # GEN_NSGA2 = 50
                # NUM_REMOVE_NSGA2 = 10
                # RATE_CROSS_NSGA2 = 0.8
                # RATE_MUTAION_NSGA2 = 0.1

                # nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, TIMELIMIT, NUM_REMOVE_NSGA2, RATE_CROSS_NSGA2, RATE_MUTAION_NSGA2, sol_mau)
                # nsga2.run()


