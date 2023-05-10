from graph_link import *
from graph_network import *
from graph_node import *
from graph_sfc import *
from graph_sfc_set import *
from graph_vnf import *

name_folder = "nsf_uniform_1"

path_folder = "/Users/duongdong/tinhtoantienhoa/dataset/"

path_input = path_folder + name_folder + "/input.txt"

path_request10 = path_folder + name_folder + "/request10.txt"
path_request20 = path_folder + name_folder + "/request20.txt"
path_request30 = path_folder + name_folder + "/request30.txt"

# f: so luong VNF
# l: so luong VNF toi da trong 1 nut SV
# n: so luong nut
# V_nodes: id, delay, costSV(= -1 la nut PNF), costVNF1,2,3... 
# m: so luong canh 
# E_links:u, v ,delay
# f, l, n, V_nodes, m, E_links = input.read_input(name_folder)
print(path_input)

# # R so luong request moi requests[i] co :bw,mem,cpu,u,v,k,VNFs...
# R, requests = input.read_request10(name_folder)

# x, y = initSolution.oneSolution(n, f, R, requests)
