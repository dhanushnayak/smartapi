import flask
import json
from flask import request, jsonify
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

@app.route("/api/user/<username>/<password>/valid",methods=['GET'])
def user(username,password):
    data = mongo.userdata(username)
    if data['password']==password:
        valid=True
        df=pd.DataFrame(data)
        return jsonify(json.loads(df.to_json(orient='records')))
    else:
        valid=False
        return jsonify({'valid':False})

@app.route("/api/user/<username>/getalcohol",methods=['GET'])
def getalcohol(username):
    
        data = mongo.getAlcohol(username)
        df=pd.DataFrame(data)
        res=df.drop('_id',axis=1).sort_values(by='Time',ascending=False)
        return jsonify(json.loads(res.to_json(orient='records')))
   

if __name__=="__main__":
    app.run(debug=True)