
# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output
input_f = "./code/output"
output_f = "./danhgia/pareto"

vung = ["cogent", "conus", "nsf"]

mien = ["center", "rural", "uniform", "urban"]

id = ["0", "1", "2", "3", "4"]

# C:\Users\DongTramCam\Desktop\tinhtoantienhoa\code\output\cogent_center_0\
name_file = ["request10_ISO.txt", "request10_MOTLBO.txt", "request10_NSGA2.txt", "request10_MOEAD.txt",\
              "request20_ISO.txt", "request20_MOTLBO.txt", "request20_NSGA2.txt", "request20_MOEAD.txt",  \
                "request30_ISO.txt", "request30_MOTLBO.txt", "request30_NSGA2.txt", "request30_MOEAD.txt",]

input = input_f +"/"+ vung[0] +"_"+ mien[0] +"_"+ id[0] +"/"+ name_file[1]
output = output_f +"/"+ vung[0] +"_"+ mien[0] +"_"+ id[0] +"/"+ name_file[1]

def pareto(input, output):
        
        with open(input, "r") as file:
            content = file.read()

        content = content.split("Gen:")
        data = content[-1]
        data = data.split("[")

        data[1] = data[1].replace("]","")
        data[1] = data[1].replace("\n","")
        print(data[1])
        

pareto(input, output)