
miens = ["conus","cogent", "nsf"]

vungs = ["urban", "center", "rural", "uniform"]

requests = [10, 20, 30]

i_s = [2, 1, 0, 3, 4]

for mien in miens:
    for vung in vungs:
            for i in i_s:
                for request in requests:
                    if (mien == "cogent") and (vung == "center") and i in [0,1,2]: continue

                    name_folder = mien+"_"+vung+"_"+str(i) + "/request"+str(request)
