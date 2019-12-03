import os
from flask import Flask, request, abort, send_file

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

# constant
IMAGE_DIR = 'img'

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print('Invalid signature. Please check your channel access token/channel secret.')
        abort(400)
    except Exception as e:
        print(e)

    return 'OK'

@app.route('/image')
def get_image():
    img_id = request.args.get('id')
    if not img_id:
        return 'no id passed!', 400
    return send_file(f'./{IMAGE_DIR}/{img_id}.jpg', mimetype='image/jpeg')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message_2(event: MessageEvent):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=f'{os.environ.get("BASE_URL")}/image?id=001',
            preview_image_url=f'{os.environ.get("BASE_URL")}/image?id=001'
        )
    )