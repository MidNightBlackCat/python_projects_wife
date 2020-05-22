import pymongo
import pkuseg
import os
import codecs
import re
from collections import Counter

myclient=pymongo.MongoClient("mongodb://localhost:27017")
mydb=myclient["jin_ri_news_1"]
mycol=mydb["comments_2"]
comments_text=mycol.find({},{"comment_text":1})
comments_list=[]

root_path=os.getcwd()
stop_word_file='stopword.txt'
stop_file_path=os.path.join(root_path,stop_word_file)

for item in comments_text:
    text=item['comment_text']
    comments_list.append(text)
comments_collection="".join(comments_list)

seg=pkuseg.pkuseg(model_name='web',user_dict='user_dict.txt')
seg_text=seg.cut(comments_collection)
clear_text=[]
with codecs.open(stop_file_path,'r',encoding="utf-8") as f:
    stop_words=f.read()
stop_list=stop_words.split("\n")
for word in seg_text:
    if(len(word)>1):
        if word not in stop_list:
            clear_text.append(word)
countor=Counter(clear_text)
print(countor.most_common(50))
