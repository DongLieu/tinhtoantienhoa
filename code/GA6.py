import copy
from typing import List, Tuple
import time

from graph_network import *
from graph_sfc_set import *

from Solution import *

class GA6:
    def __init__(self, N, Gen, timelimit,w, num_remove, sol_mau:Solution) -> None:
        self.path_output = sol_mau.name_folder_output + "_Ga"+str(w[0])+".txt"
        self.network = sol_mau.net
        self.sfc_set = sol_mau.sfcs 
        self.w = w[1:]

        self.n_pop = N
        self.Gen = Gen
        self.num_remove = num_remove
        self.CR = 0.5
        self.time = timelimit

        self.pop = []
        self.fitness = []
        self.top_fitness = []   
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
            # chon loc
            self.selective()
            # prin
            self.print_gen(gen)
            # sinh san
            self.reproductionss()
            # tinh gia tri ham muc tieu
            self.evaluate_population()

            current_time = time.time()  # Lấy thời gian hiện tại
            elapsed_time = current_time - start_time  # Tính thời gian đã trôi qua
            if elapsed_time >= self.time:  # Kiểm tra nếu đã đạt đến thời gian kết thúc (ví dụ: 600 giây - 10 phút)
                break  # Thoát khỏi vòng lặp
            
            if self.khongthaydoi():
                break
    def khongthaydoi(self):
        khacnhaukhong = 0
        for sol1 in self.top_fitness:
            for sol2 in self.top_fitness:
                if self._obj_func(self.pop[sol1]) != self._obj_func(self.pop[sol2]):
                    print("k bang")
                    return False
        return True

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
        for solution in range(self.n_pop):
            fit = self._obj_func(self.pop[solution])
            fitniss_sol = sum(fit[i]*self.w[i] for i in range(3))
            fitniss_tmp.append([solution, fitniss_sol])
        self.fitness = fitniss_tmp

    # chon loc
    def selective(self):
        sorted_fit = sorted(self.fitness, key=lambda x: x[1], reverse=True)
        self.expulsion_set = [sol_id[0] for sol_id in sorted_fit[:self.num_remove]]
        self.top_fitness = [sol[0] for sol in sorted_fit[self.n_pop - 10:self.n_pop]]
        
    # sinh san
    def reproductionss(self):
        childs = []

        # lai ghep
        childs_tmp = []
        dad_used = []
        for dad1 in self.top_fitness:
            dad_used.append(dad1)
            for dad2 in range(self.n_pop):
                if dad2 in self.expulsion_set:continue
                if dad2 in dad_used:continue
                if dad2 in self.top_fitness:
                    sols, suc = self._laighep(dad1, dad2)
                    if suc:
                        childs_tmp = childs_tmp + sols
                else:
                    random_laighep = random.random()
                    if random_laighep > self.CR:
                        continue

                    sols, suc = self._laighep(dad1, dad2)
                    if suc:
                        childs_tmp = childs_tmp + sols
        if len(childs_tmp) > self.num_remove:
            for i in range(self.num_remove - 10):
                element_to_choice = random.choice(childs_tmp)
                childs.append(element_to_choice)
        else: childs = childs_tmp
        # dot bien
        sol_add = self.num_remove - len(childs)
        while(sol_add > 0):
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
                    sol_add -=1
                else:
                    del new_netw
                    del new_sfc_set
        i = 0
        for sol_change in self.expulsion_set:
            self.pop[sol_change] = childs[i]
            i += 1

    def print_gen(self, gen):
        with open(self.path_output, 'a') as file:
            # Ghi các lời gọi print vào file
            print("Gen: {}".format(gen + 1), file=file)
            for sol in self.top_fitness:
                print("     {}".format(self._obj_func(self.pop[sol])), file=file)
            print("", file=file)

    def _sol_in_pop(self, new_sol: Solution)->bool:
        for sol in self.pop:
            if new_sol.x == sol.x:
                return True
        return False
    
    def _laighep(self, dad1, dad2)->Tuple[List[Solution], bool]:
        x_dad1 = self.pop[dad1].x
        x_dad2 = self.pop[dad2].x
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