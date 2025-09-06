from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import get_response  # your chatbot module

# Flask app
app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    reply = get_response(incoming_msg)
    resp.message(reply)
    return str(resp)

if __name__ == "__main__":
    print("🚀 Flask WhatsApp bot running on http://127.0.0.1:5000")
    print("👉 Remember: run ngrok separately with `ngrok http 5000`")
    app.run(port=5000)
