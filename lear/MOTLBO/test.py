from collections import deque

queue = deque()

queue.append(10)
queue.append(20)

# Lấy và xoá phần tử từ hàng đợi
item = queue.popleft()
print(item)  # Output: 10

item = queue.popleft()
print(item)  # Output: 20

if queue:
    print("ok")
else:
    print("ko")