import copy
from typing import Tuple
from tqdm import tqdm

from graph_network import *
from graph_sfc_set import *

from Solution import *

class MOEAD:
    def __init__(self, N, Gen, name_folder, request:int) -> None:
        self.path_output = "/Users/duongdong/tinhtoantienhoa/code/output/" + name_folder + "/request" + str(request) + "_MOEAD.txt"

        self.network = Network("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/input.txt")
        self.sfc_set = SFC_SET("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/request" + str(request) + ".txt")
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints(self.sfc_set)
        
        self.n_pop = N
        self.Gen = Gen
        self.num_nei = 3
        self.CR = 0.8

        self.weight = []
        self.B = []

        self.pop = []
        self.fitness = []
        self.z = [1, 1, 1]

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
        # khoi tao w 
        self.initialization_weight()
        # tinh cac nei 
        self.neighboring_Solutions()
        # khoi tao
        self.initialize_population()
        #  tinh gia tri ham muc tieu va z
        self.evaluate_population()
        for gen in tqdm(range(self.Gen)):
            # chon ngau nhien ca the trong quan the de sinh san
            rand_sol = random.randint(0, self.n_pop - 1)
            # sinh san tu ca the duoc chon(laighep-dotbien)
            new_sol, ok = self.reproductionss(rand_sol)
            if not ok:
                with open(self.path_output, 'a') as file:
                # Ghi các lời gọi print vào file
                    print("Gen: {}".format(gen + 1), file=file)
                    print("     continue", file=file)
                    print("", file=file)
                continue

            sol_neis = self.B[rand_sol]
            for sol_nei in sol_neis:
                self.new_sol_is_good_to_update(sol_nei, new_sol)
            self.print_the_result_in_generation(gen)
            
            
    def initialization_weight(self):
        w = []
        evenly = [1/3, 1/3, 1/3]
        delay = [0.9000000, 0.050000000, 0.05000000]
        costSV = [0.0500000, 0.90000000, 0.050000000]
        costVNF = [0.05000000, 0.05000000, 0.9000000]
        w.append(evenly)
        w.append(delay)
        w.append(costSV)
        w.append(costVNF)

        for i in range(self.n_pop - len(w)):
            w.append(self._random_vector_w())

        self.weight = w

    def neighboring_Solutions(self):
        for w1 in range(self.n_pop):
            from_w1 = []
            for w2 in range(self.n_pop):
                # Tính tổng bình phương của hiệu các tọa độ tương ứng
                squared_diff =(self.weight[w1][0] - self.weight[w2][0])**2 + (self.weight[w1][1] - self.weight[w2][1])**2 + (self.weight[w1][2] - self.weight[w2][2])**2 
                # Lấy căn bậc hai của tổng bình phương
                distance = squared_diff ** 0.5
                tmp = [w2, distance]
                from_w1.append(tmp)

            form_w1_nei = sorted(from_w1, key=lambda x: x[1])
            nei_w1 = [nei[0] for nei in form_w1_nei[:self.num_nei]]
            self.B.append(nei_w1)
            
                        
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
        for sol in range(self.n_pop):
            fit_sol =  self._obj_func(self.pop[sol])
            self.update_of_reference_point_z(fit_sol)

            FV = sum(x * y for x, y in zip(fit_sol, self.weight[sol]))

            fitniss_tmp.append(FV)
        
        self.fitness = fitniss_tmp
    # tinh gia tri z
    def update_of_reference_point_z(self, fit_sol):
        for i in range(len(self.z)):
            if fit_sol[i] <= self.z[i]:
                self.z[i] = fit_sol[i]


    def reproductionss(self, sol_id)-> Tuple[Solution, bool]:
        random_laighep = random.random()

        if random_laighep < self.CR:
            # lai ghep
            return self._laighep(sol_id)
        else:
            # dot bien
            return self._dotbien(sol_id)
    
    def new_sol_is_good_to_update(self, sol_id, sol_new: Solution):
        fitness = self._obj_func(sol_new)
        self.update_of_reference_point_z(fitness)

        weight = self.weight[sol_id]
        result = sum(x * y for x, y in zip(fitness, weight))

        if result < self.fitness[sol_id]:
            self.fitness[sol_id] = result
            self.pop[sol_id] = sol_new

    def print_the_result_in_generation(self, gen):
        with open(self.path_output, 'a') as file:
                # Ghi các lời gọi print vào file
                print("Gen: {}".format(gen + 1), file=file)
                for sol_id in range(self.n_pop):
                    # weights = self.weight[sol_id]
                    # rounded_weights = [round(w, 5) for w in weights]
                    print("     fitness:{} | w: {}".format(self.fitness[sol_id], self.weight[sol_id]), file=file)
                print("", file=file)

        return
    
    def _random_vector_w(self):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1 - x)
        z = 1 - x - y
        return [x, y, z]
    
    def _dotbien(self, sol_id)-> Tuple[Solution, bool]:
        sol_dad = self.pop[sol_id]
        num_nodes = len(sol_dad.x_vnf)

        i = 0
        while(i<10):
            x = copy.deepcopy(sol_dad.x)
            i += 1

            id_vnf_hientai = random.randint(num_nodes, len(x) - 1)
            type_vnf_hientai = x[id_vnf_hientai]

            type_vnf_dotbien = random.randint(0, self.network.num_type_vnfs - 1)
            if type_vnf_dotbien != type_vnf_hientai:
                x[id_vnf_hientai] = type_vnf_dotbien

                new_netw = copy.deepcopy(self.network)
                new_sfc_set = copy.deepcopy(self.sfc_set)

                y = Solution(new_netw, new_sfc_set)
                y.x = x
                y.tinh_x_vnf()
                success = y.kichhoatnode_dinhtuyen()
                if success:
                    return y, True
                else:
                    del new_netw
                    del new_sfc_set
        
        return None, False
    
    def _laighep(self, sol_id)-> Tuple[Solution, bool]:

        return None, False
