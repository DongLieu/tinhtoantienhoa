from read_data import *

path_output = "./code/danhgia/danhgia/IGD.txt"
with open(path_output, 'w') as file:
    file.truncate(0)

with open(path_output, 'a') as file:
# Ghi các lời gọi print vào file
    print("{}:      {}                       ||   {}                   ||           {}".format("name_data", "MOTLBO", "NSGA2", "MOEAD"), file=file)
# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output

output_f = "./code/danhgia/pareto"

vung = ["cogent", "conus", "nsf"]

mien = ["center", "rural", "uniform", "urban"]

id = ["0", "1", "2", "3", "4"]

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output\cogent_center_0\
name_file10 = ["request10_MOTLBO.txt", "request10_NSGA2.txt", "request10_MOEAD.txt"]
name_file20 = ["request20_MOTLBO.txt", "request20_NSGA2.txt", "request20_MOEAD.txt"]
name_file30 = ["request30_MOTLBO.txt", "request30_NSGA2.txt", "request30_MOEAD.txt"]

def print_write(name, a, b, c):

    with open(path_output, 'a') as file:
        print(name,"   & ", "{:.4f}".format(a)," & ","{:.4f}".format(b)," & ","{:.4f}".format(c),"   \\\\", file=file)



def dominate(a, b):
    if a[0] <= b[0]:
        if a[1] <= b[1]:
            if a[2] <= b[2]:
                return True
    return False

def cocho_a_vaokhong(pareto, a):
    if a in pareto: return False
    for b in pareto:
        if dominate(b,a):
            return False
        
    return True


def pareto_front(rq):
    pareto = []
    motlbo = rq[0]
    nsga2 = rq[1]
    moead = rq[2]

    for a in moead:
        if cocho_a_vaokhong(pareto, a): pareto.append(a)

    for a in motlbo:
        if cocho_a_vaokhong(pareto, a): pareto.append(a)

    for a in nsga2:
        if cocho_a_vaokhong(pareto, a): pareto.append(a)
    
    return pareto

def d_min(a, p):
    min = 9999
    for i in a:
        check = sum((i[j]-p[j])**2 for j in range(3))
        if check < min: 
            min = check
    return min

def IGD(a, front_pareto):
    igd = 0
    for p in front_pareto:
        igd += d_min(a, p)
    
    igd = igd ** 0.5
    return igd/len(front_pareto)

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
                print(input)
                rq30.append(read_file(input)) 
            # igd10
            pf = pareto_front(rq10)
            igd_motlbo10 = IGD(rq10[0], pf)
            igd_nsga210 = IGD(rq10[1], pf)
            igd_moead10 = IGD(rq10[2], pf)
            # igd20
            pf = pareto_front(rq20)
            igd_motlbo20 = IGD(rq20[0], pf)
            igd_nsga220 = IGD(rq20[1], pf)
            igd_moead20 = IGD(rq20[2], pf)
            # igd30
            pf = pareto_front(rq30)
            igd_motlbo30 = IGD(rq30[0], pf)
            igd_nsga230 = IGD(rq30[1], pf)
            igd_moead30 = IGD(rq30[2], pf)
            # trung binh
            igd_0 = (igd_motlbo10 + igd_motlbo20 + igd_motlbo30)/3
            igd_1 = (igd_nsga210+igd_nsga220+igd_nsga230)/3
            igd_2 = (igd_moead10+igd_moead20+igd_moead30)/3
            name = vu +"\\_"+ mi +"\\_"+ i
            print_write(name, igd_0, igd_1, igd_2)




            

            
