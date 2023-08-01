
# File này dùng để convert lại file output của thuật toán GA-6 để đưa vào folder pareto 
input_f = "./code/output"
output_f = "./code/danhgia/pareto"

vung = ["cogent", "conus", "nsf"]

mien = ["center", "rural", "uniform", "urban"]

id = ["0", "1", "2", "3", "4"]


name_file = [
            "request10_Ga1.txt", "request10_Ga2.txt", "request10_Ga3.txt", "request10_Ga4.txt", "request10_Ga5.txt", "request10_Ga6.txt",\
            "request20_Ga1.txt", "request20_Ga2.txt", "request20_Ga3.txt", "request20_Ga4.txt", "request20_Ga5.txt", "request20_Ga6.txt",\
            "request30_Ga1.txt", "request30_Ga2.txt", "request30_Ga3.txt", "request30_Ga4.txt", "request30_Ga5.txt", "request30_Ga6.txt",\
]

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