# LINEでオウム返し
from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage,
)

app = Flask(__name__)

#環境変数取得
# 予めheroku側で変数を設定する必要あり。heroku cliコマンド heroku config:set ・・・
# またはログインしてSettings → Config Varsから設定
# 重要！：肝心の設定値はLINE Developersにログイン後、以下の値をコピーして設定
# チャンネル基本設定 → チャンネルシークレット
# Messaging API設定 → チャネルアクセストークン
# 以上の設定を予めした上で↓の設定が有効となる
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# GET ブラウザから直接アクセスしてきた場合
@app.route("/")
def hello_world():
    return "hello world!"

# POST /callback はLINE DevelopersのWebhook設定したURL つまり LINE側から呼び出される
## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # requestの受信
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'
 
## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。

# message=TextMessage が テキスト受信時のイベント
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # event.message.text = ユーザが送信したメッセージ内容
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。
 
# message=TextMessage が 画像受信時のイベント
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("画像の対応はまだよ"))

# main関数
if __name__ == "__main__":
    # ポート番号の設定
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
