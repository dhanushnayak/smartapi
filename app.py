import flask
import json
from flask import request, jsonify,make_response
import MongoData 
from sms import Sms
import pandas as pd
valid = False

app = flask.Flask(__name__)
app.config["DEBUG"] = True

mongo = MongoData.mongodata()
i=0
@app.route('/')
def home():
    return '''<h1>Smart Helmet Backend</h1>
<p></p>'''

@app.route("/api/valid/<username>/<password>/",methods=['GET'])
def user(username,password):
    data = mongo.userdata(username)
    print(data)
    if data['password']==password:
        valid=data
        data.pop("_id")
        return jsonify(data)
    else:
        valid=False
        return make_response(jsonify({'valid':False}),404)

@app.route("/api/user/<username>/status/<device>/<status>",methods=['GET'])
@app.route("/api/user/<username>/status/",methods=['GET'])
def onthedevice(username,device=None,status=None):
    if status is not None:
        if status.lower()=='on':
            mongo.setstatus(username,value=status,device=device.lower())
            d = mongo.getstatus(username)
            if d is None:
                return make_response(jsonify({'valid':False}),404)
            df = pd.DataFrame([d]).drop('_id',axis=1).to_json(orient='records')
            print("Data Frame = ",df)
            return jsonify(json.loads(df)[0])
        else:
            mongo.setstatus(username,value=status,device=device.lower())
            d = mongo.getstatus(username)
            if d is None:
                return make_response(jsonify({'valid':False}),404)
            df = pd.DataFrame([d]).drop('_id',axis=1).to_json(orient='records')
            print("Data Frame = ",df)
            return jsonify(json.loads(df)[0])
    else:
            d = mongo.getstatus(username)
            if d is None:
                return make_response(jsonify({'valid':False}),404)
            df = pd.DataFrame([d]).drop('_id',axis=1).to_json(orient='records')
            print("Data Frame = ",df)
            return jsonify(json.loads(df)[0])

@app.route("/api/user/<username>/falldetect/<status>/<speed>",methods=['GET']) 
def sendsms(username,status,speed):
    speed1 = int(speed)
    msg1=''
    print(status)
    if status == 'on':
        if speed1 >= 50 and speed1 <= 60:
            msg1 = "falldetected with moderate risk"
        elif speed1 > 60:
            msg1 = "falldetected with high risk"
        elif speed1 < 50:
            msg1 = "falldetected with low risk"
        print(speed1, msg1)
        sms1 = Sms(msg=msg1,user=username)
        send_status =  sms1.Send()
        if send_status[0]:
            if mongo.MessageSaved(msg=msg1,user=username,status=True,time=send_status[1]) != None:
                return jsonify({'sent':msg1})
        
    return make_response(jsonify({"msg":msg1}),404)
                
@app.route("/api/user/<username>/update/number/<number>",methods=['GET']) 
def changemynumber(username,number):
    if mongo.ChangeMyContact(username,number)=='invalid number':
        return make_response(jsonify({'valid':False,"number":number}),404)
    else:
        return jsonify({"Number":number})

@app.route("/api/user/<username>/add/number/<number>",methods=['GET']) 
def addnumber(username,number):
    if mongo.AddparentContact(username,number)=='invalid number':
        return make_response(jsonify({'valid':False,"number":number}),404)
    else:
        return jsonify({"Number":number,"added":True})    

@app.route("/api/user/<username>/delete/number/<number>",methods=['GET']) 
def deletenumber(username,number):
    if mongo.DeleteparentContact(username,number)=='invalid number':
        return make_response(jsonify({'valid':False,"number":number}),404)
    else:
        return jsonify({"Number":number,"added":True})    

@app.route("/api/user/<username>/getlocation",methods=['GET'])
def getlocation(username):
    user = mongo.getlocation(username)
    if user!=None:
        return jsonify({"lat":user[0],"log":user[1]})
    else:
        return make_response(jsonify({'valid':False}),404)

@app.route("/api/user/<username>/update/location/<lat>/<log>",methods=['GET'])
def updatelocation(username,lat,log):
    if mongo.UpdateLocation(user=username,lat=lat,log=log) != None:
        return jsonify({"Update":"Done","Lat":lat,"log":log})
    else:
        return make_response(jsonify({'valid':False}),404)

               
@app.route("/api/user/<username>/getalcohol",methods=['GET'])
def getalcohol(username):
        data = mongo.getAlcohol(username)
        data.pop('_id')
        return jsonify(data)


