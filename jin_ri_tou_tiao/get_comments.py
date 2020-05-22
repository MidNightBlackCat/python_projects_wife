import requests
import pymongo
import json
from urllib.parse import urlencode


newclinent = pymongo.MongoClient("mongodb://localhost:27017")
mydb = newclinent["jin_ri_news_1"]


def name_col(num):
    mycol = mydb["comments_" + str(num)]
    return mycol


def handle_url(url):
    header = {
        "accept": "text/javascript, text/html, application/xml, text/xml, */*",
        "accept - encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en;q=0.9,zh;q=0.8,zh-CN;q=0.7,zh-TW;q=0.6,ja;q=0.5",
        "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    response = requests.get(url, headers=header)
    return (response)


def handle_response(url):
    break_for = True
    response = handle_url(url)
    response_json = json.loads(response.text)
    if (len(response_json["data"]) == 0):
        print("评论已经获取完毕！！")
        return break_for
    else:
        for item in response_json["data"]:
            comment = {}
            comment['id'] = item["comment"]["id"]
            comment['username']=item["comment"]["user_name"]
            comment["comment_text"] = item["comment"]["text"]
            comment["reply_count"] = item["comment"]["reply_count"]
            comment["digg_count"] = item["comment"]["digg_count"]
            comment["creat_time"] = item["comment"]['create_time']
            mycol.insert_one(comment)
        print("已经完成20次数据库写入")


def handle_comment_url(id):
    for a in range(0, 80, 20):
        param_data = {
            "group_id": id,
            "item_id": id,
            "offset": a,
            "count": 20
        }
        url = "https://www.toutiao.com/article/v2/tab_comments/?aid=24&app_name=toutiao-web&" + urlencode(param_data)
        result = handle_response(url)
        if result:
            break


num = input("please input number:")
id = input("please input id:")
mycol = name_col(num)
handle_comment_url(id)
