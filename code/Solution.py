import random
from collections import deque

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
        
        self.vnf_requests = []
        self._search_vnf_requests()

        #khi dinh tuyen moi tinh toan 
        # dinh tuyen
        self.delay_servers_and_links_use = 0
        # dat-ok
        self.cost_servers_use = 0
        # dat-ok
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
        self.x = x
        self.tinh_x_vnf()
        

    def tinh_x_vnf(self):
        top = self.net.num_nodes

        for node in range(self.net.num_nodes):
            tmp = []
            if self.x[node] == 0:
                self.x_vnf[node] = []
                continue
            else:
                
                self.x_vnf[node] = self.x[top:top + self.x[node]]
                top += self.x[node]
        self._tinh_vnf_x()
        
    def _tinh_vnf_x(self):
        for i in range(self.net.num_type_vnfs):
            tmp_vnf_x = []
            for j,k in self.x_vnf.items():
                if i in k:
                    tmp_vnf_x.append(j)

            self.vnf_x[i] = tmp_vnf_x

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
                        continue
                    else:
                        # print("sv {} khong the cai dat vnf type {}.".format(id, vnf) )
                        return False
                # chi phi cai dat vnf 
                self.cost_vnfs_use += self.net.N[id].total_installed_vnf_cost
        return True

    def kichhoatnode_dinhtuyen(self)->bool:
        success = self.x_has_vnf_in_vnf_request()
        if not success:
            # print("x khong co vnf request")
            return success

        success = self._kichhoatNodes()
        if not success:
            # print("cannot install vnf")
            return success

        self._dinhtuyen() 
        return True
       
    def _dinhtuyen(self):
        for sfc in self.sfcs.sfc_set:
            dinhtuyen_tmp_node = dict()
            queue = deque()
            for i in sfc.vnf_list:
                queue.append(i)

            node_current = sfc.source
            node_destination = sfc.destination
            if node_current in self.net.server_ids:
                self.delay_servers_and_links_use += self.net.N[node_current].delay
            
            dinhtuyen_tmp_node[node_current] = -1
            # duyet tu vnf dau
            while queue:
                vnf_top = queue.popleft()  
                nodes_co_vnf_top = self.vnf_x[vnf_top]
                
                node_continue = nodes_co_vnf_top[0]
                for node in nodes_co_vnf_top:
                    if self.net.min_delay_local_tsps[node_current][node_continue] > self.net.min_delay_local_tsps[node_current][node]:
                        node_continue = node
                
                self.delay_servers_and_links_use += self.net.min_delay_local_tsps[node_current][node_continue]

                node_current = node_continue

                dinhtuyen_tmp_node[node_current] = vnf_top

            self.delay_servers_and_links_use += self.net.min_delay_local_tsps[node_current][node_destination]
            dinhtuyen_tmp_node[node_destination] = -1

            self.y[sfc.id] = dinhtuyen_tmp_node
        
    def _search_vnf_requests(self):
        for sfc in self.sfcs.sfc_set:
            for vnf in sfc.vnf_list:
                if vnf in self.vnf_requests:
                    continue
                else:
                    self.vnf_requests.append(vnf)
                    if len(self.vnf_requests) == self.net.num_type_vnfs:
                        return

    def x_has_vnf_in_vnf_request(self) -> bool:

        for vnf_type, nodes in self.vnf_x.items():
            if nodes == []:
                if vnf_type in self.vnf_requests:
                    return False
        
        return True

