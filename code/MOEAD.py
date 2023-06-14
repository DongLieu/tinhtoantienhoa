import copy
from typing import List, Tuple
# from tqdm import tqdm
import time

from graph_network import *
from graph_sfc_set import *

from Solution import *

class MOEAD:
    def __init__(self, N, Gen, timelimit, name_folder, request:int) -> None:
        self.path_output = "/Users/duongdong/tinhtoantienhoa/code/output/" + name_folder + "/request" + str(request) + "_MOEAD.txt"

        self.network = Network("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/input.txt")
        self.sfc_set = SFC_SET("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/request" + str(request) + ".txt")
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints_and_min_paths(self.sfc_set)
        
        self.n_pop = N
        self.Gen = Gen
        self.num_nei = 3
        self.CR = 0.8
        self.time = timelimit

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
        # thoi gian bat dau
        start_time = time.time() 
        gen = 0
        while True:
            gen += 1
        # for gen in tqdm(range(self.Gen)):
            # chon ngau nhien ca the trong quan the de sinh san
            rand_sol = random.randint(0, self.n_pop - 1)
            # sinh san tu ca the duoc chon(laighep-dotbien)
            new_sols, ok = self.reproductionss(rand_sol)
            if not ok:
                
                with open(self.path_output, 'a') as file:
                # Ghi các lời gọi print vào file
                    print("Gen:new {}".format(gen), file=file)
                    print("     continue len = {}".format(len(new_sols)), file=file)
                    print("", file=file)

                current_time = time.time()  # Lấy thời gian hiện tại
                elapsed_time = current_time - start_time  # Tính thời gian đã trôi qua
                if elapsed_time >= self.time:  # Kiểm tra nếu đã đạt đến thời gian kết thúc (ví dụ: 600 giây - 10 phút)
                    break  # Thoát khỏi vòng lặp
                else:
                    continue
            else:
                for new_sol in new_sols:
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


    def reproductionss(self, sol_id)-> Tuple[List[Solution], bool]:
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
                print("Gen: {}".format(gen), file=file)
                for sol_id in range(self.n_pop):
                    # weights = self.weight[sol_id]
                    # rounded_weights = [round(w, 5) for w in weights]
                    print("     id: {}| fitness:{} | w: {}".format(sol_id,self.fitness[sol_id], self.weight[sol_id]), file=file)
                print("", file=file)

        return
    
    def _random_vector_w(self):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1 - x)
        z = 1 - x - y
        return [x, y, z]
    
    def _dotbien(self, sol_id)-> Tuple[List[Solution], bool]:
        num_sols = random.randint(1, self.n_pop)
        sol_sons = []
        i = 0
        while(i < num_sols):
            new_net = copy.deepcopy(self.network)
            new_sfc = copy.deepcopy(self.sfc_set)
            init = Solution(new_net, new_sfc)

            init.init_random()
            if self._sol_in_pop(init):
                del new_net
                del new_sfc
            else:
                suc = init.kichhoatnode_dinhtuyen()

                if suc:
                    i += 1
                    sol_sons.append(init)
                else:
                    del new_net
                    del new_sfc
        if len(sol_sons) != 0:
            return sol_sons, True
        
        return None, False
    
    def _laighep(self, sol_id)-> Tuple[List[Solution], bool]:
        neis = copy.deepcopy(self.B[sol_id])
        num_dad = len(neis)
        dads = []
        for nei in neis:
            sol = copy.deepcopy(self.pop[nei])
            dads.append(sol)

        numnode = len(dads[0].x_vnf)
        # ba diem cat
        diemcats = []
        khoangcachcat = int(numnode/num_dad)
        for i in range(1, num_dad):
            diemcats.append(i*khoangcachcat)
        x_dict = {}

        for diemcat in range (len(diemcats) + 1):
            x_diemcat = []
            for dad in dads:

                if diemcat == 0:
                    x_sv = dad.x[:diemcats[diemcat]]    
                    num_vnf = sum(x_sv)
                    vnf = dad.x[numnode: numnode+num_vnf]
                    x_diemcat.append([x_sv, vnf])

                elif diemcat == len(diemcats):
                    x_sv = dad.x[diemcats[diemcat - 1]: numnode]
                    num_vnf = sum(x_sv)

                    num_vnf_truoc = sum(dad.x[:diemcats[diemcat - 1]])
                    vnf = dad.x[numnode + num_vnf_truoc: numnode + num_vnf_truoc + num_vnf]
                    x_diemcat.append([x_sv, vnf])
                    

                else:
                    x_sv = dad.x[diemcats[diemcat - 1]: diemcats[diemcat]]
                    num_vnf = sum(x_sv)

                    num_vnf_truoc = sum(dad.x[:diemcats[diemcat - 1]])
                    vnf = dad.x[numnode + num_vnf_truoc: numnode + num_vnf_truoc + num_vnf]
                    x_diemcat.append([x_sv, vnf])
            
            x_dict[diemcat] = x_diemcat

        x_vnf = []
        for i in range(num_dad):
            x_tmp = []
            for j in range(num_dad):
                if i == j:
                    continue
                for k in range(num_dad):
                    if k == j or k == i:
                        continue
                    else:
                        x_tmp.append(x_dict[0][i])
                        x_tmp.append(x_dict[1][j])
                        x_tmp.append(x_dict[2][k])
                        x_vnf.append(x_tmp)
                        x_tmp = []

        x = []
        for sol_x in x_vnf:
            x_tpm = []
            x_tpm += (sol_x[0][0])
            x_tpm += (sol_x[1][0])
            x_tpm +=(sol_x[2][0])

            x_tpm+=(sol_x[0][1])
            x_tpm+=(sol_x[1][1])
            x_tpm+=(sol_x[2][1])

            x.append(x_tpm)

        new_sols = []
        for x_sol in x:
            new_net = copy.deepcopy(self.network)
            new_sfc = copy.deepcopy(self.sfc_set)
            init = Solution(new_net, new_sfc)

            init.x = x_sol
            if self._sol_in_pop(init):
                del new_net
                del new_sfc
            else:
                init.tinh_x_vnf()
                suc = init.kichhoatnode_dinhtuyen()
                if suc:
                    new_sols.append(init)
            
        if len(new_sols) != 0:
            return new_sols, True
        else:
            return new_sols, False
