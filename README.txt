Các bộ dữ liệu nằm trong các folders topology_distribution_id
Mỗi folder gồm các files input.txt, request10.txt, request20.txt, request30.txt.

#File input.txt
Dòng đầu tiên gồm một số nguyên k, l chỉ số lượng VNF và số VNF tối đa được cài đặt 
trên một nút Server. (l được lấy ngẫu nhiên trong 
đoạn [Ceil(T / |V_Server|), 2 * Ceil(T / |V_Server|)])
Dòng tiếp theo gồm một số nguyên n chỉ số lượng nút.
n dòng tiếp theo mỗi dòng gồm các số nguyên miêu tả một nút trên đồ thị: 
	id, delay, costServer.
	(nếu costServer >= 0 thì nút id là server, tiếp đến là T số costVNF_1, costVNF_2, ...,
	costVNF_T tương ứng với chi phí để cài đặt VNF f_1, f_2, ..., f_T ở nút server id,
	 nếu costServer = -1 thì nút id là PNF),
	(costServer random trong khoảng [5000, 10000], costVNF random trong khoảng [1000, 2000])
Dòng tiếp theo gồm một số nguyên m chỉ số lượng cạnh.
m dòng tiếp theo mỗi dòng gồm các số nguyên miêu tả một cạnh trên đồ thị:
	u, v, delay
	(Một cạnh nối giữa u và v) delay [200,500]

#File requestX.txt
Dòng đầu tiên gồm một số nguyên Q chỉ số lượng request.
Q dòng tiếp theo mỗi dòng gồm các số nguyên miêu tả một request:
	bandwith, memory, cpu, u, v, k, tiếp theo là k VNFs yêu cầu thực hiện theo thứ tự
	(Request tiêu tốn một lượng băng thông bandwith, bộ nhớ memory, lượng xử lý cpu,
	 yêu cầu từ nút u tới nút v và yêu cầu thực hiện k VNFs theo thứ tự)