import copy
from typing import Tuple
from tqdm import tqdm


from graph_link import *
from graph_network import *
from graph_node import *
from graph_sfc import *
from graph_sfc_set import *
from graph_vnf import *

from Solution import *
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
        
        self.need_improve = []
        self.dominant_set = []
        self.expulsion_set = []

        self.quansat = 0

    def run(self):
        # khoi tao
        self.initialize_population()
        # tinh gia tri ham muc tieu
        self.evaluate_population()
        # trung sol
        self.trung_sol()
        # sap xep, tim ra top_finess va ca the yeu
        self.good_finess_and_expulsion()
        for gen in tqdm(range(self.Gen)):
            # day
            self.teaching_phase()
            # hoc
            self.learning_phase()
            # loai bo va them vao ca the moi
            self.remove_phase()
            # dinh tuyen, tinh gia tri
            self.evaluate_population()
            # trung sol
            self.trung_sol()
            # sap xep, tim ra top_finess va ca the yeu
            self.good_finess_and_expulsion()

            for good_fitness in self.dominant_set:
                if sum(self.fitness[good_fitness]) < sum(self.fitness[self.quansat]):
                    self.quansat = good_fitness
            
            with open('output.txt', 'a') as file:
                # Ghi các lời gọi print vào file
                if self.quansat in self.need_improve:
                    print("llllllllllllllllllll")

                print("Good: {}||ID: {} || x: {}".format(sum(self.fitness[self.quansat]),self.quansat,  self.pop[self.quansat].x_vnf), file = file)
                print("Gen: {}::::len_fitnis={}||len-pop={}".format(gen + 1, len(self.fitness), len(self.pop)), file=file)
                for good_fitness in self.dominant_set:
                    print("{}: {}".format(sum(self.fitness[good_fitness]), self.fitness[good_fitness]), file=file)
                print("", file=file)  # In một dòng trống
                
    # Ham muc tieu:
    def _obj_func(self,sol: Solution):
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

    # chon ra ca the khong bi thong tri boi ca the khac lam teacher
    def good_finess_and_expulsion(self):
        need_improve_tmp = []
        for sol1_id in range(0, self.n_pop):
            for sol2_id in range(0 ,self.n_pop):
                if sol1_id == sol2_id:
                    continue
                if self.fitness[sol1_id][0] >= self.fitness[sol2_id][0] and self.fitness[sol1_id][1] >= self.fitness[sol2_id][1] and self.fitness[sol1_id][2] >= self.fitness[sol2_id][2]:
                    if self.fitness[sol1_id] == self.fitness[sol2_id]:
                        while(1):
                            print("sol1 = sol2")
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
                                    self.pop[sol1_id] = init
                                    break
                                else:
                                    del new_net
                                    del new_sfc
                    else:
                        if self.quansat == sol1_id:
                            print("quansat id = {}|| x = {}".format(sol1_id, self.pop[sol1_id].x))
                            print("fitness_quan sat =", self.fitness[self.quansat])
                            print("sol2 id : {}|| x = {}".format(sol2_id, self.pop[sol2_id].x))
                            print("fitness sol2=", self.fitness[sol2_id])

                        need_improve_tmp.append(sol1_id)
                        break

        self.need_improve = need_improve_tmp

        dominant_set_tmp = []
        for sol_id in range(self.n_pop):
            if sol_id in self.need_improve:
                continue
            else:
                dominant_set_tmp.append(sol_id)

        self.dominant_set = dominant_set_tmp
        
        fitniss_lose = []
        for sol_ex in self.need_improve:
            tmp = []
            tmp.append(sol_ex)
            total_fitniss = sum(self.fitness[sol_ex])
            tmp.append(total_fitniss)
            fitniss_lose.append(tmp)

        sorted_lose = sorted(fitniss_lose, key=lambda x: x[1], reverse=True)
        self.expulsion_set = [sol_lose[0] for sol_lose in sorted_lose[:self.num_remove]]


    # teaching_phase()
    def teaching_phase(self):
        for teacher in self.dominant_set:
            for student in self.need_improve:
                if student in self.expulsion_set:
                    continue
                else:
                    stu = self.pop[student]
                    tea = self.pop[teacher]

                    new_student, success = self._teacher_teaching_student(tea, stu)
                    if success:
                        if self._sol_in_pop(new_student):
                            continue
                        else:
                            # kiem tra xem co tot hon student hien tai ko
                            yes = self._thaythe(stu, new_student)
                            if yes:
                                if self.quansat == student:
                                    print("thay doi o tech: id:", self.quansat)
                                    print("x1:", self.pop[student].x)
                    
                                stu = new_student

                                if self.quansat == student:
                                    print("x2:", self.pop[student].x)

                  

        
    def learning_phase(self):
        for student1 in self.need_improve:
            if student1 in self.expulsion_set:
                    continue
            for student2 in self.need_improve:
                if student1 in self.expulsion_set or student1 == student2:
                    continue
                else:
                    stu1 = self.pop[student1]
                    stu2 = self.pop[student2]

                    r = np.random.rand()
                    if r > 0.5:
                        stu_new, success = self._teacher_teaching_student(stu1, stu2)
                        if success:
                            if self._sol_in_pop(stu_new):
                                continue
                            else:
                                # kiem tra xem co tot hon student hien tai ko
                                yes = self._thaythe(stu1, stu_new)
                                if yes:
                                    if self.quansat == student1:
                                        print("thay doi o lear id:", self.quansat)
                                        print("x1:", self.pop[student1].x)
                    
                                    stu1 = stu_new
                                    if self.quansat == student1:
                                        print("x2:", self.pop[student1].x)


        
    # loai bo va them vao ca the moi
    def remove_phase(self):
        for sol in self.expulsion_set:
            if self.quansat == sol:
                print("loi sieu to")
            while(1):
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
                        self.pop[sol] = init
                        break
                    else:
                        del new_net
                        del new_sfc
                    
    

    def _teacher_teaching_student(self, teacher: Solution, student: Solution) -> Tuple[Solution, bool]:
        x_teacher = teacher.x
        x_student = student.x
        num_nodes = len(teacher.x_vnf)
        diem_cat = random.randint(1, num_nodes - 1)

        new_netw = copy.deepcopy(self.network)
        new_sfc_set = copy.deepcopy(self.sfc_set)
        
        new_student = Solution(new_netw, new_sfc_set)

        x = x_student[:diem_cat] + x_teacher[diem_cat:num_nodes]
        num_vnf_student = sum(x_student[:diem_cat])
        num_vnf_teacher = sum(x_teacher[:diem_cat])
        
        x = x + x_student[num_nodes:num_nodes + num_vnf_student]
        x = x + x_teacher[num_nodes + num_vnf_teacher: len(x_teacher)]

        sum_check = sum(x[:num_nodes])
        if sum_check != len(x) - num_nodes:
            print("lai ra mot ca the moi khong dung duoc")
            return new_student, False
        else:
            new_student.x = x
            new_student.tinh_x_vnf()
            success = new_student.kichhoatnode_dinhtuyen()
            if success:
                return new_student, True
            else:
                # print("khong kich hoat dc")
                return new_student, False
            
    def _thaythe(self, student: Solution, new_student: Solution)->bool:
        fitnis_student = self._obj_func(student)
        fitnis_new_student = self._obj_func(new_student)

        if sum(fitnis_new_student) < sum(fitnis_student):
            return True
        else:
            return False
    def _sol_in_pop(self, new_sol: Solution)->bool:
        for sol in self.pop:
            if new_sol.x == sol.x:
                return True
        
        return False
    def trung_sol(self):
        for sol1 in range(0, len(self.pop)):
            for sol2 in range(sol1 +1 ,len(self.pop)):
                if self.fitness[sol1] == self.fitness[sol2]:
                     print("trung lap == tung lap")
                     while(1):
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
                                self.pop[sol1] = init
                                self.fitness[sol1] = self._obj_func(init)
                                break
                            else:
                                del new_net
                                del new_sfc




        
# NAME_FOLDER = "nsf_uniform_1"

# PATH_FOLDER = "/Users/duongdong/tinhtoantienhoa/dataset/"

# path_input = PATH_FOLDER + NAME_FOLDER + "/input.txt"

# path_request10 = PATH_FOLDER + NAME_FOLDER + "/request10.txt"
# path_request20 = PATH_FOLDER + NAME_FOLDER + "/request20.txt"
# path_request30 = PATH_FOLDER + NAME_FOLDER + "/request30.txt"

# net = Network(path_input)
# sfc = SFC_SET(path_request10)
# sfc.create_global_info(net)
# net.create_constraints(sfc)

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
# # print("     x:")
# x = c.x 
# print(c.x)

# new_net = copy.deepcopy(net)
# new_sfc = copy.deepcopy(sfc)
# init = Solution(new_net, new_sfc)

# init.x = x
# init.tinh_x_vnf()
# init.kichhoatnode_dinhtuyen()
# print(init.x)
# for sol in catherandom:
#     print(init.x == sol.x )

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

