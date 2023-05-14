import numpy as np

# Ham muc tieu
def obj_func1(x):
    return (x-3)**2 #x=3

def obj_func2(x):
    return (x+3)**2 #x=-3

# MOTLBO class
class MOTLBO:
    def __init__(self, obj_func1, obj_func2, n_pop, n_gen, num_teacher, alpha, beta):
        self.obj_func1 = obj_func1
        self.obj_func2 = obj_func2
        self.alpha = alpha
        self.beta = beta
        self.n_pop = n_pop
        self.n_gen = n_gen
        self.num_teacher = num_teacher
        self.pop = None
        self.fitness1 = None
        self.fitness2 = None
        self.teacher1 = None
        self.teacher2 = None

    #khoi tao quan the [-5; 5]
    def initialize_population(self):
        self.pop = np.random.rand(self.n_pop) * 10 - 5

    def top_finess(self):
        # arc_finess_new0 = np.sort(self.fitness[:,0]
        topfiness1 = np.argsort(self.fitness1[:,1])
        self.fitness1 = self.fitness1[topfiness1]
        topfiness2 = np.argsort(self.fitness2[:,1])
        self.fitness2 = self.fitness2[topfiness2]
       
    #tinh gia tri cho tat ca ca the
    def evaluate_population(self):
        fitness1 = np.array([self.obj_func1(x) for x in self.pop])
        fitness2 = np.array([self.obj_func2(x) for x in self.pop])
        self.fitness1 = np.column_stack((self.pop, fitness1))
        self.fitness2 = np.column_stack((self.pop, fitness2))

    def choose_teacher(self):
        self.teacher1 = self.fitness1[:,0][:num_teacher]
        self.teacher2 = self.fitness2[:,0][:num_teacher]

    def thaythe(self, giatrithaythe, bithaythe):
        for i in range(len(self.pop)):
            if self.pop[i] == bithaythe:
                self.pop[i] = giatrithaythe

    def learning_phase(self):
        for i in range(self.num_teacher):
            learner1 = self.teacher1[i]
            learner2 = self.teacher2[i]
            for j in range(self.num_teacher):
                if i != j:
                    teacher1 = self.teacher1[j]
                    teacher2 = self.teacher2[j]
                    r = np.random.rand()
                    if r > 0.5:
                        learner1_cokhathi = learner1 + self.beta * (teacher1 - learner1)
                        if self.obj_func1(learner1_cokhathi) < self.obj_func1(learner1):
                            self.thaythe(learner1_cokhathi, learner1)

                            
                        learner2_cokhathi = learner2 + self.beta * (teacher2 - learner2)
                        if self.obj_func2(learner2_cokhathi) < self.obj_func2(learner2):
                            self.thaythe(learner2_cokhathi, learner2)
 
    def teaching_phase(self):
        for i in range(self.num_teacher):
            teacher1 = self.teacher1[i]
            teacher2 = self.teacher2[i]
            for j in range(self.n_pop):
                if self.pop[j] not in self.teacher1 and self.pop[j] not in self.teacher2:
                    student = self.pop[j]
                    r = np.random.rand()
                    if r > 0.5:
                        hoctot1 = student + alpha * (teacher1-student)
                        if self.obj_func1(hoctot1) < self.obj_func1(student):
                            self.thaythe(hoctot1, student)
                    else:
                        hoctot2 = student + alpha * (teacher2-student)
                        if self.obj_func2(hoctot2) < self.obj_func2(student):
                            self.thaythe(hoctot2, student)
    # full stream process
    def run(self):
        # khoi tao
        self.initialize_population()
        # tinh gia tri
        self.evaluate_population()
        # sap xep
        self.top_finess()
        # chon teacher
        self.choose_teacher()
        for gen in range(self.n_gen):
            # day
            self.teaching_phase()
            # hoc
            self.learning_phase()
            # tinh lai gia tri
            self.evaluate_population()
            # sap xep
            self.top_finess()
            # chon teacher
            self.choose_teacher()
            print("Gen" + str(gen+1) + ":" + str(self.teacher1[0]) + "        "+ str(self.teacher2[0]))

        return self.teacher1[0], self.teacher2[0]

# tham so dau vao
n_pop = 15 # so ca the trong quan the
n_gen = 1000 # so the he
num_teacher = 5 # so teacher
alpha = 0.05 # toc do hoc cua student
beta = 0.01 # toc do hoc cua teacher

motlbo = MOTLBO(obj_func1,obj_func2, n_pop, n_gen, num_teacher, alpha, beta)
motlbo.run()
