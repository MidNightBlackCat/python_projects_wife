from pymongo import MongoClient
import emojis
import time
from google.cloud import translate_v2 as translate
translate_client=translate.Client()


newclient = MongoClient("mongodb://localhost:27017")
mydb = newclient["jin_ri_news_1"]
collectionarray = mydb.list_collection_names()


def translate_comment(col):
    print('开始%s翻译'% col)
    collection = mydb[col]
    collection.update_many({}, {'$set': {'Comment_English': 'none'}})
    querry = {"Comment_English": 'none'}
    comment_array = collection.find({}, {'comment_text': 1})
    print('已获取所有评论，准备开始翻译')
    for i in comment_array:
        ch_comment = emojis.decode(i['comment_text'])
        result=translate_client.translate(ch_comment,target_language='en')
        collection.update_one(querry, {'$set': {'Comment_English': result['translatedText']}})
def modify_date(coldb):
        date_time=coldb.find({},{'creat_time':1})
        for item in date_time:
            creat_time=item['creat_time']
            n_date=time.localtime(creat_time)
            for_date=time.strftime("%Y-%m-%d",n_date)
            coldb.update_one({'creat_time':creat_time},{'$set':{'creat_time':for_date}})
i = 1
for col in collectionarray:
    translate_comment(col)
    print('已经完成%d个库评论数据翻译' % i)
    i += 1


