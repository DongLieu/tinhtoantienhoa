import copy

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


catherandom = []
while(1):
    new_net = copy.deepcopy(net)
    new_sfc = copy.deepcopy(sfc)
    init = Solution(new_net, new_sfc)
    init.init_random()
    print(init.x_vnf)
    suc = init._kichhoatNodes()

    if suc:
        catherandom.append(init)
        break
    else:
        del new_net
        del new_sfc

# print("ok")
c = catherandom[0]
print("=================")

print(c.vnf_requests)
print(c.vnf_x)
print(c.x_has_vnf_in_vnf_request())
if c.x_has_vnf_in_vnf_request():
    c._dinhtuyen()
    print(c.y)

# for id, node in net.N.items():
#     print(id)
# nei = net.find_all_neighbor_by_id(2)
# print(nei)
# print(net.L[str(0) + '-' + str(1)].delay)
# d = dict()
# print(net.min_delay_local_tsps[0])
# d[1] = [1, 2, 3]
# d[2] = [1, 2, 31]

# c = dict()
# c[1] = d

# print(c)
# c._dinhtuyen()


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
    def obj_func(sol: Solution):
        fitness = []
        fitness.append(sol.delay_servers_and_links_use/(sol.max_delay_links + sol.max_delay_servers))
        fitness.append(sol.cost_servers_use/sol.max_cost_servers)
        fitness.append(sol.cost_vnfs_use/sol.max_cost_vnfs)

        return fitness
    # Khoi tao quan the
    def initialize_population(self):
        while(len(self.pop) != self.n_pop):
            new_netw = copy.deepcopy(self.network)
            new_sfc_set = copy.deepcopy(self.sfc_set)
            init = Solution(new_netw, new_sfc_set)
            init.init_random()
            suc = init._kichhoatNodes()
            if suc:
                self.pop.append(init)
                del new_netw
                del new_sfc_set
            else:
                del new_netw
                del new_sfc_set
    # kich hoat node, dinhtuyen, tinh gia tri ham muc tieu cho moi pop[i]
    def evaluate_population(self):
        return
    # chon ra ca the khong bi thong tri boi ca the khac lam teacher
    def top_finess_and_expulsion(self):
        return
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
        # dinh tuyen, tinh gia tri
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

        


