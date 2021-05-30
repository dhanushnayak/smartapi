# mention url
# import required module
import requests
import json
import datetime
import MongoData
import os
class Sms():
    def __init__(self,msg,user):
        db = MongoData.mongodata()
        self.user =  db.getuser(user)
        self.msg = msg
        self.location = "https://maps.google.com?q={},{}".format(self.user['lat'],self.user['log'])
        self.contact = self.user['parent'][:3]
        self.time = datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        path = "Keysshmet.txt"
        with open(path) as file:
            self._key=file.read()
            
    def Send(self):
        url = "https://www.fast2sms.com/dev/bulk"

        my_data = {
            # Your default Sender ID
            'sender_id': 'TXTIND',

            # Put your message here!
            'message': '{} at {},{},{},in-{}'.format(self.msg,self.time,self.user['Name'],self.user['contact'],self.location),

            'language': 'english',
            'route': 'p',
            #'numbers':  '{},{},{},{}'.format(*self.contact,self.user['contact'])
            'numbers':  '8310210801'
        }
        print(my_data)
        headers = {
                'authorization': self._key,
                'Content-Type': "application/x-www-form-urlencoded",
                'Cache-Control': "no-cache"
            }
            # make a post request
        response = requests.request("POST",url,data = my_data,headers = headers)
            #load json data from source
        returned_msg = json.loads(response.text)

            # print the send message
        if returned_msg['message'][0]=='SMS sent successfully.':
            return True,self.time
        else:
            return False,self.time