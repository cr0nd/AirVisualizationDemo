
# PM2.5(微克每立方米), PM10(微克每立方米), SO2(微克每立方米), NO2(微克每立方米), CO(毫克每立方米), O3(微克每立方米), U(m/s), V(m/s), TEMP(K), RH(%), PSFC(Pa), lat, lon,

# 根据 lat,lon 维度和经度 获取adcode值

# 数组，每个数组是一个对象：name的值为地区名 和 value值为大小

# 例如湖南省的值
# 先求每个市的值
# 每个市需要递归求每个区的值


import csv
import os.path
import datetime
import sys
from pprint import pprint

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
                if item_name in adcode_monitors[adcode]:
                    adcode_monitors[adcode][item_name]['values'].append(float(str.strip(row[row_index])))
                else:
                    adcode_monitors[adcode][item_name] = {'values':[float(str.strip(row[row_index]))]}
            else:
                adcode_monitors[adcode] = {item_name:{'values':[float(str.strip(row[row_index]))]}}
            # 0 pm2.5
        for i_adcode in adcode_monitors.keys():
            adcode_monitors[i_adcode][item_name]["max"] = max(adcode_monitors[i_adcode][item_name]['values'])
    pass


def get_adcode_info_childrenArr(adcode):
    return (adcode_info[str(adcode)]["childrenArr"])


def get_adcode_info_childrenNum(adcode):
    return (adcode_info[str(adcode)]["childrenNum"])


adcode_ans = {}
# 递归求值
def get_adcode_item_value(adcode,item_name):
    child_num = get_adcode_info_childrenNum(adcode)
    if(child_num==0):
        if(adcode in adcode_monitors):
            cur_max=adcode_monitors[int(adcode)][item_name]["max"]
            if int(adcode) in adcode_ans:
                adcode_ans[int(adcode)][item_name] = cur_max
            else:
                adcode_ans[int(adcode)] = {item_name: cur_max}
            return cur_max
            pass
        else:
            cur_max=0
            if int(adcode) in adcode_ans:
                adcode_ans[int(adcode)][item_name] = cur_max
            else:
                adcode_ans[int(adcode)] = {item_name: cur_max}
            return cur_max
            return 0
    else:
        child_arr = get_adcode_info_childrenArr(adcode)
        arr_max = 0
        for child_adcode in child_arr:
            arr_max = max(get_adcode_item_value(child_adcode,item_name=item_name),arr_max)

        # 赋值
        if int(adcode) in adcode_ans:
            adcode_ans[int(adcode)][item_name] = arr_max
        else:
            adcode_ans[int(adcode)] = {item_name:arr_max}
        return arr_max



def get_day_allinfo(save_path,csv_path):
    global adcode_ans
    global adcode_monitors

    adcode_ans = {}
    adcode_monitors = {}

    project_name = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    for index,items_name in enumerate(project_name):
        create_adcode_monitors(items_name,index,csv_path)
        l = get_adcode_item_value("100000",items_name)
    # 求取AQI的值
    get_all_AQI()

    with open(save_path,'w',encoding='utf-8') as save_f:
        json.dump(adcode_ans,save_f,ensure_ascii=False)
        save_f.close()


def get_all_AQI():
    project_name = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    aqi_number = {
        "PM10":[[0,25,50,50,0,0],[50,150,50,100,50,50],[150,250,50,100,150,100],[250,350,50,100,250,150],[350,420,100,70,350,200],[420,500,100,80,420,300],[500,600,100,100,500,400]],
        "PM2.5":[[0,35,50,35,0,0],[35,75,50,40,35,50],[75,115,50,40,75,100],[115,150,50,35,115,150],[150,250,100,100,150,200],[250,350,100,100,250,300],[350,500,100,150,350,400]],
        "SO2":[[0,50,50,50,0,0],[50,150,50,100,50,50],[150,475,50,325,150,100],[475,800,50,325,475,150],[800,1600,100,800,800,200],[1600,2100,100,500,1600,300],[2100,2620,100,520,2100,400]],
        "NO2":[[0,40,50,40,0,0],[40,80,50,40,40,50],[80,180,50,100,80,100],[180,280,50,100,180,150],[280,565,100,285,280,200],[565,750,100,185,565,300],[750,940,100,190,750,400]],
        "O3":[[0,160,50,160,0,0],[160,200,50,40,160,50],[200,300,50,100,200,100],[300,400,50,100,300,150],[400,800,100,400,400,200],[800,1000,100,200,800,300],[1000,1200,100,200,1000,400]],
        "CO":[[0,2,50,2,0,0],[2,4,50,2,2,50],[4,14,50,10,4,100],[14,24,50,10,14,150],[24,36,100,12,24,200],[36,48,100,12,36,300],[48,60,100,12,48,400]]
    }
    global adcode_ans
    for adcode in adcode_ans.keys():
        aqi_max = 0
        for item_name in project_name :
            item_value = adcode_ans[adcode][item_name]
            for x in aqi_number[item_name][::-1]:
                if item_value >= x[0]:
                    iaqi = x[2]/x[3]*(item_value-x[4])+x[5]
                    if aqi_max<iaqi:
                        aqi_max = iaqi
                    break
            pass
        aqi_max = round(aqi_max)
        adcode_ans[adcode]["AQI"] = aqi_max

        aqi_rank_score = [0,51,101,151,201,301]
        aqi_rank_name = ["优","良","轻度污染","中度污染","重度污染","严重污染"]
        for i in range(5,-1,-1):
            if aqi_max>=aqi_rank_score[i]:
                adcode_ans[adcode]["AQIRANK"] = aqi_rank_name[i]
            break





def get_all_infomation(a1,a2,a3,b1,b2,b3):
    begin = datetime.date(a1,a2,a3)
    end = datetime.date(b1,b2,b3)
    for i in range((end-begin).days+1):
        day = begin+datetime.timedelta(days=i)
        save_dir = "./data/day_data/{}".format(day.strftime("%Y%m"))
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_path = "./data/day_data/{}/day_{}.json".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        csv_path = "./data/origin_data/{}/CN-Reanalysis-daily-{}00.csv".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        if not os.path.exists(save_path):
            print(save_path)
            get_day_allinfo(save_path=save_path,csv_path=csv_path)
            print(save_path,"ok")


if __name__ == '__main__':
    adcode_info = {}
    with open("adcode_info.json", 'r', encoding='utf-8') as load_f:
        adcode_info = json.load(load_f)
    if len(sys.argv)>1 :
        get_all_infomation(int(sys.argv[1]), int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]))
        pass
    else:
        get_all_infomation(2013,1,1,2018,12,31)

