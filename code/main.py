from MOTLBO import *

name_folder = "nsf_uniform_1"
# name_folder = "nsf_urban_0"

path_folder = "/Users/duongdong/tinhtoantienhoa/dataset/"

path_input = path_folder + name_folder + "/input.txt"

path_request10 = path_folder + name_folder + "/request10.txt"
path_request20 = path_folder + name_folder + "/request20.txt"
path_request30 = path_folder + name_folder + "/request30.txt"

n_pop = 100
gen = 1000
num_remove = 10

motlbo = MOTLBO(n_pop, gen, num_remove, path_input, path_request10)
motlbo.initialize_population()
print(len(motlbo.pop))
print(motlbo.pop[0].x_vnf)