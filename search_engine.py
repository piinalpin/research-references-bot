# Load libraries
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from sklearn.feature_extraction.text import TfidfVectorizer
from stop_words import get_stop_words
from database import Query, Details
import pandas as pd
import numpy as np
import string, re
import random

stemmer = StemmerFactory().create_stemmer()
stopwords_id = get_stop_words("id")


def preprocess(text):
    text = text.lower().split(" ")
    text_clean = " ".join([i for i in text if i not in stopwords_id])
    text_stem = stemmer.stem(text_clean)
    result = ''.join([i for i in text_stem if not i.isdigit()])
    result = re.sub(r'[^\x00-\x7f]', r'', result)
    result = re.sub(r'[^\w\s]', '', result)
    return result


class Engine(object):

    def __init__(self, query):
        self.dataset = pd.read_excel("docs/dataset_preprocessing.xlsx")
        self.query = preprocess(query)
        self.phrase = [self.query] + self.dataset["preprocessed_title"].tolist()
        self.vectorizer = TfidfVectorizer()

    def get_scores(self):
        query = Query.get_by_query(self.query)
        if query is not None:
            details = query["details"]
            result = pd.DataFrame(details)
            dictionary = {
                "author": result["author"],
                "title": result["title"],
                "url": result["url"],
                "year": result["year"],
                "score": result["score"]
            }
            return dictionary
        else:
            transform = self.vectorizer.fit_transform(self.phrase)
            scores = (transform[0, :] * transform[1:, :].T).A[0]
            self.dataset["score"] = scores
            result = self.dataset.sort_values(by="score", ascending=False).head(10)
            dictionary = {
                "author": result["author"],
                "title": result["title"],
                "url": result["url"],
                "year": result["year"],
                "score": result["score"]
            }
            query = Query(query=self.query)
            query.save()
            for i in range(len(dictionary["author"])):
                author = list(dictionary["author"])[i].lstrip()
                title = list(dictionary["title"])[i].lstrip()
                url = list(dictionary["url"])[i].lstrip()
                year = list(dictionary["year"])[i]
                score = float(list(dictionary["score"])[i])
                details = Details(author=author, title=title, url=url, year=year, score=score, query_id=query.id)
                details.save()
            return dictionary



