import numpy as np
from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import casual_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from tqdm import tqdm

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def custom_tokenizer(text):
    tokens = [w.lower() for w in casual_tokenize(text)
              if w.isalpha() and w.lower() not in stop_words]
    return tokens

def compute_pmi_cooc_sparse(X, vocab, identity_terms, total_docs, top_n=20):
    """Given a sparse term-doc matrix (X) and vocab dict, calculate PMI for (identity, cooc_term)."""
    id_indices = [vocab[t] for t in identity_terms if t in vocab]
    term_counts = np.asarray((X[:, id_indices] > 0).sum(axis=0)).ravel()

    idx_to_word = {idx: word for word, idx in vocab.items()}
    cooc_terms_set = set()
    for i, iterm in enumerate(identity_terms):
        if iterm not in vocab: continue
        idx = vocab[iterm]
        rows = X[:, idx].nonzero()[0]
        others_counter = Counter()
        for row in rows:
            present = X[row].nonzero()[1]
            for j in present:
                w = idx_to_word[j]
                if w != iterm and w not in identity_terms and w not in stop_words:
                    others_counter[w] += 1
        for w, cnt in others_counter.most_common(top_n):
            cooc_terms_set.add(w)

    # Fix: convert to deterministic ordered list for indexing!
    cooc_terms = sorted(list(cooc_terms_set))
    cooc_indices = [vocab[w] for w in cooc_terms if w in vocab]
    word_counts = np.asarray((X[:, cooc_indices] > 0).sum(axis=0)).ravel()
    results = {}
    for i, iterm in enumerate(identity_terms):
        if iterm not in vocab: continue
        idx = vocab[iterm]
        results[iterm] = {}
        for j, other in enumerate(cooc_terms):
            if other not in vocab: continue
            oidx = vocab[other]
            cooc_mask = (X[:, idx] > 0).toarray().ravel() & (X[:, oidx] > 0).toarray().ravel()
            cooc = np.count_nonzero(cooc_mask)
            p_ab = cooc / total_docs
            p_a = term_counts[i] / total_docs
            p_b = word_counts[j] / total_docs if j < len(word_counts) else 1e-10
            if p_ab > 0 and p_a > 0 and p_b > 0:
                pmi = np.log2(p_ab / (p_a * p_b))
            else:
                pmi = float('-inf')
            results[iterm][other] = (pmi, cooc)
    return results, cooc_terms

def main(top_n=20, split="validation", sample_size=5000):
    identity_terms = ["boy", "girl", "man", "woman", "king", "queen"]
    ds = load_dataset("roneneldan/TinyStories", split=split)
    if sample_size is not None:
        ds = ds.select(range(min(sample_size, len(ds))))

    texts = [x["text"] for x in ds]
    vectorizer = CountVectorizer(tokenizer=custom_tokenizer,
                                 lowercase=True,
                                 stop_words=None,  # already filtered in tokenizer
                                 min_df=10)  # only words in at least 10 docs
    X = vectorizer.fit_transform(texts)
    vocab = vectorizer.vocabulary_
    total_docs = X.shape[0]

    pmi_results, cooc_terms = compute_pmi_cooc_sparse(X, vocab, identity_terms, total_docs, top_n=top_n)

    print("Total samples:", total_docs)
    print("Identity terms:", identity_terms)
    print()

    for iterm in identity_terms:
        print(f"\nIdentity term: '{iterm}'")
        print("-" * 40)
        for other in cooc_terms:
            if other in pmi_results[iterm]:
                pmi, count = pmi_results[iterm][other]
                print(f"Other: '{other}' | PMI={pmi:.4f} (cooc={count})")

if __name__ == "__main__":
    main(top_n=20, split="validation", sample_size=5000)