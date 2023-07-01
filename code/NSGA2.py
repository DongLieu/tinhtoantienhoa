import copy
from typing import List, Tuple
# from tqdm import tqdm
import math
import time

from graph_network import *
from graph_sfc_set import *

from Solution import *

class NSGA2:
    def __init__(self, N, Gen, timelimit, num_remove, name_folder, request:int) -> None:
        self.path_output = "./code/output/" + name_folder + "/request" + str(request) + "_NSGA2.txt"

        self.network = Network("./code/dataset/" + name_folder + "/input.txt")
        self.sfc_set = SFC_SET("./code/dataset/" + name_folder + "/request" + str(request) + ".txt")
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints_and_min_paths(self.sfc_set)
        
        self.n_pop = N
        self.Gen = Gen
        self.num_remove = num_remove
        self.time = timelimit

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
        # thoi gian bat dau
        start_time = time.time() 
        gen = 0
        while True:
            gen += 1
        # for gen in tqdm(range(self.Gen)):
            self.rank = dict()
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

            current_time = time.time()  # Lấy thời gian hiện tại
            elapsed_time = current_time - start_time  # Tính thời gian đã trôi qua
            if elapsed_time >= self.time:  # Kiểm tra nếu đã đạt đến thời gian kết thúc (ví dụ: 600 giây - 10 phút)
                break  # Thoát khỏi vòng lặp
            else:
                print("Gen: ", gen)


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
    
        expulsion_add = self._chooce_on_crowding_distance(rank_choce, num_expulsion)

        tmp_expulsion = tmp_expulsion + expulsion_add
        self.expulsion_set = tmp_expulsion
    
    def print_gen(self, gen):
        with open(self.path_output, 'a') as file:
            # Ghi các lời gọi print vào file
            print("Gen: {}".format(gen + 1), file=file)
            for sol in self.rank[0]:
                print("     id:{} |Total fit:{} |fitness:{}".format(sol, sum(self.fitness[sol]), self.fitness[sol]), file=file)
            print("", file=file)


    def _chooce_on_crowding_distance(self, rank_chooce, num_expulsion):
        expulsion = []

        if num_expulsion == 0:
            return expulsion
        # bien xa nhat
        z = [-1, -1, -1]
        for sol_id in self.rank[rank_chooce]:
            if (self.fitness[sol_id][0] <  self.fitness[z[0]][0]) or (z[0] == -1):
                z[0] = sol_id
            if (self.fitness[sol_id][1] <  self.fitness[z[1]][1]) or (z[1] == -1):
                z[1] = sol_id
            if (self.fitness[sol_id][2] <  self.fitness[z[2]][2]) or (z[2] == -1):
                z[2] = sol_id
        giulai = copy.deepcopy(z)

        check = num_expulsion - len(self.rank[rank_chooce]) + 3
        if check > 0:
            for i in range(check):
                element_to_remove = random.choice(z)
                expulsion.append(element_to_remove)
                z.remove(element_to_remove)
            for sol_id1 in self.rank[rank_chooce]:
                if sol_id1 in giulai: continue
                expulsion.append(sol_id1)
            return expulsion

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
        childs = []
        childs_tmp = []

        dad_used = []
        # lai ghep
        for dad1 in self.rank[0]:
            dad_used.append(dad1)
            for dad2 in range(self.n_pop):
                if dad2 in self.expulsion_set:continue
                if dad2 in dad_used:continue
                sols_new, ok = self._laighep(dad1, dad2)
                if ok:
                    childs_tmp = childs_tmp + sols_new
        
        if len(childs_tmp) > self.num_remove:
            for i in range(self.num_remove - 10):
                element_to_choice = random.choice(childs_tmp)
                childs.append(element_to_choice)
        else: childs = childs_tmp

        del childs_tmp

        # dotbien
        sol_can_bo_sung = len(self.expulsion_set) - len(childs)
        while(sol_can_bo_sung > 0):
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
                    childs.append(init)
                    sol_can_bo_sung -=1
                else:
                    del new_netw
                    del new_sfc_set
        i = 0
        for sol_change in self.expulsion_set:
            # print(sol_change)
            self.pop[sol_change] = childs[i]
            i += 1

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
    def _laighep(self, dad1, dad2)->Tuple[List[Solution], bool]:
        x_dad1 = copy.deepcopy(self.pop[dad1].x)
        x_dad2 = copy.deepcopy(self.pop[dad2].x)
        num_nodes = len(self.pop[dad1].x_vnf)
        diem_cat = random.randint(1, num_nodes - 1)

        x1 = x_dad1[:diem_cat] + x_dad2[diem_cat:num_nodes]
        x2 = x_dad2[:diem_cat] + x_dad1[diem_cat:num_nodes]

        num_vnf_dad1 = sum(x_dad1[:diem_cat])
        num_vnf_dad2 = sum(x_dad2[:diem_cat])

        x1 = x1 + x_dad1[num_nodes:num_nodes + num_vnf_dad1]
        x1 = x1 + x_dad2[num_nodes+num_vnf_dad2:len(x_dad2)]

        x2 = x2 + x_dad2[num_nodes:num_nodes+num_vnf_dad2]
        x2 = x2  +x_dad1[num_nodes+num_vnf_dad1:len(x_dad1)]
        
        new_netw1 = copy.deepcopy(self.network)
        new_sfc_set1 = copy.deepcopy(self.sfc_set)
        new_netw2 = copy.deepcopy(self.network)
        new_sfc_set2 = copy.deepcopy(self.sfc_set)
        
        new_sol1 = Solution(new_netw1, new_sfc_set1)
        new_sol2 = Solution(new_netw2, new_sfc_set2)

        new_sol1.x = x1
        new_sol2.x = x2

        new_sol1.tinh_x_vnf()
        new_sol2.tinh_x_vnf()

        suc1 = new_sol1.kichhoatnode_dinhtuyen()
        suc2 = new_sol2.kichhoatnode_dinhtuyen()

        sols = []
        if suc1:sols.append(new_sol1)
        if suc2: sols.append(new_sol2)

        return sols, (suc1 or suc2)

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