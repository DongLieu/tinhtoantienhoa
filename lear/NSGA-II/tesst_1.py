import random
import numpy as np
from math import pow

# Định nghĩa hàm mục tiêu f1 = (x-1)^2
def objective_f1(x):
    return pow((x - 1), 2)

# Định nghĩa hàm mục tiêu f2 = -x^2
def objective_f2(x):
    return -pow(x, 2)

# Định nghĩa hàm mục tiêu f3 = x^2 - 8
def objective_f3(x):
    return pow(x, 2) - 8

# Hàm tạo quần thể ban đầu
def initialize_population(population_size):
    population = []
    for _ in range(population_size):
        individual = random.uniform(-10, 10)  # Khởi tạo cá thể ngẫu nhiên trong khoảng [-10, 10]
        population.append(individual)
    return population

# Đánh giá giá trị các hàm mục tiêu cho từng cá thể
def evaluate_population(population):
    evaluated_population = []
    for individual in population:
        f1 = objective_f1(individual)
        f2 = objective_f2(individual)
        f3 = objective_f3(individual)
        evaluated_population.append((individual, f1, f2, f3))
    return evaluated_population

# Hàm lựa chọn cá thể dựa trên chiều không gian Pareto
def select_parents(population, num_parents):
    parents = []
    ranked_population = sorted(population, key=lambda x: (x[1], x[2], x[3]))  # Sắp xếp quần thể theo giá trị của các hàm mục tiêu
    parents = ranked_population[:num_parents]
    return parents

# Hàm lai ghép hai cá thể
def crossover(parent1, parent2):
    alpha = random.uniform(0, 1)  # Chọn một điểm cắt ngẫu nhiên
    child = alpha * parent1 + (1 - alpha) * parent2  # Áp dụng phép lai ghép kết hợp điểm cắt
    return child

# Hàm đột biến cá thể
def mutate(individual, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        individual = random.uniform(-10, 10)  # Thay thế cá thể bằng một cá thể ngẫu nhiên khác
    return individual

# Hàm tạo thế hệ mới từ các cá thể được chọn lọc và các toán tử di truyền
def create_offspring(parents, population_size, crossover_rate, mutation_rate):
    offspring = []
    num_parents = len(parents)
    while len(offspring) < population_size:
        parent1, parent2 = random.sample(parents, 2)  # Chọn hai cá thể cha mẹ ngẫu nhiên từ danh sách cha mẹ
        child = crossover(parent1[0], parent2[0])  # Lai ghép hai cá thể cha mẹ để tạo ra cá thể con
        child = mutate(child, mutation_rate)  # Đột biến cá thể con
        offspring.append(child)
    return offspring[:population_size]  # Trả về một số lượng cá thể con tương ứng với kích thước quần thể

# Hàm chạy thuật toán NSGA-II
def nsga2(population_size, num_generations, crossover_rate, mutation_rate):
    population = initialize_population(population_size)
    for _ in range(num_generations):
        evaluated_population = evaluate_population(population)
        parents = select_parents(evaluated_population, population_size)
        population = create_offspring(parents, population_size, crossover_rate, mutation_rate)
    evaluated_population = evaluate_population(population)
    return evaluated_population

# Chạy thuật toán và in kết quả
population_size = 100
num_generations = 50
crossover_rate = 0.8
mutation_rate = 0.1

results = nsga2(population_size, num_generations, crossover_rate, mutation_rate)
for individual in results:
    x, f1, f2, f3 = individual
    print("x =", x)
    print("f1 =", f1)
    print("f2 =", f2)
    print("f3 =", f3)
    print("-----------")
