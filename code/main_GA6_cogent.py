
from GA6 import *


from graph_network import *
from graph_sfc_set import *

from Solution import *

miens = ["cogent"]
vungs = ["center"]#"center" 3,4

requests = [10, 20, 30]

TIMELIMIT = 600

i_s = [0,1,2, 3, 4]

weights = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [0.4, 0.3, 0.3],
    [0.3, 0.4, 0.3],
    [0.3, 0.3, 0.4],
]

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
             ############################-GA6-##############################
                N_POP = 100
                GEN = 100
                NUM_REMOVE = 20
                for i in range(len(weights)):
                    w = [(i+1)] + weights[i]
                    ga = GA6(N_POP, GEN,TIMELIMIT ,w, NUM_REMOVE, sol_mau)
                    ga.run()

                




