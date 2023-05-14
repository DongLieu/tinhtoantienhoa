import numpy as np

# Hàm tính giá trị f(x) và g(x)
def f(x):
    return x**2

def g(x):
    return (x-2)**2

# Hàm tính khoảng cách Euclidean giữa hai điểm
def euclidean_distance(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

# Hàm MOTLBO
def motlbo(f, g, bounds, pop_size, max_gen):
    # Khởi tạo quần thể
    pop = np.random.uniform(bounds[0], bounds[1], size=(pop_size, 1))

    # Tiến hành tối ưu hóa
    for gen in range(max_gen):
        # Tính giá trị f(x) và g(x) cho từng cá thể trong quần thể
        f_values = np.array([f(x) for x in pop])
        g_values = np.array([g(x) for x in pop])

        # Tính khoảng cách Euclidean giữa các cá thể
        distances = np.zeros((pop_size, pop_size))
        for i in range(pop_size):
            for j in range(pop_size):
                distances[i, j] = euclidean_distance(pop[i], pop[j])

        # Tìm kiếm giải pháp Pareto-optimality
        pareto_optimal = []
        for i in range(pop_size):
            is_pareto_optimal = True
            for j in range(pop_size):
                if f_values[j] <= f_values[i] and g_values[j] <= g_values[i] and distances[i, j] < distances[j, i]:
                    is_pareto_optimal = False
                    break
            if is_pareto_optimal:
                pareto_optimal.append(i)

        # Cập nhật quần thể bằng cách chọn lọc ngẫu nhiên các giải pháp Pareto-optimality
        selected_indices = np.random.choice(pareto_optimal, size=pop_size, replace=True)
        pop = pop[selected_indices]

        # Tiến hành lai ghép và đột biến
        for i in range(0, pop_size, 2):
            p1 = pop[i]
            p2 = pop[i + 1]
            p3 = pop[np.random.randint(0, pop_size)]
            p4 = pop[np.random.randint(0, pop_size)]

            beta = np.random.uniform(-0.25, 1.25, size=(1, 1))
            c1 = p1 + beta * (p2 - p3)
            c2 = p4 + beta * (p1 - p2)

            c1 = np.clip(c1, bounds[0], bounds[1])
            c2 = np.clip(c2, bounds[0], bounds[1])

            # Thay thế các cá thể không tối ưu bbằng các con cá thể con sau khi lai ghép và đột biến
            if f(c1) < f(p1) and g(c1) < g(p1):
                pop[i] = c1
            if f(c2) < f(p2) and g(c2) < g(p2):
                pop[i + 1] = c2
        # Trả về kết quả
        pareto_optimal_solutions = [pop[i] for i in pareto_optimal]
        return pareto_optimal_solutions

bounds = [0, 5] # Khoảng giá trị của biến x
pop_size = 100 # Kích thước quần thể
max_gen = 100 # Số lượng thế hệ
pareto_optimal_solutions = motlbo(f, g, bounds, pop_size, max_gen)
print("Các giải pháp Pareto-optimality:")
for i, sol in enumerate(pareto_optimal_solutions):
    print("Giải pháp", i+1, ": x =", sol[0], ", f(x) =", f(sol[0]), ", g(x) =", g(sol[0]))