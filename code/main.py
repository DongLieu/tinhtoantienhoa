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
# moead.evaluate_population()

# print(moead.pop[0].x)
# sol,yes = moead._dotbien(0)
# if yes:
#     print(sol.x)
# else:
#     print(sol)
# # print(moead.B)
# print("------------")
# for i in moead.B:
#     print(i)
# print("------")
# for i in range(moead.n_pop):
#     print("fit={}|                 FV={}|          w={}| ".format(moead._obj_func(moead.pop[i]), moead.fitness[i], moead.weight[i]))


# import multiprocessing

# def function1():
#     # Thực hiện công việc của hàm 1

# def function2():
#     # Thực hiện công việc của hàm 2

# # Tạo các tiến trình (processes) cho từng hàm
# process1 = multiprocessing.Process(target=function1)
# process2 = multiprocessing.Process(target=function2)

# # Khởi động các tiến trình
# process1.start()
# process2.start()

# # Đợi cho tất cả các tiến trình hoàn thành
# process1.join()
# process2.join()

# # Tiếp tục thực hiện các công việc khác
