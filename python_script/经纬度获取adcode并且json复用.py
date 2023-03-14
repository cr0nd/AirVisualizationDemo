import csv
import json
import os
import requests

reverse_geocoding_adcode_json = {}


def reverse_geocoding_load_json():
    path = "./reverse_geocoding.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as load_f:
            global reverse_geocoding_adcode_json
            reverse_geocoding_adcode_json = json.load(load_f)
    pass


def reverse_geocoding_save_json():
    with open('./reverse_geocoding.json','w',encoding='utf-8') as f:
        json.dump(reverse_geocoding_adcode_json,f,ensure_ascii=False)
        f.close()
    pass


def reverse_geocoding_adcode(lat, lon):
    latlonkey = str.strip(lat) + ',' + str.strip(lon)
    global reverse_geocoding_adcode_json
    if latlonkey in reverse_geocoding_adcode_json.keys():
        return reverse_geocoding_adcode_json[latlonkey]
    f = reverse_geocoding_by_baiduapi(lat, lon)
    reverse_geocoding_adcode_json[latlonkey] = f
    return f


def reverse_geocoding_by_baiduapi(a, b):
    # print("正在调用百度API")
    origin_url = """here is your apicode"""
    lat = str.strip(a)
    lon = str.strip(b)
    url = origin_url.format(lat, lon)
    r = requests.get(url)
    j = r.json()
    # 返回值
    # nj = {
    #     'adcode':j['result']['addressComponent']['adcode'],
    #     'province':j['result']['addressComponent']['province'],
    #     'district':j['result']['addressComponent']['district'],
    #     'city': j['result']['addressComponent']['city'],
    #     'city_level': j['result']['addressComponent']['city_level'],
    # }
    return j['result']['addressComponent']['adcode']
    pass


def test():
    with open('./data/origin_data/201301/CN-Reanalysis-daily-2013010100.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        reader = list(reader)
        for index, row in enumerate(reader):
            if(index<45000):
                temp = reverse_geocoding_adcode((row[11]), (row[12]))
                if(index % 50 ==0):
                    print(index)


reverse_geocoding_load_json()


if __name__ == '__main__':
    reverse_geocoding_load_json()
    test()
    l =(reverse_geocoding_adcode_json.__len__())
    print(l)
    print(reverse_geocoding_adcode_json)
    # reverse_geocoding_save_json()
