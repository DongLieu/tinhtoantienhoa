import random
import math

z = [-1, -11, -12]
print(z)
num_expulsion = 3


expulsion =[]

for i in range(num_expulsion):
    element_to_remove = random.choice(z)
    expulsion.append(element_to_remove)
    z.remove(element_to_remove)

print(z)
print(expulsion)

print(math.sqrt(25))