import datetime
import pymongo
import random


class mongodata():
    def __init__(self):
        self.db = pymongo.MongoClient("mongodb://smarthelmet:dhanushp@cluster0-shard-00-00.ok7zk.mongodb.net:27017,cluster0-shard-00-01.ok7zk.mongodb.net:27017,cluster0-shard-00-02.ok7zk.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-96d086-shard-0&authSource=admin&retryWrites=true&w=majority")
        self.helmet=self.db['helmet']
        self.valid = False
        
    def getAlcohol(self,userid):
        alco=self.helmet['alcohol']
        quey = {"userid":userid}
        return alco.find_one(quey)
        
    def addalcoholtodb(self,userid,loc,alert,bike='KA-51-Y-2369',value=None):
        d={'value':value,'loc':loc,'alert':alert,'Time':datetime.datetime.utcnow()}
        value = self.helmet['alcohol']
        if value.find_one({"userid":userid})==None:
            d1={"userid":userid,"bike":bike,"Alcoholdata":[d]}
            idx=value.insert_one(d1)
            return idx.inserted_id
        else:
            idx=value.update({'userid': userid}, {'$push': {'Alcoholdata': d}})
            return idx
    def getuser(self,userid):
        db = self.helmet['users']
        user = db.find_one({"userid": userid})
        return user
    def userdata(self,userid):
        value = self.helmet['users']
        myuser = value.find_one({"email":userid})
        if myuser is None:
            self.valid = False
        return myuser

    
    def setstatus(self,user,value,device):
        col = self.helmet.get_collection("status_check")
     
        query = {"userid":str(user)}
        device1 = str(device).lower()
        newvalues = { "$set": { device1 : value, "Time":datetime.datetime.utcnow() } }
        col.update_one(query,newvalues,upsert=True)
    def getstatus(self,user):
        col = self.helmet.get_collection("status_check")
     
        query = {"userid":str(user)}
        val=col.find_one(query)
        #print(val)
        return val
    def MessageSaved(self,msg,status,user,time):
        db = self.helmet['Message']
        userdb = self.helmet['users']
        user1  = userdb.find_one({"userid":user})
        message = {"recipt":msg,"time":time,"status":status,"to":user1['parent']}
        if user1==None:
            
            d= {'user':user1['Name'],"userid":user1['userid'],"message":[message]}
            idx = db.insert_one(d)
        else:
            idx= db.update({'userid': user}, {'$push': {'message': message}})
        return idx

    def DeleteparentContact(self,user,contact):
        if len(contact)==10:
            db = self.helmet['users']
            idx=db.update({"userid":user},{"$pull":{"parent":contact}})
            if idx['updatedExisting']==True:
                return idx
            else:
                return "invalid number"
        else:
            return "invalid number"
    def AddparentContact(self,user,contact):
        if len(contact)==10:
            db = self.helmet['users']
            idx=db.update({"userid":user},{"$push":{"parent":contact}})
            if idx['updatedExisting']==True:
                return idx
            else:
                return "invalid number"
        else:
            return "invalid number"
    def ChangeMyContact(self,user,contact):
        if len(contact)==10:
            db=self.helmet['users']
            idx = db.update({"userid":user},{ "$set": {"contact":contact} })
            if idx['updatedExisting']==True:
                return idx
            else:
                return "invalid number"
        else:
            return "invalid number"


    def UpdateLocation(self,user,lat,log):
        db = self.helmet['users']
        idx = db.update({"userid":user},{"$set":{"lat":lat,"log":log}})
        return idx

    def getlocation(self,user):
        db = self.helmet['users']
        user = db.find_one({"userid":user})
        if user == None:
            return None
        return user['lat'],user['log']
    
    def getMessage(self,user):
        db = self.helmet['Message']
        user = db.find_one({"userid":user})
        return user
