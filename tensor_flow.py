from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import json, nltk, pickle, random, tflearn
import numpy as np
import tensorflow as tf

stemmer = StemmerFactory().create_stemmer()
nltk.download('punkt')


class TensorFlow(object):

    def __init__(self, intents):
        self.classes = list()
        self.documents = list()
        self.ERROR_THRESHOLD = 0.25
        self.ignore_words = ["?"]
        self.intents = json.load(open(intents))
        self.output = list
        self.training = list()
        self.train_x = None
        self.train_y = None
        self.words = list()
        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                w = nltk.word_tokenize(pattern)
                self.words.extend(w)
                self.documents.append((w, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])
        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in self.ignore_words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))
        self.train_doc()
        self.model = self.set_model()

    def train_doc(self):
        training = list()
        output_empty = [0] * len(self.classes)
        for doc in self.documents:
            bag = list()
            pattern_words = doc[0]
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])
        self.training = training
        random.shuffle(self.training)
        self.training = np.array(self.training)
        self.train_x = list(self.training[:, 0])
        self.train_y = list(self.training[:, 1])

    def set_model(self):
        net = tflearn.input_data(shape=[None, len(self.train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.train_y[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir="tflearn_logs")
        model.fit(self.train_x, self.train_y, n_epoch=1000, batch_size=8, show_metric=True)
        model.save('model.tflearn')
        pickle.dump({'words': self.words, 'classes': self.classes, 'train_x': self.train_x, 'train_y': self.train_y},
                    open("training_data", "wb"))
        return model

    @staticmethod
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    @staticmethod
    def bow(sentence, words, show_details=False):
        sentence_words = TensorFlow.clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return np.array(bag)

    def classify(self, sentence):
        data = pickle.load(open("training_data", "rb"))
        classes = data['classes']
        words = data['words']
        self.model.load("model.tflearn")
        results = self.model.predict([TensorFlow.bow(sentence, words)])[0]
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = list()
        for r in results:
            return_list.append((classes[r[0]], r[1]))
        return return_list

    def response(self, sentence):
        results = self.classify(sentence)
        if results:
            while results:
                for i in self.intents['intents']:
                    if i['tag'] == results[0][0]:
                        return random.choice(i['responses'])
                results.pop(0)
