import flask
import json
from flask import request, jsonify
import MongoData 
import pandas as pd
valid = False

app = flask.Flask(__name__)
app.config["DEBUG"] = True
mongo = MongoData.mongodata()

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Smart Helmet Backend</h1>
<p></p>'''

@app.route("/api/user/<username>/<password>/",methods=['GET'])
def user(username,password):
    data = mongo.userdata(username)
    if data['password']==password:
        valid=True
        return jsonify({'valid':True})
    else:
        valid=False
        return jsonify({'valid':False})

@app.route("/api/user/<username>/getalco",methods=['GET'])
def getalcohol(username):
    
        data = mongo.getAlcohol(username)
        df=pd.DataFrame(data)
        res=df.drop('_id',axis=1).sort_values(by='Time',ascending=False)
        return jsonify(json.loads(res.to_json(orient='records')))
   

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5001,debug=True)
