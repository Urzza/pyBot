from bson import ObjectId
from pymongo import MongoClient

class Tag:
    dbName = "pyBot"
    host = "localhost"
    port = 27017
    collectionName = "tags"
    
    client = MongoClient(host, port)
    db = client[dbName]

    def __init__(self, tagName, url = None):
        res = self.db[self.collectionName]\
                  .find_one({"name" : tagName})
        print(res)
        if res:
            self.name = res["name"]
            self.id = res["_id"]
            print(res["urls"])
            if not url:
                self.urls = res["urls"]
                self.status = "clear"
            else:
                self.urls = url
                self.status = "dirty"
        else:
            self.id = ObjectId()
            self.name = tagName
            self.urls = url
            self.status = "dirty"
                    
    def __update_one(self, *args):
        self.db[self.collectionName].update_one(*args)
        
    def save(self):
        if self.status is "dirty":
            self.__update_one({"name" : self.name},\
                              {"$push" : {"urls" : self.urls}},\
                              True)
            self.status = "clear"
            return "saved"
        else:
            print("status: %s" % self.status)
            return "duplicate"

    def show(self):
        return self.urls
        
    @classmethod
    def showAll(cls):
        return cls.db[cls.collectionName].find({})
