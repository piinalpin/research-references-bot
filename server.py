from bot import ChatBot
from search_engine import Engine
from tensor_flow import TensorFlow
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os


app = Flask(__name__)

line_bot_api = LineBotApi('dV+nd/GrdLaiKnQ1plwe8QuJ08HE6KSoccIzJxvJO7hx2TSE1QF4mS51TUYlxYr7o0q0pUvnaEchYl1phF75ZYoNaVoEnt+z4wEaEOgI7+rtxxJd6njG9HKsZK2Aj1fKU5iGtWQMq+zYRJLosfNXKgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('44ea69c0b9b62849571e363d93e53127')
resp = TensorFlow(intents="docs/intents.json")


def make_reply(msg):
    txt = None
    if msg is not None:
        txt = resp.response(msg)
    return txt


@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """
    text = event.message.text
    text = text.partition("tentang")
    if "tentang" not in text:
        reply = make_reply(text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply))
    else:
        query = Engine(query=text[2].lstrip())
        dictionary = query.get_scores()
        for i in range(len(dictionary["author"])):
            author = list(dictionary["author"])[i].lstrip()
            title = list(dictionary["title"])[i].lstrip()
            url = list(dictionary["url"])[i].lstrip()
            year = list(dictionary["year"])[i]
            msg = "*Author:* {}%0D%0A*Title:* {}%0D%0A*Url:* {}%0D%0A*Year:* {}".format(author, title, url, year)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
