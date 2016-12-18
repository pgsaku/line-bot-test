from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import(
    InvalidSignatureError
)
from linebot.models import(
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi(os.environ.get('LINEBOT_CHANNEL_TOKEN'))
handler = WebhookHandler(os.environ.get('LINEBOT_CHANNEL_SECRET'))

app = Flask(__name__)

@app.route('/callback', methods=['POST'])
def collback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)

    received_text = event.message.text

    send_text = profile.display_name + 'さん hello world'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=send_text)
    )

if __name__ == '__main__':
    app.run()
