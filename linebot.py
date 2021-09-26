import json
from linebot import LineBotApi
from linebot.models import TextSendMessage

# JSONファイル読み込み
file = open('info.json', 'r')
info = json.load(file)

@app.route("/")
def hello_world():
    return "hello world!"

CHANNEL_ACCESS_TOKEN = info['CHANNEL_ACCESS_TOKEN']
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

def main():
    USER_ID = info['USER_ID']
    messages = TextSendMessage(text="テスト")
    line_bot_api.push_message(USER_ID, messages=messages)

# メイン関数呼び出し
if __name__ == "__main__":
    main()
