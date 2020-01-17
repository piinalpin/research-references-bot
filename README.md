# Reference Research Bot
This project will create search engine bot on telegram using TF IDF and Cosine Similarity.

![Chat Bot](https://raw.githubusercontent.com/piinalpin/research-references-bot/master/docs/chatbot.gif)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Make sure you have installed Python 3 on your device

### File Structure

1. [bot.py](https://github.com/piinalpin/research-references-bot/blob/master/bot.py) this file to serve get updates and send message from request
2. [config.cfg](https://github.com/piinalpin/research-references-bot/blob/master/config.cfg) token telegram bot from Bot Father
3. [database.py](https://github.com/piinalpin/research-references-bot/blob/master/database.py) define database structure with object oriented mapping
4. [search_engine.py](https://github.com/piinalpin/research-references-bot/blob/master/search_engine.py) custom library to get result of cosine similarity document
5. [server.py](https://github.com/piinalpin/research-references-bot/blob/master/server.py) serve message and result from engine
6. [tensor_flow.py](https://github.com/piinalpin/research-references-bot/blob/master/tensor_flow.py) natural language processing for greeting response
7. [intents.json](https://github.com/piinalpin/research-references-bot/blob/master/docs/intents.json) greeting or intents json data

### Step for get dataset
1. Scraping data from http://digilib.uad.ac.id/penelitian/Penelitian/index see on [Scrapping.ipynb](https://github.com/piinalpin/research-references-bot/blob/master/docs/Scrapping.ipynb)
2. Update dataset

### How To Run
1. Install requirement
```
pip install -r requirements.txt
```
2. Install `punkt` with `nltk.download()`
```
>>> import nlit
>>> nltk.download("punkt")
```
3. Run `server.py`
```
python server.py
```
4. Go to Telegram Application or access from Telegram Web, then chat with this bot.

## Built With

* [Python 3](https://www.python.org/download/releases/3.0/) - The language programming used
* [Virtualenv](https://virtualenv.pypa.io/en/latest/) - The virtual environment used
* [SQL Alchemy](https://www.sqlalchemy.org/) - The database library
* [NLTK](https://pypi.org/project/nltk/) - Natural Language Toolkit
* [Tensor Flow](https://pypi.org/project/tensorflow/) - Tensor Flow
* [Tf Learn](https://pypi.org/project/tflearn/) - Tensor flow for learning
* [Scikit Learn](https://pypi.org/project/sklearn/) - Scikit Learn use Cosine Similarity

## Clone or Download

You can clone or download this project
```
> Clone : git clone https://github.com/piinalpin/research-references-bot.git
```

## Chat His

* Telegram Bot Chat : https://t.me/research_references_bot
* LINE Bot Chat : http://line.me/ti/p/@437nryhw

## Authors

* **Alvinditya Saputra** - [LinkedIn](https://linkedin.com/in/piinalpin) [Instagram](https://www.instagram.com/piinalpin) [Twitter](https://www.twitter.com/piinalpin)
