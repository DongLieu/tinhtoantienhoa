
input = "/Users/duongdong/tinhtoantienhoa/code/danhgia/danhgia/C_metric.txt"
with open(input, "r") as file:
    content = file.read()


content = content.split("\n")
content = content[:len(content)-1]
data = []
for i in content:

    tmp = i.split("&")
    data_tmp = []
    for j in tmp:
        a = float(j)
        data_tmp.append(a)
    data.append(data_tmp)


path_output = "./code/danhgia/danhgia/d_metric.txt"
with open(path_output, 'w') as file:
    file.truncate(0)

for i in range(12):
    a = i*5
    # print(data[a])
    # print(data[a + 4])
    d1 = sum(data[a+m][0] for m in range(5))
    d2 = sum(data[a+m][1] for m in range(5))
    d3 = sum(data[a+m][2] for m in range(5))
    d1 = d1/5
    d2 = d2/5
    d3 = d3/5
    with open(path_output, 'a') as file:
        print(" & {:.4f}".format(d1)," & ","{:.4f}".format(d2)," & ","{:.4f} \\\\".format(d3), file=file)
