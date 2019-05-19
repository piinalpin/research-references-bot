from bot import ChatBot
from search_engine import Engine
from tensor_flow import TensorFlow

update_id = None
resp = TensorFlow(intents="docs/intents.json")


def make_reply(msg):
    txt = None
    if msg is not None:
        txt = resp.response(msg)
    return txt


while True:
    print("....")
    bot = ChatBot("config.cfg")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                if "message" in item:
                    message = item["message"]["text"]
                else:
                    message = item["edited_message"]["text"]
            except:
                message = None
            try:
                from_ = item["message"]["from"]["id"]
            except:
                from_ = item["edited_message"]["from"]["id"]
            text = message.partition("tentang")
            if "tentang" not in text:
                reply = make_reply(message)
                bot.send_message(reply, from_)
            else:
                query = Engine(query=text[2].lstrip())
                dictionary = query.get_scores()
                for i in range(len(dictionary["author"])):
                    author = list(dictionary["author"])[i].lstrip()
                    title = list(dictionary["title"])[i].lstrip()
                    url = list(dictionary["url"])[i].lstrip()
                    year = list(dictionary["year"])[i]
                    score = float(list(dictionary["score"])[i])
                    msg = "*Author:* {}%0D%0A*Title:* {}%0D%0A*Url:* {}%0D%0A*Year:* {}".format(author, title, url, year)
                    bot.send_message(msg, from_)
