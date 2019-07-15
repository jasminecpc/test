from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,VideoSendMessage,StickerSendMessage
)

app = Flask(__name__)

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    # 回應使用者輸入的話
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
    #訊息回傳圖片
    message=ImageSendMessage(
        original_content_url='https://storage.googleapis.com/www-cw-com-tw/article/201810/article-5bd182cf13ebb.jpg'
         preview_image_url='https://storage.googleapis.com/www-cw-com-tw/article/201810/article-5bd182cf13ebb.jpg'
    )
    line_bot_api.reply_message(event.reply_token,message)
    
    #訊息回傳影片
     message=VideoSendMessage(
        original_content_url='https://example.com/original.mp4',
        preview_image_url='https://exmaple.com/preview.mp4'
    )
    line_bot_api.reply_message(event.reply_token,message)
    #訊息回傳貼圖
    message=StickerSendMessage(
        package_id='1',
        sticker_id='1'
    )
    line_bot_api.reply_message(event.reply_token,message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)
