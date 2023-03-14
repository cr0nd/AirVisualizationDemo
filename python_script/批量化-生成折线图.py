# 指定adcode 获取某天的所有数据

# 指定adcode 获取


# 测试 指定adcode 和 时间的年月日范围，获取所有数据
import datetime
import json
import os


def get_all_aqi_information(adcode, item_name, a1, a2, a3, b1, b2, b3):
    print(adcode)
    save_path = "./data/line_aqi_data/line_aqi_{}.json".format(adcode)
    if os.path.exists(save_path):
        return
    ans = []
    begin = datetime.date(a1, a2, a3)
    end = datetime.date(b1, b2, b3)
    for i in range((end - begin).days + 1):
        day = begin + datetime.timedelta(days=i)
        load_dir = "./data/day_data/{}".format(day.strftime("%Y%m"))
        day_str = day.strftime("%Y-%m-%d")
        load_file = load_dir + "/day_{}.json".format(day.strftime("%Y%m%d"))
        with open(load_file, "r", encoding="utf-8") as f:
            ret = json.load(f)
            val = ret[str(adcode)][item_name]
            ans.append([day_str, val])

    if not os.path.exists(save_path):
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(ans, f, ensure_ascii=False)
    print(adcode,"ok")
    return ans


adcode_info = {}

def get_adcode_info_childrenNum(adcode):
    return (adcode_info[str(adcode)]["childrenNum"])

def get_adcode_info_childrenArr(adcode):
    return (adcode_info[str(adcode)]["childrenArr"])


def get_children_infomation(adcode,item_name, a1, a2, a3, b1, b2, b3,level):
    get_all_aqi_information(adcode, item_name, a1, a2, a3, b1, b2, b3)
    if (level>3):
        # 大于1表示精确到省
        # 大于2精确到省的下一级，一般是市，直辖市是区
        return None
    arr = get_adcode_info_childrenArr(adcode)
    for i in arr:
        get_all_aqi_information(i, item_name, a1, a2, a3, b1, b2, b3)
        # 开始递归
        get_children_infomation(i, item_name, a1, a2, a3, b1, b2, b3, level+1)


if __name__ == '__main__':
    adcode_info = {}
    with open("adcode_info.json", 'r', encoding='utf-8') as load_f:
        adcode_info = json.load(load_f)


    get_children_infomation(100000,"AQI",2013,1,1,2018,12,31,level=1)
    # ret = get_all_aqi_information(310000,"AQI",2013,1,1,2018,12,31)
