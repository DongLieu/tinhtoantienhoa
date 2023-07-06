import copy
from typing import Tuple
# from tqdm import tqdm
import time

from graph_network import *
from graph_sfc_set import *

from Solution import *
class MOTLBO:
    def __init__(self, N, Gen, time, num_remove, name_folder, request:int) -> None:
        self.path_output = "/Users/duongdong/tinhtoantienhoa/code/output/" + name_folder + "/request" + str(request) + "_MOTLBO.txt"

        self.network = Network("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/input.txt")
        self.sfc_set = SFC_SET("/Users/duongdong/tinhtoantienhoa/code/dataset/" + name_folder + "/request" + str(request) + ".txt")
        self.sfc_set.create_global_info(self.network)
        self.network.create_constraints_and_min_paths(self.sfc_set)

        self.n_pop = N
        self.Gen = Gen
        self.num_remove = num_remove
        self.time = time

        self.pop = []
        self.fitness = []

        self.teacher = []
        self.teacher_fitness = []
        
        self.need_improve = []
        self.dominant_set = []
        self.expulsion_set = []

        self.trungsol = []
        self.removetrung = []

    def run(self):
        with open(self.path_output, 'w') as file:
            file.truncate(0)

        # khoi tao
        self.initialize_population()
        # tinh gia tri ham muc tieu
        self.evaluate_population()
        # sap xep, tim ra top_finess va ca the yeu
        self.good_finess_and_expulsion()
        # thoi gian bat dau
        start_time = time.time() 
        gen = 0
        while True:
            gen += 1
        # for gen in tqdm(range(self.Gen)):
            # day
            self.teaching_phase()
            # hoc
            self.learning_phase()
            # hoi thao
            self.seminar_phase()
            # loai bo va them vao ca the moi
            self.remove_phase()
            # dinh tuyen, tinh gia tri
            self.evaluate_population()
            # sap xep, tim ra top_finess va ca the yeu
            self.good_finess_and_expulsion()
            
            self.print_gen(gen)

            current_time = time.time()  # Lấy thời gian hiện tại
            elapsed_time = current_time - start_time  # Tính thời gian đã trôi qua
            if elapsed_time >= self.time:  # Kiểm tra nếu đã đạt đến thời gian kết thúc (ví dụ: 600 giây - 10 phút)
                break  # Thoát khỏi vòng lặp
                
    # Ham muc tieu:
    def _obj_func(self,sol: Solution):
        fitness = []
        fitness.append(sol.delay_servers_and_links_use/(sol.max_delay_links + sol.max_delay_servers))
        fitness.append(sol.cost_servers_use/sol.max_cost_servers)
        fitness.append(sol.cost_vnfs_use/sol.max_cost_vnfs)

        return fitness
    
    # print
    def print_gen(self,gen):
        with open(self.path_output, 'a') as file:
            # Ghi các lời gọi print vào file
            print("Gen: {}".format(gen), file=file)
            for good_fitness in self.dominant_set:
                print("{}".format(self.fitness[good_fitness]), file=file)
            print("", file=file)  # In một dòng trống

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
        fitniss_tmp = []
        for solution in self.pop:
            fitniss_sol =  self._obj_func(solution)
            fitniss_tmp.append(fitniss_sol)
        
        self.fitness = fitniss_tmp

    # chon ra ca the khong bi thong tri boi ca the khac lam teacher
    def good_finess_and_expulsion(self):
        self.trungsol = []
        self.removetrung = []

        pareto_obj = []
        for sol1_id in range(0, self.n_pop):
            for sol2_id in range(0 ,self.n_pop):
                if sol1_id == sol2_id:
                    continue
                 # neu sol1 bi sol2 dominates
                if self._dominates(sol1_id, sol2_id):  
                    break
                else:
                    if sol2_id == self.n_pop - 1:
                        pareto_obj.append(sol1_id)

        self.dominant_set = pareto_obj
        
        fitniss_lose = []
        for sol_ex in range(self.n_pop):
            if sol_ex in self.dominant_set: continue
            if sol_ex in self.removetrung: continue
            
            total_fitniss = sum(self.fitness[sol_ex])
            fitniss_lose.append([sol_ex, total_fitniss])

        sorted_lose = sorted(fitniss_lose, key=lambda x: x[1], reverse=True)
        add_remove = [sol_lose[0] for sol_lose in sorted_lose[:self.num_remove - len(self.removetrung)]]

        self.expulsion_set = add_remove + self.removetrung

        ni_set = []
        for conlai in range(self.n_pop):
            if conlai in self.expulsion_set:continue

            if conlai in self.dominant_set:continue

            ni_set.append(conlai)

        self.need_improve = ni_set


    # teaching_phase()
    def teaching_phase(self):
        for teacher in self.dominant_set:
            for student in self.need_improve:
                stu = self.pop[student]
                tea = self.pop[teacher]

                new_student, success = self._teacher_teaching_student(tea, stu)
                if success:
                    # kiem tra xem co tot hon student hien tai ko
                    yes = self._thaythe(stu, new_student)
                    if yes:
                        stu = new_student
        
    def learning_phase(self):
        for student1 in self.need_improve:
            for student2 in self.need_improve:
                if student1 == student2:continue

                stu1 = self.pop[student1]
                stu2 = self.pop[student2]

                r = np.random.rand()
                if r > 0.5:
                    stu_new, success = self._teacher_teaching_student(stu1, stu2)
                    if success:
                        # kiem tra xem co tot hon student hien tai ko
                        yes = self._thaythe(stu1, stu_new)
                        if yes:
                            stu1 = stu_new                              
    # hoithao
    def seminar_phase(self):
        for teacher1 in self.dominant_set:
            for teacher2 in self.dominant_set:
                if teacher1 == teacher2:  continue

                tea1 = self.pop[teacher1]
                tea2 = self.pop[teacher2]

                new_tea, success = self._teacher_teaching_student(tea1, tea2)
                if success:
                    # kiem tra xem co tot hon teacher hien tai ko
                    yes = self._thaythe(tea1, new_tea)
                    if yes:
                        tea1 = new_tea
                                
    # loai bo va them vao ca the moi
    def remove_phase(self):
        for sol in self.expulsion_set:
            while(1):
                new_net = copy.deepcopy(self.network)
                new_sfc = copy.deepcopy(self.sfc_set)
                init = Solution(new_net, new_sfc)

                init.init_random()
                suc = init.kichhoatnode_dinhtuyen()
                if suc:
                    self.pop[sol] = init
                    break
                else:
                    del new_net
                    del new_sfc

    def _teacher_teaching_student(self, teacher: Solution, student: Solution) -> Tuple[Solution, bool]:
        x_teacher = copy.deepcopy(teacher.x)
        x_student = copy.deepcopy(student.x)
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

    def _dominates(self, sol1, sol2) ->bool:
        #True  neu sol2 dominates sol1
        if self.fitness[sol1][0] >= self.fitness[sol2][0] and\
            self.fitness[sol1][1] >= self.fitness[sol2][1] and\
            self.fitness[sol1][2] >= self.fitness[sol2][2]:
            #sol2 dominates yeu
            if self.fitness[sol1] == self.fitness[sol2]:
                if (sol1 in self.trungsol) or (sol2 in self.trungsol):
                    if sol1 in self.trungsol:
                        if not (sol2 in self.removetrung): self.removetrung = self.removetrung + [sol2]
                    else:
                        if not (sol1 in self.removetrung): self.removetrung = self.removetrung + [sol1]

                    return True
                else:
                    self.trungsol = self.trungsol + [sol1] 
                    self.removetrung = self.removetrung + [sol2]
                    return False
            #sol2 dominates hoan toan
            else:
                return True
        else:
            return False


