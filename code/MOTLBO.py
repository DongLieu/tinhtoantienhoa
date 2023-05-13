from graph_link import *
from graph_network import *
from graph_node import *
from graph_sfc import *
from graph_sfc_set import *
from graph_vnf import *
import initSolution


name_folder = "nsf_uniform_1"

path_folder = "/Users/duongdong/tinhtoantienhoa/dataset/"

path_input = path_folder + name_folder + "/input.txt"

path_request10 = path_folder + name_folder + "/request10.txt"
path_request20 = path_folder + name_folder + "/request20.txt"
path_request30 = path_folder + name_folder + "/request30.txt"


net = Network(path_input)
sfc = SFC_SET(path_request10)

print(net.num_type_vnfs)
# x la cach dat:n so nguyen dau tuong ung so VNF cai tren server i||sum(VNF) tiep theo la cac VNF duoc cai dat
# y la cach dinh tuyen tu cach dat
# x, y = initSolution.oneSolution(net.num_nodes, )


