from MOTLBO import *

NAME_FOLDER = "nsf_uniform_1"

PATH_FOLDER = "/Users/duongdong/tinhtoantienhoa/dataset/"

PATH_INPUT = PATH_FOLDER + NAME_FOLDER + "/input.txt"

PATH_REQUEST10 = PATH_FOLDER + NAME_FOLDER + "/request10.txt"
PATH_REQUEST20 = PATH_FOLDER + NAME_FOLDER + "/request20.txt"
PATH_REQUEST30 = PATH_FOLDER + NAME_FOLDER + "/request30.txt"

N_POP = 100
GEN = 3000
NUM_REMOVE = 20

motlbo = MOTLBO(N_POP, GEN, NUM_REMOVE, PATH_INPUT, PATH_REQUEST10)
with open('output.txt', 'w') as file:
    print()
motlbo.run()

# motlbo.initialize_population()
# motlbo.evaluate_population()
# motlbo.good_finess_and_expulsion()

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
# x_teacher = motlbo.pop[0]
# x_student = motlbo.pop[1]
# print(x_student.x)
# print(x_student.delay_servers_and_links_use)
# print("-----------")


# new_student, success = motlbo._teacher_teaching_student(x_teacher, x_student)
# if success:
#     print("ok")
#     x_student = new_student

# print(new_student.x)
# print(new_student.delay_servers_and_links_use)
# print("-----------")
# print(x_student.x)
# print(x_student.delay_servers_and_links_use)



# s = len(motlbo.pop[0].x_vnf)
# print(s)
# print("-----------0000")
# print(len(motlbo.expulsion_set))
# print(motlbo.expulsion_set)