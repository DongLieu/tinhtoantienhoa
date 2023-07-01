
from MOTLBO import *
from MOEAD import *
from NSGA2 import *
from ISO import *

miens = ["cogent"]
vungs = ["center"]#"rural", "uniform", "urban"]#"center",

requests = [10, 20, 30]

TIMELIMIT = 600


for mien in miens:
    for vung in vungs:
        for request in requests:
            for i in range(5):
                name_folder = mien+"_"+vung+"_"+str(i)
                # print("namefolder:{}|| request:{}|| ".format(name_folder, request))

                ############################-MOTLBO-##############################
                N_POP_MOTLBO = 50
                GEN_MOTLBO = 1000
                NUM_REMOVE_MOTLBO = 20

                motlbo = MOTLBO(N_POP_MOTLBO, GEN_MOTLBO, TIMELIMIT, NUM_REMOVE_MOTLBO, name_folder, request)
                motlbo.run()

                # ############################-MOEAD-##############################
                N_POP_MOEAD = 20

                GEN_MOEAD = 1000

                moead = MOEAD(N_POP_MOEAD, GEN_MOEAD, TIMELIMIT, name_folder, request)
                moead.run()

                # # ############################-NSGA2-##################################
                N_POP_NSGA2 = 50
                GEN_NSGA2 = 50
                NUM_REMOVE_NSGA2 = 10

                nsga2 = NSGA2(N_POP_NSGA2, GEN_NSGA2, TIMELIMIT, NUM_REMOVE_NSGA2, name_folder, request)
                nsga2.run()

                # ##########################-ISO-##################################
                N_POP_ISO = 100
                GEN_ISO = 1000
                NUM_REMOVE_ISO = 40

                iso = ISO(N_POP_ISO, GEN_ISO, TIMELIMIT, NUM_REMOVE_ISO, name_folder, request)
                iso.run()

# ##########################-ALL-##################################

# # Tạo các đối tượng Thread cho từng hàm
# thread1 = threading.Thread(target=motlbo.run)
# thread2 = threading.Thread(target=moead.run)
# thread3 = threading.Thread(target=nsga2.run)
# thread4 = threading.Thread(target=iso.run)
# # Khởi động các luồng thực thi
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()

# # Đợi cho tất cả các luồng kết 



# thread1.join()
# thread2.join()
# thread3.join()
# thread4.join()