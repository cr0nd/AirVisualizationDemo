import csv
import datetime
import json
import os


def get_wind_data_by_day(csv_path,save_path):
    project_name = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
    aqi_number = {
        "PM10":[[0,25,50,50,0,0],[50,150,50,100,50,50],[150,250,50,100,150,100],[250,350,50,100,250,150],[350,420,100,70,350,200],[420,500,100,80,420,300],[500,600,100,100,500,400]],
        "PM2.5":[[0,35,50,35,0,0],[35,75,50,40,35,50],[75,115,50,40,75,100],[115,150,50,35,115,150],[150,250,100,100,150,200],[250,350,100,100,250,300],[350,500,100,150,350,400]],
        "SO2":[[0,50,50,50,0,0],[50,150,50,100,50,50],[150,475,50,325,150,100],[475,800,50,325,475,150],[800,1600,100,800,800,200],[1600,2100,100,500,1600,300],[2100,2620,100,520,2100,400]],
        "NO2":[[0,40,50,40,0,0],[40,80,50,40,40,50],[80,180,50,100,80,100],[180,280,50,100,180,150],[280,565,100,285,280,200],[565,750,100,185,565,300],[750,940,100,190,750,400]],
        "O3":[[0,160,50,160,0,0],[160,200,50,40,160,50],[200,300,50,100,200,100],[300,400,50,100,300,150],[400,800,100,400,400,200],[800,1000,100,200,800,300],[1000,1200,100,200,1000,400]],
        "CO":[[0,2,50,2,0,0],[2,4,50,2,2,50],[4,14,50,10,4,100],[14,24,50,10,14,150],[24,36,100,12,24,200],[36,48,100,12,36,300],[48,60,100,12,48,400]]
    }
    ans = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        for index, row in enumerate(reader):
            if index==0:
                continue
            # PM2.5(微克每立方米), PM10(微克每立方米), SO2(微克每立方米), NO2(微克每立方米), CO(毫克每立方米), O3(微克每立方米), U(m/s), V(m/s), TEMP(K), RH(%), PSFC(Pa), lat, lon,
            # lat 纬度 lon 经度
            aqi_max = 0
            for item_index,item in enumerate(project_name):
                item_value = float(row[item_index])
                for x in aqi_number[item][::-1]:
                    if item_value >= x[0]:
                        iaqi = x[2] / x[3] * (item_value - x[4]) + x[5]
                        if aqi_max < iaqi:
                            aqi_max = iaqi
                        break
                pass
            aqi_max = round(aqi_max)
            ans.append([float(row[12]),float(row[11]),aqi_max])
        with open(save_path,'w',encoding='utf-8') as fs:
            json.dump(ans,fs,ensure_ascii=False)
            fs.close()
    return ans


def get_wind_infomation(a1,a2,a3,b1,b2,b3):
    begin = datetime.date(a1,a2,a3)
    end = datetime.date(b1,b2,b3)
    for i in range((end-begin).days+1):
        day = begin+datetime.timedelta(days=i)
        save_dir = "./data/aqi_data/{}".format(day.strftime("%Y%m"))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = "./data/aqi_data/{}/aqi_{}.json".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        csv_path = "./data/origin_data/{}/CN-Reanalysis-daily-{}00.csv".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        if not os.path.exists(save_path):
            print(csv_path)
            get_wind_data_by_day(csv_path=csv_path,save_path=save_path)
            print(save_path,"ok")

if __name__ == '__main__':
    # get_wind_data_by_day("./data/origin_data/201301/CN-Reanalysis-daily-2013010100.csv")
    get_wind_infomation(2013,1,1,2018,12,31)