import random
from queue import LifoQueue

from graph_network import *
from graph_sfc_set import *


class Solution():
    def __init__(self, net: Network, sfcs: SFC_SET) -> None:
        self.net = net
        self.sfcs = sfcs

        self.x = None
        self.y = dict()
        self.x_vnf = dict()
        self.vnf_x = dict()
        
        self.mem = float
        

    def _khoitao_nhaunhien_motcachdat(self):
        x = []
        # khoi tao n node x[i]=0 laf switch
        # server x[i] sever i hoat dong va chay x[i] VNF
        for i in range(self.net.num_nodes):
            if i in self.net.server_ids:
                tmp = random.randint(0, self.net.num_type_vnfs)
                x.append(tmp)
            else:
                x.append(0)


        # chon VNF hoat dong ngau nhien
        for i in range(len(x)):
            tmp_x_vnf =[]
            for j in range(x[i]):
                while(1):
                    tmp_type_vnf = random.randint(1, self.net.num_type_vnfs)
                    if tmp_type_vnf in tmp_x_vnf:
                        continue
                    else:
                        x.append(tmp_type_vnf)
                        tmp_x_vnf.append(tmp_type_vnf)
                        break

            self.x_vnf[i] = tmp_x_vnf
        # luu id sever in dict vnf_x
        for i in range(1,self.net.num_type_vnfs + 1):
            tmp_vnf_x = []
            for j,k in self.x_vnf.items():
                if i in k:
                    tmp_vnf_x.append(j)

            self.vnf_x[i] = tmp_vnf_x

        self.x = x

    # voi cach dat do, dinh tuyen theo yeu cua
    # su dung giai thuat tham lam y:
    # y sn -> dn: nut nguon den nut dich qua cac VNF cua nut nao
    # y : [sever][VNFs su dung]
    def _dinhtuyen(self):
        # ghi vao sfcs.sfc_set[i].path
        y = {}

        for sfc in self.sfcs.sfc_set:
            dinhtuyen_tmp = []
            stack_vnf = LifoQueue()
            for i in sfc.vnf_list:
                stack_vnf.put(i)

            node_start = sfc.source
            vnf_top = stack_vnf.get()

            while not stack_vnf.empty():
                # tim cho VNF
                if vnf_top in self.x_vnf[node_start]:
                    # tinh toan co du chi phi khong
                    if self.chi_phi_node_i_add_vnf_j():
                        # xuly them vnf vao bang thong
                        vnf_top = stack_vnf.get()
                else:
                    # tim nut lang rieng co vnf top
                    self.net.find_all_neighbor_by_id(node_start)



            y[sfc.id] = dinhtuyen_tmp

        
    def co_du_chi_phi_node_i_add_vnf_j(self)->bool:
        return False
