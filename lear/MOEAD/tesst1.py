import random
import numpy as np
from math import pow

class MOEAD:
    def __init__(self, population_size, num_generations, crossover_rate, mutation_rate):
        self.population_size = population_size
        self.num_generations = num_generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def objective_f1(self, x):
        return pow((x - 1), 2)    #1

    def objective_f2(self, x):
        return -pow(x, 2)         #10

    def objective_f3(self, x):
        return pow(x, 2) - 8      #0

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = random.uniform(-10, 10)
            population.append(individual)
        return population

    def evaluate_population(self, population):
        evaluated_population = []
        for individual in population:
            f1 = self.objective_f1(individual)
            f2 = self.objective_f2(individual)
            f3 = self.objective_f3(individual)
            evaluated_population.append((individual, f1, f2, f3))
        return evaluated_population

    def select_parents(self, population, num_parents):
        parents = []
        ranked_population = sorted(population, key=lambda x: (x[1], x[2], x[3]))
        parents = ranked_population[:num_parents]
        print("-----")
        print(parents)
        return parents

    def crossover(self, parent1, parent2):
        alpha = random.uniform(0, 1)
        child = alpha * parent1 + (1 - alpha) * parent2
        return child

    def mutate(self, individual):
        if random.uniform(0, 1) < self.mutation_rate:
            individual = random.uniform(-10, 10)
        return individual

    def create_offspring(self, parents):
        offspring = []
        num_parents = len(parents)
        while len(offspring) < self.population_size:
            parent1, parent2 = random.sample(parents, 2)
            child = self.crossover(parent1[0], parent2[0])
            child = self.mutate(child)
            offspring.append(child)
        return offspring[:self.population_size]

    def solve(self):
        population = self.initialize_population()
        for _ in range(self.num_generations):
            evaluated_population = self.evaluate_population(population)
            parents = self.select_parents(evaluated_population, 6)
            population = self.create_offspring(parents)
        evaluated_population = self.evaluate_population(population)
        return evaluated_population

# Chạy thuật toán MOEA/D và in kết quả
population_size = 100
num_generations = 5000
crossover_rate = 0.8
mutation_rate = 0.1

moead = MOEAD(population_size, num_generations, crossover_rate, mutation_rate)
results = moead.solve()

# for individual in results:
#     x, f1, f2, f3 = individual
#     print("x =", x)
#     print("f1 =", f1)
#     print("f2 =", f2)
#     print("f3 =", f3)
#     print("-----------")
