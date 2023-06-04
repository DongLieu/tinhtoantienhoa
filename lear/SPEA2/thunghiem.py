import threading
import time

def function1():
    # Chờ 10 giây
    time.sleep(10)
    print(1)
    # Thực hiện công việc của hàm 1 ở đây

def function2():
    time.sleep(8)
    print(2)
    # Thực hiện công việc của hàm 2 ở đây


# Tạo các đối tượng Thread cho từng hàm
thread1 = threading.Thread(target=function1())
thread2 = threading.Thread(target=function2())

# Khởi động các luồng thực thi
thread1.start()
thread2.start()

# Đợi cho tất cả các luồng kết thúc
thread1.join()
thread2.join()

# Tiếp tục thực hiện công việc khác sau khi các luồng đã kết thúc
