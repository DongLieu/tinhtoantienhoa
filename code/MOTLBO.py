import copy
import json

from graph_link import *
from graph_network import *
from graph_node import *
from graph_sfc import *
from graph_sfc_set import *
from graph_vnf import *

from Solution import *

name_folder = "nsf_uniform_1"
# name_folder = "nsf_urban_0"

path_folder = "/Users/duongdong/tinhtoantienhoa/dataset/"

path_input = path_folder + name_folder + "/input.txt"

path_request10 = path_folder + name_folder + "/request10.txt"
path_request20 = path_folder + name_folder + "/request20.txt"
path_request30 = path_folder + name_folder + "/request30.txt"

net = Network(path_input)
sfc = SFC_SET(path_request10)
sfc.create_global_info(net)
net.create_constraints(sfc)

# catherandom = []

# while(1):
#     new_net = copy.deepcopy(net)
#     new_sfc = copy.deepcopy(sfc)
#     init = Solution(new_net, new_sfc)
#     init.init_random()
#     suc = init.kichhoatnode_dinhtuyen()

#     if suc:
#         print("=========")
#         print("Thanh cong")
#         catherandom.append(init)
#         del new_net
#         del new_sfc
#         break
#     else:
#         del new_net
#         del new_sfc


# c = catherandom[0]
# print("     x:")
# print(c.x)

# print("     y:")
# for key, value in c.y.items():
#     print(f'{key}: {value}')
# print(c.delay_servers_and_links_use/(c.max_delay_links+c.max_delay_servers))
# print(c.net.num_nodes)
# print("=================")

# new_net = copy.deepcopy(net)
# new_sfc = copy.deepcopy(sfc)
# init = Solution(new_net, new_sfc)
# init.x = [0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 3, 1, 0, 3, 4, 3, 0, 2, 1, 3, 0 , 2, 1 ]
# init.tinh_x_vnf()
# suc = init.kichhoatnode_dinhtuyen()
# if suc:
#     print("Thanh cong")
#     catherandom.append(init)
# else:
#     del new_net
#     del new_sfc

# print("     x:")
# print(init.x_vnf)
# print("     y:")
# for key, value in init.y.items():
#     print(f'{key}: {value}')
# print(init.delay_servers_and_links_use/(init.max_delay_links+init.max_delay_servers))

# print("==========")
# for id, link in init.net.L.items():
#     print(link)

# print("==========")  
# for id, node in init.net.N.items():
#     print(node)
class MOTLBO:
    def __init__(self, N, Gen, num_remove, path_input, path_request) -> None:
        self.network = Network(path_input)
        self.sfc_set = SFC_SET(path_request)
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints(self.sfc_set)

        self.n_pop = N
        self.Gen = Gen
        self.num_remove = num_remove

        self.pop = []
        self.fitness = []

        self.teacher = []
        self.teacher_fitness = []
        self.expulsion = []


    # Ham muc tieu:
    def obj_func(self,sol: Solution):
        fitness = []
        fitness.append(sol.delay_servers_and_links_use/(sol.max_delay_links + sol.max_delay_servers))
        fitness.append(sol.cost_servers_use/sol.max_cost_servers)
        fitness.append(sol.cost_vnfs_use/sol.max_cost_vnfs)

        return fitness
    # Khoi tao quan the, (kich hoat node, dinhtuyen cho moi ca the)
    def initialize_population(self):
        while(len(self.pop) != self.n_pop):
            new_netw = copy.deepcopy(self.network)
            new_sfc_set = copy.deepcopy(self.sfc_set)
            
            init = Solution(new_netw, new_sfc_set)
            init.init_random()

            suc = init.kichhoatnode_dinhtuyen()
            if suc:
                self.pop.append(init)
            else:
                del new_netw
                del new_sfc_set
    #  tinh gia tri ham muc tieu cho moi pop[i]
    def evaluate_population(self):
        for solution in self.pop:
            fitniss_sol =  self.obj_func(solution)
            self.fitness.append(fitniss_sol)

    # chon ra ca the khong bi thong tri boi ca the khac lam teacher
    def top_finess_and_expulsion(self):
        for sol1_id in range(self.N):
            for sol2_id in range(self.N):
                if self.fitness[sol1_id][0] >= self.fitness[sol2_id][0] and self.fitness[sol1_id][1] >= self.fitness[sol2_id][1] and self.fitness[sol1_id][2] >= self.fitness[sol2_id][2]:
                    self.expulsion.append(sol1_id)
            
    # teaching_phase()
    def teaching_phase(self):
        return
    def learning_phase(self):
        return
    # loai bo va them vao ca the moi
    def remove_phase(self):
        return
    
    def run(self):
        # khoi tao
        self.initialize_population()
        # tinh gia tri ham muc tieu
        self.evaluate_population()
        # sap xep, tim ra top_finess va ca the yeu
        self.top_finess_and_expulsion()
        for gen in range(self.Gen):
            # day
            self.teaching_phase()
            # hoc
            self.learning_phase()
            # loai bo va them vao ca the moi
            self.remove_phase()
            # dinh tuyen, tinh gia tri
            self.evaluate_population()
            # sap xep, tim ra top_finess va ca the yeu
            self.top_finess_and_expulsion()
            print("Gen:{} Delay:{} Cost_Server:{} Cost_VNF:{}".format(gen,self.teacher_fitness[0][0], self.teacher_fitness[1][1], self.teacher_fitness[2][2]))

        


