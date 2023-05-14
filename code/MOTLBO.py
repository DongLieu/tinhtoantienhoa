from graph_link import *
from graph_network import *
from graph_node import *
from graph_sfc import *
from graph_sfc_set import *
from graph_vnf import *
import Solution

name_folder = "nsf_uniform_1"
# name_folder = "nsf_urban_0"

path_folder = "/Users/duongdong/tinhtoantienhoa/dataset/"

path_input = path_folder + name_folder + "/input.txt"

path_request10 = path_folder + name_folder + "/request10.txt"
path_request20 = path_folder + name_folder + "/request20.txt"
path_request30 = path_folder + name_folder + "/request30.txt"

catherandom = []
while(1):
    net = Network(path_input)
    sfc = SFC_SET(path_request10)
    sfc.create_global_info(net)
    net.create_constraints(sfc)

    init = Solution.Solution(net, sfc)
    init.init_random()
    print(init.x_vnf)
    suc = init._kichhoatNodes()
    if suc:
        catherandom.append(init)
        break

print("ok")
c = catherandom[0]

print("===")
s = 0
# for id ,node in catherandom[0].net.N.items():
#     print(node.vnf_cost)
#     s += node.delay
    # print("id:{} cost: {}".format(id,node.cost))

print(c.cost_server/c.net.sum_cost_servers)
print(c.cost_vnf)
print(c.net.N[2])
# while(1):
#     initmotcathe.init_randam()
#     success = initmotcathe.kichhoatnode_dinhtuyen()
#     if success:
#         break



# print(sol.sfcs.capmax)
# print(sol.net.N[1].cpu_capacity)


# print(sol.x)
# print(sol.x_vnf)
# print(sol.vnf_x)

# print(y)


# print(net.adj)


# print()
# x la cach dat:n so nguyen dau tuong ung so VNF cai tren server i||sum(VNF) tiep theo la cac VNF duoc cai dat
# y la cach dinh tuyen tu cach dat
# x, y = initSolution.oneSolution(net.num_nodes, )


