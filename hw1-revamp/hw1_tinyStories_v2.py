import numpy as np
import pandas as pd
from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import casual_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from tqdm import tqdm

from IPython import embed

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))
stop_words.remove("he")
stop_words.remove("she")

def custom_tokenizer(text):
    tokens = [w.lower() for w in casual_tokenize(text)
              if w.isalpha() and w.lower() not in stop_words]
    return tokens

def vectorizeDocs(texts,min_df=.001):
    vectorizer = CountVectorizer(tokenizer=custom_tokenizer,
                                 lowercase=True,
                                 stop_words=None,  # already filtered in tokenizer
                                 min_df=min_df)  # only words in at least 10 docs
    X = vectorizer.fit_transform(texts)
    vocab = vectorizer.vocabulary_
    total_docs = X.shape[0]
    df = pd.DataFrame(data=X.todense(),columns=list(vocab))
    return df

def computeCoocs(term, df, vocab_cnts):
    N = len(df)
    cnt_term = df[term].sum()
    # docs where both terms appear
    term_docs = df[df[term] != 0]
    cooc_cnts = term_docs[term_docs != 0].sum(axis=0)
    pmis = np.log2(N * cooc_cnts / (vocab_cnts[cooc_cnts.index] * cnt_term))
    
    # remove term itself
    pmis = pmis[pmis.index.drop(term)]
    
    # return only non inf PMIs?
    pmis = pmis[~np.isinf(pmis)]
    return pmis

def main(top_n=20, split="train", sample_size=5000):
    identity_terms = ["he","she", "boy", "girl", "man", "woman"]# , "king", "queen"]
    ds = load_dataset("roneneldan/TinyStories", split=split)
    
    if sample_size is not None:
        ds = ds.select(range(min(sample_size, len(ds))))

    texts = [x["text"] for x in ds]
    
    df = vectorizeDocs(texts)
    vocab_cnts = df.sum(axis=0)
    coocs = {}
    for term in identity_terms:
        pmis = computeCoocs(term, df,vocab_cnts)
        coocs[term] = pmis
        print(term)
        print(pmis.sort_values(ascending=False).head(top_n))
    embed();exit()

if __name__ == "__main__":
    main(top_n=10, split="train", sample_size=10000)