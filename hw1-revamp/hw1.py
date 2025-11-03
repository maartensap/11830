from IPython import embed
import numpy as np
from datasets import load_dataset

import numpy as np
from datasets import load_dataset

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import casual_tokenize

from tqdm import tqdm
import pandas as pd

# Download NLTK stopwords if not present
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def compute_pmi(term_counts, term_total, total_samples, class_names):
    total_instances = sum(total_samples.values())
    results = {term: {} for term in term_total}
    for term in term_total:
        for cls in class_names:
            term_in_class = term_counts[cls][term]
            p_term_and_class = term_in_class / total_instances
            p_term = term_total[term] / total_instances
            p_class = total_samples[cls] / total_instances
            if p_term_and_class > 0 and p_term > 0 and p_class > 0:
                pmi = np.log2(p_term_and_class / (p_term * p_class))
            else:
                pmi = float('-inf')
            results[term][cls] = (pmi, term_in_class)
    return results

def main():
    identity_terms = ["man", "woman", "gay", "straight"]
    stop_terms = stop_words
    dataset = load_dataset("Anthropic/hh-rlhf", data_dir="helpful-base")
    # dataset = load_dataset("Anthropic/hh-rlhf", data_dir="harmless-base")
    train = dataset["train"]
    
    train = train[:100000]
    train = [dict(chosen=c,rejected=r) for c,r in zip(train["chosen"],train["rejected"])]
    
    class_names = ["chosen", "rejected"]

    total_samples = {cls: len(train) for cls in class_names}
    term_counts = {cls: {term: 0 for term in identity_terms} for cls in class_names}
    term_total = {term: 0 for term in identity_terms}

    for row in tqdm(train,ascii=True):

        for cls in class_names:
            # Tokenize and remove stopwords
            tokens = [w.lower() for w in casual_tokenize(row[cls]) if w.lower() not in stop_terms]
            for term in identity_terms:
                if term.lower() in tokens:
                    term_counts[cls][term] += 1
                    term_total[term] += 1

    total_instances = len(train) * 2

    pmi_results = compute_pmi(term_counts, term_total, total_samples, class_names)

    print("Total train samples:", len(train))
    print("Identity terms:", identity_terms)
    print()

    for term in identity_terms:
        print(f"Term: '{term}'")
        for cls in class_names:
            pmi, count = pmi_results[term][cls]
            print(f"  PMI({term!r}, {cls!r}): {pmi:.4f}   (count={count})")
        print()

if __name__ == "__main__":
    main()
