import datetime
import pymongo
import random


class mongodata():
    def __init__(self):
        self.db = pymongo.MongoClient("mongodb://smarthelmet:dhanushp@cluster0-shard-00-00.ok7zk.mongodb.net:27017,cluster0-shard-00-01.ok7zk.mongodb.net:27017,cluster0-shard-00-02.ok7zk.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-96d086-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.helmet=self.db['helmet']
        self.valid = False
        
    def getAlcohol(self,userid):
        l=[]
        alco=self.helmet['alcohol']
        quey = {"userid":userid}
        for x in alco.find(quey):
            l.append(x)
        return l
    def addalcoholtodb(self,userid='12345',bike='KA-51-Y-2369',value=None):
        d={'userid':userid,'bikeid':bike,'value':value,'COL':'high','SOM':True,'Time':datetime.datetime.utcnow()}
        value = self.helmet['alcohol']
        idx=value.insert_one(d)
        return idx.inserted_id
    def userdata(self,userid):
        l=[]
        value = self.helmet['users']
        myuser = value.find({"UserID":userid})
        if myuser is None:
            self.valid = False
        for x in myuser:
            l.append(x)
        return l
    
