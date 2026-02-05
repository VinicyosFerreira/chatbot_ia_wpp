import os
from decouple import config
from flask import Flask ,request, jsonify

os.environ["PHONE_NUMBER1"] = config("PHONE_NUMBER1")
os.environ["PHONE_NUMBER2"] = config("PHONE_NUMBER2")

app = Flask(__name__)

from services.waha import Waha
from bot.ai_bot import AiBot


@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/chatbot/webhook/', methods=['POST'])
def webhook(): 
    
    data = request.json
    print("Received data", data)

    waha = Waha()
    ai_bot = AiBot()
    chatId = data['payload']['from']
    received_message = data['payload']['body']

    allowed_chat_ids = {os.environ["PHONE_NUMBER1"], os.environ["PHONE_NUMBER2"]}
   
    if chatId in allowed_chat_ids:
        history_message = waha.get_history_messages(chatId=chatId, limit=10)
        response_message = ai_bot.invoke(history_message, received_message)
        waha.send_message(chatId=chatId, message=response_message)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__': 
    app.run(debug=True, port=5000, host="0.0.0.0")


