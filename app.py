from flask import Flask, request
import bot
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/python-flask/webhook/facebook', methods = ['GET'])
def facebookWebhookVerify():
    params = request.args.to_dict()
    mode = params["hub.mode"]
    token = params["hub.verify_token"]
    challenge = params["hub.challenge"]
    if (mode and token) :
        if (mode == "subscribe" and token == os.getenv('VERIFYTOKEN')) :
            print("WEBHOOK_VERIFIED")
            return challenge
        else :
            return {}, 403
 
@app.route('/python-flask/webhook/facebook', methods = ['POST'])
def facebookWebhook():
    body = request.json
    if(len(body.get('entry')) and body.get('entry')[0]["changes"]) :
        changes = body.get('entry')[0]["changes"]
        message = changes[0]["value"]["messages"][0] if 'messages' in changes[0]["value"] else False
        if message and message["type"] == "text" :
            message_to_send = bot.OpenArtificialIntelligence(message["text"]["body"])
            bot.sendTextMessage(message_to_send)
    return 'Hello GandS!'
 
if __name__ == '__main__':

    app.run()