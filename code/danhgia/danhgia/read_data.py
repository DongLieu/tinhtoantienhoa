def read_file(input):
    with open(input, "r") as file:
        content = file.read()
    content = content.split("\n")
    if content[-1] == "":content = content[:len(content)-1]

    # print(content)
    data = []
    for i in range(len(content)):
        tmp = content[i].split(",")
        tmp2 = []
        for j in tmp:
            tmp2.append(float(j))

        if tmp2 in data:continue
        data.append(tmp2)
    return data


# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output

output_f = "./code/danhgia/pareto"

vung = ["cogent"]#, "conus", "nsf"]

mien = ["center"]#, "rural", "uniform", "urban"]

id = ["0"]#, "1", "2", "3", "4"]

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output\cogent_center_0\
name_file10 = ["request10_MOTLBO.txt", "request10_NSGA2.txt", "request10_MOEAD.txt"]
name_file20 = ["request20_MOTLBO.txt", "request20_NSGA2.txt", "request20_MOEAD.txt"]
name_file30 = ["request30_MOTLBO.txt", "request30_NSGA2.txt", "request30_MOEAD.txt"]

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


# pareto(input, output)