import numpy as np

# Ham muc tieu
def obj_func(x):
    f1 = x[0]**2
    f2 = (x[0]-2)**2
    return [f1, f2]

# MOTLBO class
class MOTLBO:
    def __init__(self, obj_func, n_var, n_pop, n_gen):
        self.obj_func = obj_func
        self.n_var = n_var
        self.n_pop = n_pop
        self.n_gen = n_gen
        self.pop = None
        self.fitness = None
        self.archive = None
        self.archive_fitness = None

    #khoi tao quan the [-2.5; 2.5]
    def initialize_population(self):
        self.pop = np.random.rand(self.n_pop, self.n_var) * 5 - 2.5


    #tinh gia tri cho tat ca ca the
    def evaluate_population(self):
        self.fitness = np.array([self.obj_func(x) for x in self.pop])


    # day
    def teaching_phase(self, alpha):
        for i in range(self.n_pop):
            teacher = self.pop[i]
            for j in range(self.n_pop):
                if i != j:
                    student = self.pop[j]
                    r = np.random.rand()
                    if r > 0.5:
                        self.pop[j] = student + alpha * (teacher - student)
    # hoc
    def learning_phase(self, beta):
        for i in range(self.n_pop):
            learner = self.pop[i]
            for j in range(self.n_pop):
                if i != j:
                    teacher = self.pop[j]
                    r = np.random.rand()
                    if r > 0.5:
                        self.pop[i] = learner + beta * (teacher - learner)
    #cap nhat lai 
    def update_archive(self):
        if self.archive is None:
            self.archive = self.pop[:5]
            self.archive_fitness = self.fitness[:5]
        else:
            # combined_pop = np.vstack((self.archive, self.pop))
            combined_fitness = np.vstack((self.archive_fitness, self.fitness))
            arc_finess_new0 = np.sort(combined_fitness[:,0])[:5]
            arc_finess_new1 = np.sort(combined_fitness[:,1])[:5]
            # unique_indices = np.unique(combined_fitness, axis=0, return_index=True)[0:5]

            self.archive_fitness =np.column_stack((arc_finess_new0, arc_finess_new1))
    # full stream process
    def run(self):
        self.initialize_population()
        self.evaluate_population()

        for gen in range(self.n_gen):
            alpha = np.random.rand()
            beta = np.random.rand()
            self.teaching_phase(alpha)
            self.learning_phase(beta)
            self.evaluate_population()
            self.update_archive()

        return self.archive, self.archive_fitness

# tham so dau vao
n_var = 2 # so bien
n_pop = 100 # so ca the trong quan the
n_gen = 1000 # so the he


motlbo = MOTLBO(obj_func, n_var, n_pop, n_gen)
motlbo.initialize_population()
motlbo.evaluate_population()
print("pop:")
print(motlbo.pop)
print("fit:")
print(motlbo.fitness)
print("===")
finess_new0 = np.sort(motlbo.fitness[:,0])[:5]
finess_new1 = np.sort(motlbo.fitness[:,1])[:5]
fn = np.column_stack((finess_new0, finess_new1))
print(fn)
print(fn.shape)
print(motlbo.fitness[:5])

# print(motlbo.fitness.shape)
# top = np.unique(motlbo.fitness[1,], axis=0, return_index=True)[1]
# new_finess = motlbo.fitness[top]
# print(new_finess)


# Run MOTLBO
# pareto_front, pareto_fitness = motlbo.run()

# Print Pareto front and fitness values
# print("Pareto Front:")
# print(pareto_front)
# print("Fitness Values:")
# print(pareto_fitness)
