import flask
import json
from flask import request, jsonify,make_response
import MongoData 
import pandas as pd
valid = False

app = flask.Flask(__name__)
#app.config["DEBUG"] = True
mongo = MongoData.mongodata()

@app.route('/')
def home():
    return '''<h1>Smart Helmet Backend</h1>
<p></p>'''

@app.route("/api/valid/<username>/<password>/",methods=['GET'])
def user(username,password):
    data = mongo.userdata(username)
    if data['password']==password:
        print(data)
        valid=True
        df=pd.DataFrame(data, index=[1])
        res=df.drop("_id",axis=1)
        return jsonify(json.loads(res.to_json(orient='records')))
    else:
        valid=False
        return make_response(jsonify({'valid':False}),404)

@app.route("/api/user/<username>/status/<status>",methods=['GET'])
def onthedevice(username,status='on'):
    if status.lower()=='on':
        return jsonify({"status":'on'})
    else:
        return jsonify({'status':'off'})
@app.route("/api/user/<username>/getalcohol",methods=['GET'])
def getalcohol(username):
    
        data = mongo.getAlcohol(username)
        df=pd.DataFrame(data)
        res=df.drop('_id',axis=1).sort_values(by='Time',ascending=True)
        return jsonify(json.loads(res.to_json(orient='records')))
   

if __name__=="__main__":
    app.run(debug=True)
