from read_data import *

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output

output_f = "./code/danhgia/pareto"

vung = ["cogent"]#, "conus", "nsf"]

mien = ["center"]#, "rural", "uniform", "urban"]

id = ["0"]#, "1", "2", "3", "4"]

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output\cogent_center_0\
name_file10 = ["request10_Ga1.txt", "request10_Ga2.txt", "request10_Ga3.txt", "request10_Ga4.txt", "request10_Ga5.txt", "request10_Ga6.txt"]
name_file20 = ["request20_Ga1.txt", "request20_Ga2.txt", "request20_Ga3.txt", "request20_Ga4.txt", "request20_Ga5.txt", "request20_Ga6.txt"]
name_file30 = ["request30_Ga1.txt", "request30_Ga2.txt", "request30_Ga3.txt", "request30_Ga4.txt", "request30_Ga5.txt", "request30_Ga6.txt"]

for vu in vung:
    for mi in mien:
        for i in id:
            path_begin = output_f +"/"+ vu +"_"+ mi +"_"+ i +"/"
            print(path_begin)

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

            ga6_10 = []
            for i in rq10:
                if i[0] in ga6_10:continue
                ga6_10.append(i[0])

            ga6_20 = []
            for i in rq20:
                if i[0] in ga6_20:continue
                ga6_20.append(i[0])

            ga6_30 = []
            for i in rq30:
                if i[0] in ga6_30:continue
                ga6_30.append(i[0])
            print(ga6_10)

