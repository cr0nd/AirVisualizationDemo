import json
import os


alladcodejson={}


def getjson(adcode=None):
    if (adcode != None):
        adcode = str(adcode)
        path = "./geo/" + adcode + ".json"
        if os.path.exists(path):
            with open(path,'r',encoding='utf-8') as load_f:
                ret = json.load(load_f)
                return ret
    return None


def save_adcode(curr_adcode):
    adcode_json = getjson(curr_adcode)
    # 得到json后，求出三个数据 0.本身的adcode 1.父节点parent的adcode 2.子节点的数量 3.子节点数组 4.level等级 5.acroutes （路由）
    global alladcodejson
    adcode = adcode_json["features"][0]["properties"]["adcode"]
    if (adcode == 100000):
        print(adcode_json["features"][0]["properties"])
    childrenNum = adcode_json["features"][0]["properties"]["childrenNum"]
    childrenArr = []
    if(childrenNum>0) :
        ret = getjson(str(adcode)+'_full')
        for i in range(childrenNum):
            n = ret["features"][i]["properties"]["adcode"]
            childrenArr.append(n)
            save_adcode(n)
    parent = adcode_json["features"][0]["properties"]["parent"]
    if isinstance(parent,str):
        parent = json.loads(parent)["adcode"]
    else:
        parent = parent["adcode"]
        pass
    center = adcode_json["features"][0]["properties"]["center"]
    if isinstance(center,str):
        center = json.loads(center)
    else:
        center = center
        pass
    print(adcode_json["features"][0]["properties"])
    if ("centroid" in adcode_json["features"][0]["properties"]):
        centroid = adcode_json["features"][0]["properties"]["centroid"]
    else:
        centroid = adcode_json["features"][0]["properties"]["center"]
    if isinstance(centroid,str):
        centroid = json.loads(centroid)
    else:
        centroid = centroid
        pass
    alladcodejson[adcode] = {
        'name':adcode_json["features"][0]["properties"]["name"],
        'parent': parent,
        'childrenNum': childrenNum,
        'childrenArr': childrenArr,
        'level':adcode_json["features"][0]["properties"]["level"],
        'center':center,
        'centroid':centroid
    }
    pass


if __name__ == '__main__':
    save_adcode(100000)
    print(alladcodejson)
    with open('adcode_info.json','w',encoding='utf-8') as f:
        json.dump(alladcodejson,f,ensure_ascii=False)
        f.close()