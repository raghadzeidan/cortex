import pymongo

if __name__ == "__main__":
    client = pymongo.MongoClient()
    db = client.db
    users = db.users

    users.delete_many({})
