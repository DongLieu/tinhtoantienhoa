from read_data import *

path_output = "./code/danhgia/danhgia/C_metric.txt"
with open(path_output, 'w') as file:
    file.truncate(0)
# with open(path_output, 'a') as file:
# # Ghi các lời gọi print vào file
#     print("Datasets & $\delta$(MOTLBO/MOEAD) & $\delta$(MOEAD/NSGA-II) & $\delta$(NSGA-II/MOTLBO)  \\\ [0.5ex] ", file=file)

def print_write(name, a, b, c):
    with open(path_output, 'a') as file:
        # print(name,"   & ", "{:.4f}".format(a)," & ","{:.4f}".format(b)," & ","{:.4f}".format(c),"   \\\\", file=file)
        print("{:.4f}".format(a)," & ","{:.4f}".format(b)," & ","{:.4f}".format(c), file=file)

output_f = "./code/danhgia/pareto"

vung = ["cogent", "conus", "nsf"]

mien = ["center", "rural", "uniform", "urban"]

id = ["0", "1", "2", "3", "4"]

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output\cogent_center_0\
name_file10 = ["request10_MOTLBO.txt", "request10_NSGA2.txt", "request10_MOEAD.txt"]
name_file20 = ["request20_MOTLBO.txt", "request20_NSGA2.txt", "request20_MOEAD.txt"]
name_file30 = ["request30_MOTLBO.txt", "request30_NSGA2.txt", "request30_MOEAD.txt"]

def dominate(a, b):
    if a[0] <= b[0]:
        if a[1] <= b[1]:
            if a[2] <= b[2]:
                return True
    return False

def tonjtaitronga(a, i):
    for j in a:
        if dominate(j,i):
            return True

def Cmetric(a, b):
    c = 0
    for i in b:
        if tonjtaitronga(a, i): c+=1

    return c/len(b)


def Dmetric(a,b):

    return Cmetric(a, b) - Cmetric(b, a)

for vu in vung:
    for mi in mien:
        for i in id:
            path_begin = output_f +"/"+ vu +"_"+ mi +"_"+ i +"/"

            # request 10: motlbo;nsga2;moead
            rq10 = []
            for bo10 in name_file10:
                input = path_begin+ bo10
                rq10.append(read_file(input)) 
            # request 20: motlbo;nsga2;moead
            rq20 = []
            for bo20 in name_file20:
                input = path_begin+ bo20
                rq20.append(read_file(input)) 
            # request 30: motlbo;nsga2;moead
            rq30 = []
            for bo30 in name_file30:
                input = path_begin+ bo30
                rq30.append(read_file(input)) 

            # motlbo/moead
            d10_1 = Dmetric(rq10[0], rq10[2])
            # moead/nsga2
            d10_2 = Dmetric(rq10[2], rq10[1])
            # nsga2/motlbo
            d10_3 = Dmetric(rq10[1], rq10[0])
            
            # motlbo/moead
            d20_1 = Dmetric(rq20[0], rq20[2])
            # moead/nsga2
            d20_2 = Dmetric(rq20[2], rq20[1])
            # nsga2/motlbo
            d20_3 = Dmetric(rq20[1], rq20[0])

            # motlbo/moead
            d30_1 = Dmetric(rq30[0], rq30[2])
            # moead/nsga2
            d30_2 = Dmetric(rq30[2], rq30[1])
            # nsga2/motlbo
            d30_3 = Dmetric(rq30[1], rq30[0])

            d1 = d10_1 + d20_1 + d30_1
            d1 = d1/3
            d2 = d10_2 + d20_2 + d30_2
            d2 = d2/3
            d3 = d10_3 + d20_3 + d30_3
            d3 = d3/3
            name = vu +"\\_"+ mi +"\\_"+ i
            print_write(name, d1, d2, d3)
