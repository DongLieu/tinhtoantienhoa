import input

name_folder = "nsf_urban_0"
# f: so luong VNF
# l: so luong VNF toi da trong 1 nut SV
# n: so luong nut
# V_nodes: id, delay, costSV(= -1 la nut PNF), costVNF1,2,3... 
# m: so luong canh 
# E_links:
f, l, n, V_nodes, m, E_links = input.read_input(name_folder)

# R so luong request moi requests[i] co :bw,mem,cpu,u,v,k,VNFs...
R, requests = input.read_request10(name_folder)

