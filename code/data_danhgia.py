
# File này dùng để convert lại file output của thuật toán MOTLBO, NSGA-II, MOEA/D để đưa vào folder pareto 
input_f = "./code/output"
output_f = "./code/danhgia/pareto"

vung = ["cogent", "conus", "nsf"]

mien = ["center", "rural", "uniform", "urban"]

id = ["0", "1", "2", "3", "4"]

name_file = ["request10_MOTLBO.txt", "request10_NSGA2.txt", "request10_MOEAD.txt",\
              "request20_MOTLBO.txt", "request20_NSGA2.txt", "request20_MOEAD.txt",  \
                "request30_MOTLBO.txt", "request30_NSGA2.txt", "request30_MOEAD.txt",]

def pareto(input, output):
        with open(output, 'w') as file:
            file.truncate(0)

        with open(input, "r") as file:
            content = file.read()

        content = content.split("Gen:")
        data = content[-1]
        data = data.split("[")
        for i in range(len(data)):
            data[i] = data[i].replace("]","")
            data[i] = data[i].replace("\n","")


            # ghi
            if i == 0: continue
            with open(output, 'a') as file:
                # Ghi các lời gọi print vào file
                print(data[i], file=file)
        
input = input_f +"/"+ vung[0] +"_"+ mien[0] +"_"+ id[0] +"/"+ name_file[0]
output = output_f +"/"+ vung[0] +"_"+ mien[0] +"_"+ id[0] +"/"+ name_file[0]

for vu in vung:
    for mi in mien:
        for i in id:
             for na in name_file:
                  input = input_f +"/"+ vu +"_"+ mi +"_"+ i +"/"+ na
                  output = output_f +"/"+ vu +"_"+ mi +"_"+ i +"/"+ na

                  pareto(input, output)

                  
             


# pareto(input, output)