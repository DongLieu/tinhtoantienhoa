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


net = Network(path_input)
sfc = SFC_SET(path_request10)

sfc.create_global_info(net)

# net.visualize
# print(sfc.num_sfc)
# print(net.num_servers)
# print(net.server_ids)
# print(net.num_type_vnfs)
sol=Solution.Solution(net, sfc)
sol._khoitao_nhaunhien_motcachdat()
# print(sol.sfcs.sfc_set[0])
print(sol.x)
print(sol.x_vnf)
print(sol.vnf_x)

# print(y)


# print(net.adj)


# print()
# x la cach dat:n so nguyen dau tuong ung so VNF cai tren server i||sum(VNF) tiep theo la cac VNF duoc cai dat
# y la cach dinh tuyen tu cach dat
# x, y = initSolution.oneSolution(net.num_nodes, )


