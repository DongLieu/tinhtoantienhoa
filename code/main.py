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
motlbo.evaluate_population()
motlbo.good_finess_and_expulsion()

# print(len(motlbo.need_improve))

# print(motlbo.fitness[0])
# print(motlbo.fitness[1])
# print(motlbo.pop[0].vnf_x)
# print(motlbo.fitness[0])
# print(motlbo.fitness[0][0])
# print(motlbo.fitness[0][1])
# print(motlbo.fitness[0][2])
# print("-----------")
# print(len(motlbo.dominant_set))
# print(motlbo.dominant_set)
x_teacher = motlbo.pop[0]
x_student = motlbo.pop[1]
print(x_student.x)
print(x_student.delay_servers_and_links_use)
print("-----------")


new_student, success = motlbo._teacher_teaching_student(x_teacher, x_student)
if success:
    print("ok")
    x_student = new_student

print(new_student.x)
print(new_student.delay_servers_and_links_use)
print("-----------")
print(x_student.x)
print(x_student.delay_servers_and_links_use)



# s = len(motlbo.pop[0].x_vnf)
# print(s)
# print("-----------0000")
# print(len(motlbo.expulsion_set))
# print(motlbo.expulsion_set)