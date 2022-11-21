import json
import os
import pickle
import re
import statistics
import statistics as st
import string
from glob import glob
from statistics import mode

import dotenv
import nltk
import numpy as np
import sklearn
import tweepy
import unidecode
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from emot.emo_unicode import EMOTICONS_EMO
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

nltk.download("wordnet")
nltk.download("omw-1.4")


# Defining dictionary containing all emojis with their meanings.
emoticons_manual = {
    ":)": "smile",
    ":-)": "smile",
    ";d": "wink",
    ":-E": "vampire",
    ":(": "sad",
    ":-(": "sad",
    ":-<": "sad",
    ":P": "raspberry",
    ":O": "surprised",
    ":-@": "shocked",
    ":@": "shocked",
    ":-$": "confused",
    ":\\": "annoyed",
    ":#": "mute",
    ":X": "mute",
    ":^)": "smile",
    ":-&": "confused",
    "$_$": "greedy",
    "@@": "eyeroll",
    ":-!": "confused",
    ":-D": "smile",
    ":-0": "yell",
    "O.o": "confused",
    "<(-_-)>": "robot",
    "d[-_-]b": "dj",
    ":'-)": "sadsmile",
    ";)": "wink",
    ";-)": "wink",
    "O:-)": "angel",
    "O*-)": "angel",
    "(:-D": "gossip",
    "=^.^=": "cat",
}

# Defining set containing all stopwords in english.
stopwordlist = [
    "a",
    "rt",
    "about",
    "above",
    "after",
    "again",
    "ain",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "by",
    "can",
    "d",
    "did",
    "do",
    "does",
    "doing",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "has",
    "have",
    "having",
    "he",
    "her",
    "here",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "i",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "itself",
    "just",
    "ll",
    "m",
    "ma",
    "me",
    "more",
    "most",
    "my",
    "myself",
    "now",
    "o",
    "of",
    "on",
    "once",
    "only",
    "or",
    "other",
    "our",
    "ours",
    "ourselves",
    "out",
    "own",
    "re",
    "s",
    "same",
    "she",
    "shes",
    "should",
    "shouldve",
    "so",
    "some",
    "such",
    "t",
    "than",
    "that",
    "thatll",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "ve",
    "very",
    "was",
    "we",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "whom",
    "why",
    "will",
    "with",
    "won",
    "y",
    "you",
    "youd",
    "youll",
    "youre",
    "youve",
    "your",
    "yours",
    "yourself",
    "yourselves",
]

# Defining regex patterns.
urlPattern = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
userPattern = r"@[^\s]+"
alphaPattern = r"[^a-zA-Z0-9]"
sequencePattern = r"(.)\1\1+"
seqReplacePattern = r"\1\1"

wordLemm = WordNetLemmatizer()

emoticons = EMOTICONS_EMO
emoticons.update(emoticons_manual)

load_dotenv()

consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_KEY_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


client = tweepy.Client(
    consumer_key=consumer_key,
    bearer_token=bearer_token,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)


def get_tweets_from_hashtag(hashtag):
    try:
        data = client.search_recent_tweets(query=hashtag)
        tweets = data[0]
        tweets = [tweet.text for tweet in tweets]
        return tweets
    except Exception as e:
        return {
            "type": "error",
            "data": "Something went Wrong, Please check the entered username",
        }


def twitterUserTweetRequest(username):
    try:
        user_res = client.get_user(
            username=username,
            tweet_fields=["id", "public_metrics"],
            user_fields=[
                "description",
                "name",
                "id",
                "profile_image_url",
                "username",
                "verified",
                "public_metrics",
            ],
        ).data
        tweet_res = client.get_users_tweets(
            id=user_res["id"], max_results=100, tweet_fields=["lang"]
        ).data
        tweet_res = list(filter(lambda x: x["lang"] == "en", tweet_res))
        tweet_res = list(
            map(lambda x: {"id": x["id"], "text": x["text"]}, tweet_res))
        profile = {
            "id": user_res["id"],
            "name": user_res["name"],
            "username": user_res["username"],
            "verified": user_res["verified"],
            "profile_image_url": "".join(
                user_res["profile_image_url"].split("_normal")
            ),
            "public_metrics": user_res["public_metrics"],
            "url": f"https://twitter.com/{user_res['username']}",
        }
        return {"type": "success", "data": {
            "profile": profile, "tweets": tweet_res}}
    except print(0):
        return {
            "type": "error",
            "data": "Something went Wrong, Please check the entered username",
        }


def load_models():
    bow = sorted(glob("../models/bow/*"))
    tfidf = sorted(glob("../models/tfidf/*"))
    bow_models = []
    tfidf_models = []
    for model_path in bow:
        model = pickle.load(open(model_path, "rb"))
        bow_models.append(model)
    for model_path in tfidf:
        model = pickle.load(open(model_path, "rb"))
        tfidf_models.append(model)
    return bow_models, tfidf_models


def preprocess(textdata):
    textdata = list(textdata)
    processedText = []

    for tweet in textdata:
        tweet = tweet.lower()

        # Remove all URls
        tweet = re.sub(urlPattern, "", tweet)
        # Replace all emojis.
        for emot in EMOTICONS_EMO:
            tweet = re.sub(
                "(" + re.escape(emot) + ")",
                " " +
                "_".join(EMOTICONS_EMO[emot].replace(",", "").split()) + " ",
                tweet,
            )
        # Remove @USERNAME.
        tweet = re.sub(userPattern, "", tweet)
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, " ", tweet)
        # Replace 3 or more consecutive letters by 2 letter.
        tweet = re.sub(sequencePattern, seqReplacePattern, tweet)
        # Remove all punctuations left
        tweet = tweet.translate(str.maketrans("", "", string.punctuation))

        """remove html tags from text"""
        soup = BeautifulSoup(tweet, "html.parser")
        tweet = soup.get_text(separator=" ")

        """Remove accented characters from text"""
        tweet = unidecode.unidecode(tweet)

        tweetwords = ""
        for word in tweet.split():
            # Checking if the word is a stopword.
            if word not in stopwordlist:
                if len(word) > 1:
                    # Lemmatizing the word.
                    word = wordLemm.lemmatize(word)
                    tweetwords += word + " "

        processedText.append(tweetwords)

    return processedText


def preprocess_pipeline(tweets):
    preprocessed_tweets = preprocess(tweets)
    return preprocessed_tweets


def get_predictions(tweets):

    bow_models, tfidf_models = load_models()

    predictions = []
    probalities = []
    bow = pickle.load(open("../models/vectorizers/bow.pickle", "rb"))
    tfidf = pickle.load(open("../models/vectorizers/tfidf.pickle", "rb"))
    bow_vector = bow.transform(tweets)
    tfidf_vector = tfidf.transform(tweets)
    for model in bow_models:
        probalities.extend(model.predict_proba(bow_vector).tolist())
        predictions.append(model.predict(bow_vector).tolist())
    for model in tfidf_models:
        probalities.extend(model.predict_proba(tfidf_vector).tolist())
        predictions.append(model.predict(tfidf_vector).tolist())

    return probalities, predictions


def get_percentage_positive(predictions):
    percentage_positive = []
    for preds in predictions:
        percentage_positive.append(np.sum(preds) / len(preds))

    return percentage_positive

def get_frequency_dict(tweets):
    freq = {}
    tweets = ' '.join(tweets).split()
    for word in tweets:
        freq[word] = freq.get(word, 0) + 1
    return freq


app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["GET"])
def new():
    return "hello world!"


@app.route("/predict", methods=["GET"])
@cross_origin()
def predict():
    args = request.args.to_dict()
    query = args.get("query")
    bow = sorted(glob("../models/bow/*"))
    tfidf = sorted(glob("../models/tfidf/*"))
    models = bow + tfidf
    print(query)

    idx = models.index('../models/tfidf/Logistic_Regression_tfidf.pkl')

    if query.startswith("@"):
        username = query
        tweets = twitterUserTweetRequest(username[1:])
        tweets = tweets.get("data").get("tweets")
        tweets = [tweet.get("text") for tweet in tweets]
        tweets = preprocess_pipeline(tweets)
        freq = get_frequency_dict(tweets)
        probalities, predictions = get_predictions(tweets)
        percentage_positive = get_percentage_positive(predictions)
        probalities = [
            [x.split("/")[-1].split(".")[0], float(np.round(y, 4)) * 100]
            for x, y in zip(models, percentage_positive)
        ]

        avg = np.mean(percentage_positive)
        lr_pp = float(np.round(percentage_positive[idx], 4) )* 100
        data = [100-lr_pp, lr_pp]
        prediction = "Positive"
        if avg < 0.5:
            prediction = "Negative"
            data = [lr_pp, 100-lr_pp]
        return {"tweet": query, "prediction": prediction,
                "probabilties": probalities, "data": {
                    "datasets": [{
                        "data": data
                    }],
                    "labels": [
                        'Negative',
                        'Positive'
                    ]
                }, "freq": freq}

    elif query.startswith("#"):
        tweets = get_tweets_from_hashtag(query)
        print(tweets)
        tweets = preprocess_pipeline(tweets)
        freq = get_frequency_dict(tweets)
        probalities, predictions = get_predictions(tweets)
        percentage_positive = get_percentage_positive(predictions)
        pred = mode(np.array(predictions).flatten().tolist())
        probalities = [
            [x.split("/")[-1].split(".")[0], float(np.round(y, 4)) * 100]
            for x, y in zip(models, percentage_positive)
        ]
        avg = np.mean(percentage_positive)
        lr_pp = float(np.round(percentage_positive[idx], 4) )* 100
        data = [100-lr_pp, lr_pp]
        if pred == 0:
            probalities = [[x[0], 100 - x[1]] for x in probalities]
            data = [lr_pp, 100-lr_pp]
        probalities = sorted(probalities, key=lambda x: x[1], reverse=True)
        avg = np.mean(percentage_positive)
        prediction = ["Negative", "Positive"][pred]
        return {"tweet": query, "prediction": prediction,
                "probabilties": probalities, "data": {
                    "datasets": [{
                        "data": data
                    }],
                    "labels": [
                        'Negative',
                        'Positive'
                    ]
                }, "freq": freq}

    else:
        tweets = preprocess_pipeline([query])
        probalities, predictions = get_predictions(tweets)
        predictions = np.array(predictions).flatten().tolist()
        prediction = mode(predictions)
        probalities = [
            [x.split("/")[-1].split(".")[0],
             float(np.round(y[prediction], 4)) * 100]
            for x, y in zip(models, probalities)
        ]
        prediction = "Positive" if prediction else "Negative"
        probalities = sorted(probalities, key=lambda x: x[1], reverse=True)
        return {"tweet": query, "prediction": prediction,
                "probabilties": probalities}


if __name__ == "__main__":
    app.run(port=5002, debug=True)
