import random
import math

# Định nghĩa hàm mục tiêu
def f1(x):
    return (x - 1) ** 2

def f2(x):
    return -x ** 2

def f3(x):
    return x ** 2 - 8

# Định nghĩa hàm tính toán khoảng cách Euclidean giữa hai điểm
def euclidean_distance(point1, point2):
    return math.sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(point1, point2)))

# Khởi tạo quần thể ban đầu
population_size = 100
lower_bound = -10
upper_bound = 10
population = []
for _ in range(population_size):
    x = random.uniform(lower_bound, upper_bound)
    population.append([x, f1(x), f2(x), f3(x)])

# Thiết lập tham số MOEA/D
max_generations = 100
neighborhood_size = 10

# Bước lặp qua các thế hệ
for generation in range(max_generations):
    # Tạo các điểm con cái mới
    offspring_population = []
    for _ in range(population_size):
        # Lựa chọn ngẫu nhiên một cá thể trong hàng xóm của mỗi cá thể
        neighborhood = random.sample(population, neighborhood_size)
        parent = random.choice(neighborhood)
        
        # Tạo con cái mới bằng cách đột biến cá thể cha
        offspring = parent.copy()
        offspring[0] = random.uniform(lower_bound, upper_bound)
        offspring[1] = f1(offspring[0])
        offspring[2] = f2(offspring[0])
        offspring[3] = f3(offspring[0])
        
        offspring_population.append(offspring)

    # Tính toán chỉ số Pareto để lựa chọn cá thể tốt nhất
    for i in range(population_size):
        individual = offspring_population[i]
        individual_pareto_dominant = True
        
        for j in range(population_size):
            if i != j:
                other_individual = offspring_population[j]
                if (individual[1] > other_individual[1] and individual[2] > other_individual[2] and individual[3] > other_individual[3]) or \
                   (individual[1] >= other_individual[1] and individual[2] > other_individual[2] and individual[3] > other_individual[3]) or \
                   (individual[1] > other_individual[1] and individual[2] >= other_individual[2] and individual[3] > other_individual[3]) or \
                   (individual[1] > other_individual[1] and individual[2] > other_individual[2] and individual[3] >= other_individual[3]):
                    individual_pareto_dominant = False
                    break

        if individual_pareto_dominant:
            population[i] = individual

# In ra các giải pháp tối ưu tìm được
print("Optimal Solutions:")
for individual in population:
    print("x = {:.4f}, f1 = {:.4f}, f2 = {:.4f}, f3 = {:.4f}".format(individual[0], individual[1], individual[2], individual[3]))
