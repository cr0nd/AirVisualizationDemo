import csv
import datetime
import json
import os


def get_wind_data_by_day(csv_path,save_path):
    ans = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        for index, row in enumerate(reader):
            if index==0:
                continue
            # PM2.5(微克每立方米), PM10(微克每立方米), SO2(微克每立方米), NO2(微克每立方米), CO(毫克每立方米), O3(微克每立方米), U(m/s), V(m/s), TEMP(K), RH(%), PSFC(Pa), lat, lon,
            # lat 纬度 lon 经度
            ans.append([float(row[12]),float(row[11]),float(row[0])])
        with open(save_path,'w',encoding='utf-8') as fs:
            json.dump(ans,fs,ensure_ascii=False)
            fs.close()
    return ans

def get_wind_infomation(a1,a2,a3,b1,b2,b3):
    begin = datetime.date(a1,a2,a3)
    end = datetime.date(b1,b2,b3)
    for i in range((end-begin).days+1):
        day = begin+datetime.timedelta(days=i)
        save_dir = "./data/pm2.5_data/{}".format(day.strftime("%Y%m"))
        if not os.path.exists(save_dir):
            os.mkdirs(save_dir)
        save_path = "./data/pm2.5_data/{}/pm2.5_{}.json".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        csv_path = "./data/origin_data/{}/CN-Reanalysis-daily-{}00.csv".format(day.strftime("%Y%m"),day.strftime("%Y%m%d"))
        if not os.path.exists(save_path):
            print(csv_path)
            get_wind_data_by_day(csv_path=csv_path,save_path=save_path)
            print(save_path,"ok")

if __name__ == '__main__':
    # get_wind_data_by_day("./data/origin_data/201301/CN-Reanalysis-daily-2013010100.csv")
    get_wind_infomation(2013,1,1,2018,12,31)