import os

# Bộ dữ liệu:
def _read_file(folder, filename):
        # Lấy đường dẫn tuyệt đối đến thư mục hiện tại
    current_dir = os.path.abspath(os.getcwd())

    # Kết hợp đường dẫn tương đối để tạo đường dẫn đầy đủ đến file input.txt
    file_path = os.path.join(current_dir, "dataset", folder, filename)

    # Đọc nội dung của file và chia theo dòng
    with open(file_path, "r") as f:
        data_line = f.readlines()

    data_str = []
    for line in data_line:
        tmp = line.split(" ")
        data_str.append(tmp)
    
    data = []
    for i in range(len(data_str)):
        tmp = []
        for j in range(len(data_str[i])):   
            tmp.append(int(data_str[i][j]))
        data.append(tmp)
    return data

def read_input(name_folder):
    data = _read_file(name_folder, "input.txt")
    # so luong VNF
    f = data[0][0]
    # so luong VNF toi da duoc cai dat 
    l = data[0][1]
    # so luong nut
    n = data[1][0]

    # mỗi dòng gồm các số nguyên miêu tả một nút trên đồ thị: id, delay, costServer:costVNF_1, costVNF_2,...
    V_nodes = []
    for i in range(2, n + 2):
        tmp = []
        tmp.append(data[i][0])
        tmp.append(data[i][1])
        tmp.append(data[i][2])
        if data[i][2] == -1 :
            V_nodes.append(tmp)
            continue
        else:
            for j in range(3, 3 + f):
                tmp.append(data[i][j])
            V_nodes.append(tmp)
    # so canh
    m = data[n+2][0]
    # mỗi dòng gồm các số nguyên miêu tả một cạnh trên đồ thị:u, v, delay(Một cạnh nối giữa u và v) delay [200,500]
    E_links = []
    for i in range(n+3, n+3 + m):
        tmp = []
        tmp.append(data[i][0])
        tmp.append(data[i][1])
        tmp.append(data[i][2])
        E_links.append(tmp)

    return f, l, n, V_nodes, m, E_links


def _read_request(name_folder, name_file):
    data = _read_file(name_folder, name_file)
    # so luong request:
    Q = data[0][0]
    # miêu tả một request:bandwith, memory, cpu, u, v, k, tiếp theo là k VNFs yêu cầu thực hiện theo thứ tự
    Requests = []
    for i in range(1, 1 + Q):
        tmp = []
        tmp.append(data[i][0]) #bw
        tmp.append(data[i][1]) #mem
        tmp.append(data[i][2]) #cpu
        tmp.append(data[i][3]) #u
        tmp.append(data[i][4]) #v
        k = data[i][5]
        tmp.append(k) #k
        for j in range(6, 6 + k):
            tmp.append(data[i][j])

        Requests.append(tmp)


    return Q, Requests

def read_request10(name_folder):
    return _read_request(name_folder, "request10.txt")

def read_request20(name_folder):
    return _read_request(name_folder, "request20.txt")

def read_request30(name_folder):
    return _read_request(name_folder, "request30.txt")

