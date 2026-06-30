from flask import Flask, jsonify
import os
import threading
import fbchat

app = Flask(__name__)

SERVER_NAME = "Satyam Pandey"
DEPLOYED_BY = "Satyam Pandey"

FB_EMAIL = os.environ.get("FB_EMAIL")
FB_PASSWORD = os.environ.get("FB_PASSWORD")
TARGET_GROUP_ID = os.environ.get("GROUP_ID")

class SatyamBot(fbchat.Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        if author_id == self.uid:
            return

        if thread_id == TARGET_GROUP_ID:
            msg_text = message_object.text
            if msg_text:
                anonymous_text = f"👤 Anonymous: {msg_text}\n\n— Secured by {SERVER_NAME}"
                self.send(fbchat.Message(text=anonymous_text), thread_id=thread_id, thread_type=thread_type)

def start_fb_bot():
    try:
        print(f"[{SERVER_NAME}] Logging into Facebook...")
        bot = SatyamBot(FB_EMAIL, FB_PASSWORD)
        print(f"[{SERVER_NAME}] Bot is now listening...")
        bot.listen()
    except Exception as e:
        print(f"Error: {e}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "server_name": SERVER_NAME,
        "status": "Active",
        "deployed_by": DEPLOYED_BY
    })

if __name__ == '__main__':
    threading.Thread(target=start_fb_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
