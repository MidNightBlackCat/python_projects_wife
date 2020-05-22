import pandas as pd
from pymongo import MongoClient


def read_mongo():
    newclinent = MongoClient("mongodb://localhost:27017")
    mydb = newclinent["jin_ri_news_1"]
    collection_array=mydb.list_collection_names()

    for name in collection_array:
        cursor = mydb[name].find({})
        file_path=str(name)+".csv"
        df =  pd.DataFrame(list(cursor))
        if '_id' in df:
            del df['_id']
        df.to_csv(file_path, encoding="utf_8_sig")


if __name__ == '__main__':
    read_mongo()
