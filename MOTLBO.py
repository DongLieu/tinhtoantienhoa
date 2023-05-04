import numpy as np

def obj_func(x_jvk, y_jvu, d_vu, d_v, q ):
    tu = 0
    mau = 0
    

# so luong nut
n = 4

V_server = [1, 2, 3, 4]
V_switch = [4, 3, 2, 1]

# tap cac yeu cau VNF
F = [1, 2, 3]

# do che
d = {}
# do che may chu v chay VNF
d["v"] = []
# do che cua lien ket uv
d["uv"] = []

cost = {}
# chi phi kich hoat may chu v
cost["server"] = []
# chi phi cai dat VNF f_k tren server node v
cost["vnf"] = []

# tap cac yeu cau SFC
R = []
# nut nguon cua yeu cau R[j]
sn = []
# di qua cac nut de dap ung mot tap cac VNF da dc sap xep
F_Rj = []
# nut dich cua yeu cau R[j]
dn = []
w = {}
# bo nho
w["mem"] = []
# bang thong
w["wb"] = []
# cpu
w["cpu"] = []

m = {}
#bang thong toi da lien ket uv
m["bw"] = []
#bo nho toi da nut v
m["mem"] = []
#cpu toi da nut v
m["cpu"] = []
# so luong loai VNF toi da dc cai trong nut v
m["vnf"] = []

c = {}
#bang thong lien ket uv da sd
c["bw"] = []
#bo nho nut v da su dung
c["mem"] = []
#cpu nut v da su dung
c["cpu"] = []
# so luong loai VNF dc cai trong nut v
c["vnf"] = []