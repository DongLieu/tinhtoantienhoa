import random

def _khoitaomotcachdat(num_nodes, num_VNFs):
    x = []
    total_VNF = 0
    # khoi tao n server x[i]=0 sever i khong hoat dong
    # server x[i]=j sever i hoat dong va chay j VNF
    for i in range(num_nodes):
        tmp = random.randint(0, num_VNFs)
        total_VNF += tmp
        x.append(tmp)

    # chon VNF hoat dong ngau nhien
    for i in range(total_VNF):
        tmp = random.randint(0, num_VNFs)
        x.append(tmp)

    return x

# voi cach dat do, dinh tuyen theo yeu cua
# su dung giai thuat tham lam y:
# y sn -> dn: nut nguon den nut dich qua cac VNF cua nut nao
def _dinhtuyen(x, R, requests):
    y = []
    return y
# tao mot loi giai
def oneSolution(num_nodes, num_VNFs, num_requests, requests):
    x = _khoitaomotcachdat(num_nodes, num_VNFs)
    y = _dinhtuyen(x, num_requests, requests)
    return x, y
