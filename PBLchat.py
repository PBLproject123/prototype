 
from google_trans_new import google_translator
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from twilio.rest import Client

###########################3  TWILIO API for sending messages  ############### 
account_sid = 'AC33dbd106a71d73880871ff03888ef5fd'
auth_token = 'ee8d4e1aaa2fa39ec120b021ef8a6126'
client = Client(account_sid, auth_token) 

def sendtxt(message , person="7666779269"):      #paste your whatsapp number here
    message = client.messages.create( 
                                  from_='whatsapp:+14155238886',  
                                  body= message,      
                                  to='whatsapp:+91{}'.format(person) 
                              )



    
#######################    translate from one to other language  #################

def hinglish(sent,src="en",dest="mr"):
    translator = google_translator()
    result = translator.translate(sent, lang_src=src,lang_tgt=dest)
    return result





#################  members on group   ############################

groupdata = {"7666779269":{"name":"Mayuresh Khanaj","lang_code":"en"},
             "7028712174":{"name":"Aarkin","lang_code":"mr"},
             "9075118158":{'name':'rupesh','lang_code':'hi'},
            '7558404927':{'name':'avdhut','lang_code':'te'},
            '9764049370':{'name':'iliyaas','lang_code':'ur'}
             }




#######################  process of translation  ############################

def trans_msg(msg , sender ,lang_codeof=groupdata ):
    sender = sender[3:]
    sam =  "*"+lang_codeof[sender]['name']+"*"
    for i in lang_codeof:
        if i != sender:
            new_text = sam+" \n" + hinglish(msg,lang_codeof[sender]['lang_code'] ,lang_codeof[i]['lang_code']  )
            sendtxt(new_text,i)



########################## FLASK  APP STARTS HERE  ##########################

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"
 
@app.route("/sms", methods=['POST'])
def sms_reply():
    msg = request.form.get('Body').lower()
    am = msg
    remote_number = request.values.get("From", "").split(":")[1]    
    return trans_msg(am,remote_number)

if __name__ == "__main__":
    app.run(debug=True)
