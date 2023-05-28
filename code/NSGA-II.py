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

     # Ham muc tieu:
    def _obj_func(self,sol: Solution):
        fitness = []
        fitness.append(sol.delay_servers_and_links_use/(sol.max_delay_links + sol.max_delay_servers))
        fitness.append(sol.cost_servers_use/sol.max_cost_servers)
        fitness.append(sol.cost_vnfs_use/sol.max_cost_vnfs)

        return fitness
    
    def run(self):
        self.initialize_population()
        self.evaluate_population()
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

    def _sol_in_pop(self, new_sol: Solution)->bool:
        for sol in self.pop:
            if new_sol.x == sol.x:
                return True
        return False
    
    #  tinh gia tri ham muc tieu cho moi pop[i]
    def evaluate_population(self):
        fitniss_tmp = []
        for solution in self.pop:
            fitniss_sol =  self._obj_func(solution)
            fitniss_tmp.append(fitniss_sol)
        
        self.fitness = fitniss_tmp
