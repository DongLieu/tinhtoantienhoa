import copy
from typing import Tuple
from tqdm import tqdm

from graph_network import *
from graph_sfc_set import *

from Solution import *

class NSGA2:
    def __init__(self, N, Gen, num_remove, name_folder, request:int) -> None:
        self.path_output = "/Users/duongdong/tinhtoantienhoa/code/output/" + name_folder + "/request" + str(request) + "_NSGA2.txt"

        self.network = Network("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/input.txt")
        self.sfc_set = SFC_SET("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/request" + str(request) + ".txt")
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints(self.sfc_set)
        
        self.n_pop = N
        self.Gen = Gen
        self.num_remove = num_remove

        self.pop = []
        self.fitness = []
        self.rank = dict()
        self.expulsion_set = []

     # Ham muc tieu:
    def _obj_func(self,sol: Solution):
        fitness = []
        fitness.append(sol.delay_servers_and_links_use/(sol.max_delay_links + sol.max_delay_servers))
        fitness.append(sol.cost_servers_use/sol.max_cost_servers)
        fitness.append(sol.cost_vnfs_use/sol.max_cost_vnfs)

        return fitness
    
    def run(self):
        with open(self.path_output, 'w') as file:
            file.truncate(0)
        # khoi tao quan the
        self.initialize_population()
        # tinh gia tri ham muc tieu
        self.evaluate_population()
        for gen in range(self.Gen):
            # Sắp xếp không chủ quan: Sử dụng sắp xếp không chủ quan để phân 
            # loại các cá thể thành các tầng Pareto front. Các tầng Pareto front 
            # càng cao thì càng tốt.
            self.classify_individuals_Pareto_front_layers()
            # chon loc
            self.selective()
            # sinh san
            self.reproductionss()


    # Hàm tạo quần thể ban đầu
    def initialize_population(self):
        while(len(self.pop) != self.n_pop):
            new_netw = copy.deepcopy(self.network)
            new_sfc_set = copy.deepcopy(self.sfc_set)
            
            init = Solution(new_netw, new_sfc_set)
            init.init_random()
            
            if self._sol_in_pop(init):
                del new_netw
                del new_sfc_set
            else:
                suc = init.kichhoatnode_dinhtuyen()
                if suc:
                    self.pop.append(init)
                else:
                    del new_netw
                    del new_sfc_set
    
    #  tinh gia tri ham muc tieu cho moi pop[i]
    def evaluate_population(self):
        fitniss_tmp = []
        for solution in self.pop:
            fitniss_sol =  self._obj_func(solution)
            fitniss_tmp.append(fitniss_sol)
        self.fitness = fitniss_tmp

        def co_trung_fitness():
            for i in range(self.n_pop):
                for j in range(i+1, self.n_pop):
                    if self._trung_fit(i, j):
                        while(1):
                            new_netw = copy.deepcopy(self.network)
                            new_sfc_set = copy.deepcopy(self.sfc_set)
                            
                            init = Solution(new_netw, new_sfc_set)
                            init.init_random()
                            
                            if self._sol_in_pop(init):
                                del new_netw
                                del new_sfc_set
                            else:
                                suc = init.kichhoatnode_dinhtuyen()
                                if suc:
                                    self.pop[i] = init
                                    self.fitness[i] = self._obj_func(init)
                                    co_trung_fitness()
                                    return
                                else:
                                    del new_netw
                                    del new_sfc_set
        co_trung_fitness()



    def classify_individuals_Pareto_front_layers(self):
        rank0 =[]
        for i in range(self.n_pop):
            i_tmp = 0
            for j in range(self.n_pop):
                if i == j or (j in rank0): continue

                if self._dominates(i, j):
                    i_tmp = 1
                    break
            if i_tmp == 0:
                rank0.append(i)
        self.rank[0] = rank0

                    
    def _dominates(self, sol1, sol2) ->bool:
        #True  neu sol1 dominates sol2
        if self.fitness[sol1][0] <= self.fitness[sol2][0] and\
            self.fitness[sol1][1] <= self.fitness[sol2][1] and\
            self.fitness[sol1][2] <= self.fitness[sol2][2]:
            return True
        else:
            return False

    def _trung_fit(self, sol1, sol2)->bool:
        if self.fitness[sol1][0] == self.fitness[sol2][0] and\
            self.fitness[sol1][1] == self.fitness[sol2][1] and\
            self.fitness[sol1][2] == self.fitness[sol2][2]:
            return True
        else:
            return False

    def _sol_in_pop(self, new_sol: Solution)->bool:
        for sol in self.pop:
            if new_sol.x == sol.x:
                return True
        return False