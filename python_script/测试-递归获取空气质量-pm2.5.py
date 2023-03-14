
# PM2.5(微克每立方米), PM10(微克每立方米), SO2(微克每立方米), NO2(微克每立方米), CO(毫克每立方米), O3(微克每立方米), U(m/s), V(m/s), TEMP(K), RH(%), PSFC(Pa), lat, lon,

# 根据 lat,lon 维度和经度 获取adcode值

# 数组，每个数组是一个对象：name的值为地区名 和 value值为大小

# 例如湖南省的值
# 先求每个市的值
# 每个市需要递归求每个区的值


import csv

from 经纬度获取adcode并且json复用 import *

adcode_monitors = {}


# 第一步，整理成 {adcode:{item_name:平均值}}
# 例如 item_name:"PM2.5"
def create_adcode_monitors(item_name,row_index,csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        for index, row in enumerate(reader):
            if index==0:
                continue
            adcode = int(reverse_geocoding_adcode((row[11]), (row[12])))
            # adcode = '0' 的属于不在中国陆地地图之内的
            if adcode in adcode_monitors:
                adcode_monitors[adcode][item_name].append(float(str.strip(row[row_index])))
            else:
                adcode_monitors[adcode] = {item_name:[float(str.strip(row[row_index]))]}
            # 0 pm2.5
        for i_adcode in adcode_monitors.keys():
            average = sum(adcode_monitors[i_adcode][item_name])/len(adcode_monitors[i_adcode][item_name])
            adcode_monitors[i_adcode]["max"] = max(adcode_monitors[i_adcode][item_name])
            adcode_monitors[i_adcode]["min"] = min(adcode_monitors[i_adcode][item_name])
            adcode_monitors[i_adcode]["average"] = average
    pass


adcode_info = {}

def get_adcode_info_childrenArr(adcode):
    return (adcode_info[str(adcode)]["childrenArr"])


def get_adcode_info_childrenNum(adcode):
    return (adcode_info[str(adcode)]["childrenNum"])


adcode_ans = {}
# 递归求值
def get_adcode_item_value(adcode,item_name="PM2.5"):
    child_num = get_adcode_info_childrenNum(adcode)
    if(child_num==0):
        if(adcode in adcode_monitors):
            adcode_ans[int(adcode)]=adcode_monitors[int(adcode)]["max"]
            return adcode_monitors[int(adcode)]["max"]
            pass
        else:
            return 0
    else:
        child_arr = get_adcode_info_childrenArr(adcode)
        arr_max = 0
        for child_adcode in child_arr:
            arr_max = max(get_adcode_item_value(child_adcode,item_name=item_name),arr_max)
        adcode_ans[int(adcode)] = arr_max
        return arr_max



if __name__ == '__main__':
    adcode_ans = {}
    adcode_info = {}
    adcode_monitors = {}

    with open("adcode_info.json", 'r', encoding='utf-8') as load_f:
        adcode_info = json.load(load_f)
    create_adcode_monitors("PM2.5",0,'./data/201301/CN-Reanalysis-daily-2013010100.csv')
    l = get_adcode_item_value("100000")
    with open("pm2.5-2013010100.json",'w',encoding='utf-8') as save_f:
        json.dump(adcode_ans,save_f,ensure_ascii=False)
        save_f.close()
