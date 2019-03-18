import flask
import re
import pandas as pd
import spacy
from flask import Response
from pandas import DataFrame
from spacy import displacy
import en_core_web_sm

nlp = spacy.load('en_core_web_md')

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template("index.html")


@app.route('/process', methods=["POST"])
def process():
    if flask.request.method == 'POST':
        rawtext = flask.request.form['rawtext']
        doc = nlp(rawtext)
        d = []
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
        global df
        df= pd.DataFrame(d, columns=('named entity', 'output'))
        df = df.groupby('named entity')['output'].unique().apply(list)
        return flask.render_template("index.html", datalen=range(0,len(df)), data=df)

@app.route('/down', methods=["POST"])
def download():
    Response(df.to_csv('Named-Entry-Extractor.csv'))
    return flask.render_template("save.html",data="You file is saved at your local disk..!!")

if __name__ == '__main__':
    app.run(debug=True)

