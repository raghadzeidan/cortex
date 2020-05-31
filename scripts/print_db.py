import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient(host="my_mongo",port=27017)
    db = client.db
    users = db.users

    results = users.find({})
    for result in results:
        print(result)
