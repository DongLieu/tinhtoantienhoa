# import random

# def random_vector():
#     x = random.uniform(0, 1)
#     y = random.uniform(0, 1 - x)
#     z = 1 - x - y
#     return [x, y, z]

# w = random_vector()

# print(w)
import random
import numpy as np

def f1(x):
    return -x**2

def f2(x):
    return (1 - x)**2

def f3(x):
    return x**2 - 8

def initialize_population(size):
    population = []
    for _ in range(size):
        x = random.uniform(-10, 10)
        individual = {'x': x, 'f1': f1(x), 'f2': f2(x), 'f3': f3(x)}
        population.append(individual)
    return population

def update_neighborhood(population, neighborhood_size):
    for i, individual in enumerate(population):
        distances = []
        for j, other in enumerate(population):
            if i != j:
                distance = np.linalg.norm(np.array([individual['f1'], individual['f2'], individual['f3']]) - np.array([other['f1'], other['f2'], other['f3']]))
                distances.append((j, distance))
        distances.sort(key=lambda x: x[1])
        neighborhood = [idx for idx, _ in distances[:neighborhood_size]]
        individual['neighborhood'] = neighborhood

def create_offspring(parents, neighborhood):
    offspring = {}
    parent1 = random.choice(neighborhood)
    parent2 = random.choice(neighborhood)
    while parent2 == parent1:
        parent2 = random.choice(neighborhood)
    x1 = parents[parent1]['x']
    x2 = parents[parent2]['x']
    offspring['x'] = random.uniform(min(x1, x2), max(x1, x2))
    offspring['f1'] = f1(offspring['x'])
    offspring['f2'] = f2(offspring['x'])
    offspring['f3'] = f3(offspring['x'])
    return offspring

def update_population(population, offspring, neighborhood):
    for idx in neighborhood:
        if offspring['f1'] < population[idx]['f1'] and offspring['f2'] < population[idx]['f2'] and offspring['f3'] < population[idx]['f3']:
            population[idx] = offspring

def moead(objective_functions, population_size, neighborhood_size, generations):
    population = initialize_population(population_size)
    update_neighborhood(population, neighborhood_size)
    for _ in range(generations):
        for i in range(population_size):
            neighborhood = population[i]['neighborhood']
            parents = [population[idx] for idx in neighborhood]
            offspring = create_offspring(parents, neighborhood)
            update_population(population, offspring, neighborhood)
    return population

# Thực thi thuật toán MOEA/D
population_size = 20
neighborhood_size = 5
generations = 100

result = moead([f1, f2, f3], population_size, neighborhood_size, generations)

# In kết quả
for individual in result:
    print("x:", individual['x'], "f1:", individual['f1'], "f2:", individual['f2'], "f3:", individual['f3'])
