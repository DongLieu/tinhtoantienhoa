import copy
from typing import Tuple
from tqdm import tqdm
import math

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
            # Sắp xếp Các tầng Pareto front 
            self.classify_individuals_Pareto_front_layers()
            # print Keets qua
            self.print_gen(gen)
            # chon loc(chon cac ca the giu lai, cac ca the phai thay the)
            self.selective()
            # sinh san(cac ca the co rank=0 lai ghep voi nhau va rank = 1) 
            self.reproductionss()
            # tinh gia tri ham muc tieu
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
    
    # Tinh gia tri ham muc tieu cho moi pop[i]
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
        self._fast_nondominated_sort()

    def selective(self):
        # chon ra cac ca the khong tot
        tmp_expulsion = []
        found = 0

        count = 0
        rank_choce = -1
        num_expulsion = -1

        for rank in self.rank.keys():
            count += len(self.rank[rank])

            if (count > (self.n_pop - self.num_remove)) and (found == 0):
                rank_choce = rank
                num_expulsion = count - (self.n_pop - self.num_remove)
                found = 1
                continue

            if (count > self.num_remove) and (found == 1):
                tmp_expulsion = tmp_expulsion + self.rank[rank]
        print("rankchoce = ", rank_choce)
        print("num_exxx = ", num_expulsion)

        expulsion_add = self._chooce_on_crowding_distance(rank_choce, num_expulsion)

        tmp_expulsion = tmp_expulsion + expulsion_add
        self.expulsion_set = tmp_expulsion
    
    def print_gen(self, gen):
        with open(self.path_output, 'a') as file:
            # Ghi các lời gọi print vào file
            print("Gen: {}".format(gen + 1), file=file)
            for sol in self.rank[0]:
                print("     id:{} |fitness:{}".format(sol, self.fitness[sol]), file=file)
            print("", file=file)


    def _chooce_on_crowding_distance(self, rank_chooce, num_expulsion):
        expulsion = []

        if num_expulsion == 0:
            return expulsion
        
        z = [-1, -1, -1]
        for sol_id in self.rank[rank_chooce]:
            if (self.fitness[sol_id][0] <  self.fitness[z[0]][0]) or (z[0] == -1):
                z[0] = sol_id
            if (self.fitness[sol_id][1] <  self.fitness[z[1]][1]) or (z[1] == -1):
                z[1] = sol_id
            if (self.fitness[sol_id][2] <  self.fitness[z[2]][2]) or (z[2] == -1):
                z[2] = sol_id

        distances = []
        for sol_id1 in self.rank[rank_chooce]:
            if sol_id1 in z: continue

            min_1_id = -1
            min_2_id = -1
            min = 999
            for sol_id2 in self.rank[rank_chooce]:
                if sol_id1 == sol_id2:
                    continue

                dis = self._distance_fit_sol(sol_id1, sol_id2)
                if dis < min:
                    min_2_id = min_1_id

                    min = dis
                    min_1_id = sol_id2

            distance = self._distance_fit_sol(min_1_id, min_2_id)       
            distances.append([sol_id1, distance]) 

        sorted_lose = sorted(distances, key=lambda x: x[1])
        expulsion_set_add = [sol_lose[0] for sol_lose in sorted_lose[:num_expulsion]]
        expulsion = expulsion + expulsion_set_add

        return expulsion

        

        

                



                

        
    
    def reproductionss(self):
        return

    def _distance_fit_sol(self, sol1_id, sol2_id):
        a = sum((x-y)**2 for x,y in zip(self.fitness[sol1_id],self.fitness[sol2_id]))
        return math.sqrt(a)
        
    def _fast_nondominated_sort(self):
        # mảng lưu trữ số lượng cá thể không dominated
        dominated_count = [0] * self.n_pop

        for i in range(self.n_pop):
            i_tmp = []

            for j in range(self.n_pop):
                if i == j: continue

                if self._dominates(i, j):
                    # so ca the troi hon ca the i
                    dominated_count[i] += 1
                    i_tmp.append(j)
        # Xác định tầng Pareto front đầu tiên
        front = []
        for i in range(self.n_pop):
            if dominated_count[i] == 0:
                front.append(i)
                dominated_count[i] = -1
        # Lặp lại quá trình xác định các tầng Pareto front tiếp theo
        rank = 0
        while len(front) > 0:
            self.rank[rank] = front
            next_front = []
            for i in range(len(front)):
                for j in range(self.n_pop):
                    if dominated_count[j] > 0:
                        dominated_count[j] -= 1
                        if dominated_count[j] == 0:
                            next_front.append(j)
                            dominated_count[j] = -1
            front = next_front
            rank += 1
        
            
                    

    def _dominates(self, sol1, sol2) ->bool:
        #True  neu sol1 dominates sol2
        if self.fitness[sol1][0] >= self.fitness[sol2][0] and\
            self.fitness[sol1][1] >= self.fitness[sol2][1] and\
            self.fitness[sol1][2] >= self.fitness[sol2][2]:
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