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

        #khi dinh tuyen moi tinh toan 
        self.delay_severs_use = 0
        self.delay_links_use = 0
        self.cost_servers_use = 0
        self.cost_vnfs_use = 0

# max delay server = tong vnfs request * max_delay_sever
        self.max_delay_servers = sfcs.max_delay_server
# max delay link = so request * (delaymax_qua_tatcac_nut)
        self.max_delay_links = net.max_delay_links * sfcs.total_required_vnf
# max_cost_sever = tong chi phi khi kich hoat tat ca server
        self.max_cost_servers = net.sum_cost_servers
# max cost vnfs = chi phi khi kich hoat taat ca vnfs treen tat ca server
        self.max_cost_vnfs = net.max_cost_vnfs

        
    def init_random(self):
        x = []
        for i in range(self.net.num_nodes):
            if i in self.net.server_ids:
                tmp = random.randint(0, self.net.N[i].num_vnfs_limit)
                x.append(tmp)
            else:
                x.append(0)

        for i in range(len(x)):
            tmp_x_vnf =[]
            for j in range(x[i]):
                while(1):
                    tmp_type_vnf = random.randint(0, self.net.num_type_vnfs - 1)
                    if tmp_type_vnf in tmp_x_vnf:
                        continue
                    else:
                        x.append(tmp_type_vnf)
                        tmp_x_vnf.append(tmp_type_vnf)
                        break

            self.x_vnf[i] = tmp_x_vnf

        for i in range(self.net.num_type_vnfs):
            tmp_vnf_x = []
            for j,k in self.x_vnf.items():
                if i in k:
                    tmp_vnf_x.append(j)

            self.vnf_x[i] = tmp_vnf_x
        self.x = x

    def _kichhoatNodes(self) -> bool:
        for id, vnfs in self.x_vnf.items():
            if self.net.N[id].type == 0 or vnfs == []:
                continue
            else:
                # tinh chi phi kich hoat sever node id:
                self.cost_servers_use += self.net.N[id].cost
                
                # set vnf from j vnfs
                for vnf in vnfs:
                    success = self.net.N[id].install_vnf(vnf)
                    if success:
                        # tinh chi phi cai dat vnf
                        
                        continue
                    else:
                        print("sv {} khong the cai dat vnf type {}.".format(id, vnf) )
                        return False
                        
                self.cost_vnfs_use += self.net.N[id].total_installed_vnf_cost
        return True

    def kichhoatnode_dinhtuyen(self):
        success = self._kichhoatNodes()
        if not success:
            print("cannot install vnf")

        success = self._dinhtuyen() 
        if not success:
            print("cannot dinh tuyen voi cach dat x")
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
