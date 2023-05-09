import random

def khoitaomotcachdat(n, num_VNFs):
    x = []
    total_VNF = 0
    # khoi tao n server x[i]=0 sever i khong hoat dong
    # server x[i]=j sever i hoat dong va chay j VNF
    for i in range(n):
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
def dinhtuyen(x, R, requests):
    y = []
    return y
# tao mot loi giai
def oneSolution(n, f, R, requests):
    x = khoitaomotcachdat(n, f)
    y = dinhtuyen(x, R, requests)
    return x, y
