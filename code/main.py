
from MOTLBO import *
from MOEAD import *
from NSGA2 import *
from ISO import *

from graph_network import *
from graph_sfc_set import *

from Solution import *

miens = ["nsf"]#, "congent", "conus"]
vungs = ["center"]#, "rural", "uniform", "urban"]

requests = [10]#, 20, 30]

TIMELIMIT = 600

i_s = [2]

for mien in miens:
    for vung in vungs:

        for request in requests:
            for i in i_s:
                name_folder = mien+"_"+vung+"_"+str(i)
                # print("namefolder:{}|| request:{}|| ".format(name_folder, request))

                network = Network("./code/dataset/" + name_folder + "/input.txt")
                sfc_set = SFC_SET("./code/dataset/" + name_folder + "/request" + str(request) + ".txt")
                sfc_set.create_global_info(network)
                network.create_constraints_and_min_paths(sfc_set)

                sol_mau = Solution(network, sfc_set)
                sol_mau.name_folder_output = "./code/output/" + name_folder + "/request" + str(request)
             ############################-MOTLBO-##############################
                N_POP_MOTLBO = 100
                GEN_MOTLBO = 1000
                NUM_REMOVE_MOTLBO = 20

                motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, TIMELIMIT, NUM_REMOVE_MOTLBO, sol_mau)
                motlbo.initialize_population()
                # motlbo.run()

                # # ############################-MOEAD-##############################
                # N_POP_MOEAD = 20

                # GEN_MOEAD = 1000

                # moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, TIMELIMIT, name_folder, request)
                # moead.run()

                # # # ############################-NSGA2-##################################
                # N_POP_NSGA2 = 50
                # GEN_NSGA2 = 50
                # NUM_REMOVE_NSGA2 = 10

                # nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, TIMELIMIT, NUM_REMOVE_NSGA2, name_folder, request)
                # nsga2.run()

                # # ##########################-ISO-##################################
                # N_POP_ISO = 100
                # GEN_ISO = 1000
                # NUM_REMOVE_ISO = 40

                # iso = ISO(N_POP_ISO, GEN_ISO, TIMELIMIT, NUM_REMOVE_ISO, name_folder, request)
                # iso.run()
