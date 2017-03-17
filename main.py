#-*-coding:utf8;-*-
#qpy:2
#qpy:console

print "This is console module"

import urllib2,json
import os
import datetime

#魅族天气的api
main_url = "http://aider.meizu.com/app/weather/listWeather?cityIds="
#让用户输入城市名称然后在json查找相关字段的内容
city_name = raw_input("请输入你想查询的城市名称：")

with open('Meizu_city.json') as f:
    city = json.load(f)
with open('Meizu_cities.json') as f:
    cities = json.load(f)

#先搜索这个
def city_list():
    for i in city:
        if i["countyname"].encode('utf-8') == city_name:
            return str(i["areaid"])

#如果上面那个搜索不到就搜索这个
def cities_list():
    for i in cities["cities"]:
        if i["city"].encode('utf-8')==city_name:
            return str(i["cityid"])

def inquire_func(_id):

    #根据城市ID构造URL
    complete_url = main_url + _id
    #加载网页信息
    information = json.load(urllib2.urlopen(complete_url))
    value = information["value"][0]
    
    #创建一个列表存储所有想要的信息
    weatherReport = []
    weatherReport = ["查询时间：".decode('utf-8')+str(datetime.datetime.now())+'\n']

    #省份和城市
    weatherReport.append(value["provinceName"]+' '+value["city"])

    #主要天气信息
    weatherReport.append(u"\n时间：%s" %value["realtime"]["time"])
    weatherReport.append(u"温度：%s" %value["realtime"]["temp"])
    weatherReport.append(u"天气状况：%s" %value["realtime"]["weather"])
    weatherReport.append(u"风向：%s\n" %value["realtime"]["wD"])

    #各项指数信息
    for i in  value["indexes"]:
        weatherReport.append(u"%s：%s。%s" %(i["name"],i["level"],i["content"]))
        
    #主要污染物信息
    main_pollutants = [("\nPM2.5",value["pm25"]["pm25"]),("PM10",value["pm25"]["pm10"]),("SO2",value["pm25"]["so2"]),("O3",value["pm25"]["o3"]),("CO",value["pm25"]["co"]),("NO2",value["pm25"]["no2"])]
    for i,n in main_pollutants:
        weatherReport.append(u"%s浓度：%s" %(i,n))
    
    if not os.path.exist("weather report"):
        os.mkdir("weather report")
    else:
        with open(u"weather report/%s %s.txt" %(value["city"],value["realtime"]["time"]),'w') as f:
            f.write('\n'.join(weatherReport).encode("utf-8"))

if __name__ == "__main__":
    #首先搜索到对应的城市,如果输入“all”就搜索全部城市
    all_city = []
    if city_name == 'all':
        for i in city+cities["cities"]:
            try:
                all_city.append((i["countyname"].encode("utf-8"),str(i["areaid"])))
            except KeyError:
                all_city.append((i["city"].encode("utf-8"),str(i["cityid"])))

        for name,_id in all_city:
            try:
                inquire_func(_id)
                print "It is inquiring the city:",name
            except:
                print "The Query of city("+name+") has no information"
    else:
        _id = city_list()
        if _id == None:
            _id = cities_list()
            if _id == None:
                print "没有找到这个城市，请检查你的输入是否有误"
                exit()
        inquire_func(_id)

