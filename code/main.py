import threading
import copy

from MOTLBO import *
from MOEAD import *
from NSGA2 import *
from ISO import *

NAME_FOLDER = "nsf_uniform_0"
REQUEST = 10
TIMELIMIT = 600

#############################-MOTLBO-##############################
N_POP_MOTLBO = 100
GEN_MOTLBO = 1000
NUM_REMOVE_MOTLBO = 20

motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, TIMELIMIT, NUM_REMOVE_MOTLBO, NAME_FOLDER, REQUEST)
motlbo.run()

# motlbo.initialize_population()

# print(motlbo.pop[0].x)
# # motlbo.pop[0].x = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [3, 2], 9: [], 10: [], 11: [], 12: [], 13: [1, 4, 0]}

# x = [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 2, 1, 4, 0]

# new_netw = copy.deepcopy(motlbo.network)
# new_sfc_set = copy.deepcopy(motlbo.sfc_set)

# new_student = Solution(new_netw, new_sfc_set)

# new_student.x = x

# new_student.tinh_x_vnf()
# print(new_student.x_vnf)
# success = new_student.kichhoatnode_dinhtuyen()

# print(success)

# motlbo.pop[0] = new_student

# motlbo.evaluate_population()

# print(motlbo.pop[0].x)
# print(motlbo.fitness[0])

# motlbo.good_finess_and_expulsion()



# # ############################-MOEAD-##############################
# N_POP_MOEAD = 20
# GEN_MOEAD = 1000

# moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, TIMELIMIT, NAME_FOLDER, REQUEST)
# moead.run()

# # # ############################-NSGA2-##################################
# N_POP_NSGA2 = 50
# GEN_NSGA2 = 50
# NUM_REMOVE_NSGA2 = 10

# nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, TIMELIMIT, NUM_REMOVE_NSGA2, NAME_FOLDER, REQUEST)
# nsga2.run()

# # ##########################-ISO-##################################
# N_POP_ISO = 100
# GEN_ISO = 1000
# NUM_REMOVE_ISO = 40

# iso = ISO(N_POP_ISO, GEN_ISO, TIMELIMIT, NUM_REMOVE_ISO, NAME_FOLDER, REQUEST)
# iso.run()

# ##########################-ALL-##################################

# # Tạo các đối tượng Thread cho từng hàm
# thread1 = threading.Thread(target=motlbo.run)
# thread2 = threading.Thread(target=moead.run)
# thread3 = threading.Thread(target=nsga2.run)
# thread4 = threading.Thread(target=iso.run)
# # Khởi động các luồng thực thi
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()

# # Đợi cho tất cả các luồng kết thúc
# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()