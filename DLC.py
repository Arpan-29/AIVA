import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import json
import random
import pickle

fail = False

# DATA PREPROCESSING

with open("intents.json") as file:
    data = json.load(file)

try:
    if fail:
        skip

    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:

            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    punctuations = ["?", "!", ".", ",", "-"]

    words = [stemmer.stem(w.lower()) for w in words if w not in punctuations]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# DEEP NEURAL NETWORK 

net = tflearn.input_data(shape = [None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation = "softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

# TRAINING MODEL

try:
    if fail:
        skip

    model.load("model.tflearn")
except:
    model.fit(training, output, n_epoch = 500, batch_size = 16, show_metric = True)
    model.save("model.tflearn")

# MAIN FUNCTIONS

def bag_of_words(s, words):

    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(w.lower()) for w in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)

other_responses = ["I didn't understand. Please try again.", "Sorry, I couldn't catch it.", "I didn't quite get that."]

def get_response(query):

    results = model.predict([bag_of_words(query, words)])[0]
    results_index = np.argmax(results)

    if results[results_index] > 0.75:
        tag = labels[results_index]
            
        for intent in data["intents"]:
            if intent["tag"] == tag:
                response_tag = intent["tag"]
                responses = intent["responses"]
                break

        return random.choice(responses), response_tag

    else:
        return random.choice(other_responses), None