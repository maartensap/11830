import numpy as np
from datasets import load_dataset
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import casual_tokenize
from collections import Counter, defaultdict
from tqdm import tqdm

nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('english'))

def compute_pmi_cooc(
    cooc_counts,
    term_counts,
    word_counts,
    total_samples,
    class_names,
    identity_terms,
    cooc_terms
):
    """Compute PMI for each (identity, cooc_term, class) tuple."""
    total_instances = sum(total_samples.values())
    results = {idterm: {other: {} for other in cooc_terms} for idterm in identity_terms}
    for idterm in identity_terms:
        for other_term in cooc_terms:
            for cls in class_names:
                num_cooc = cooc_counts[cls][idterm][other_term]
                p_ab = num_cooc / total_instances
                p_a = term_counts[cls][idterm] / total_instances
                p_b = word_counts[cls][other_term] / total_instances
                if p_ab > 0 and p_a > 0 and p_b > 0:
                    pmi = np.log2(p_ab / (p_a * p_b))
                else:
                    pmi = float('-inf')
                results[idterm][other_term][cls] = (pmi, num_cooc)
    return results

def main(top_n=20):
    identity_terms = ["man", "woman"]
    dataset = load_dataset("Anthropic/hh-rlhf", data_dir="harmless-base")
    train = dataset["train"]
    train = train[:1000]
    train = [dict(chosen=c,rejected=r) for c,r in zip(train["chosen"],train["rejected"])]
    class_names = ["chosen", "rejected"]

    # Only consider non-stopword, non-identity terms as "other terms"
    all_other_terms_counter = Counter()

    term_counts = {cls: {iterm: 0 for iterm in identity_terms} for cls in class_names}
    word_counts = {cls: Counter() for cls in class_names}
    cooc_counts = {cls: {iterm: Counter() for iterm in identity_terms} for cls in class_names}

    for row in tqdm(train,ascii=True):
        for cls in class_names:
            tokens = [w.lower() for w in casual_tokenize(row[cls])
                      if w.isalpha() and w.lower() not in stop_words]
            tokens_set = set(tokens)
            for iterm in identity_terms:
                if iterm in tokens_set:
                    term_counts[cls][iterm] += 1
                    for other in tokens_set:
                        if other not in identity_terms and other not in stop_words:
                            cooc_counts[cls][iterm][other] += 1
                            all_other_terms_counter[other] += 1
            for tok in tokens:
                if tok not in identity_terms and tok not in stop_words:
                    word_counts[cls][tok] += 1

    # Select the top N co-occurring terms for each identity term (union as cooc_terms)
    cooc_terms = set()
    for iterm in identity_terms:
        most_common_per_class = []
        for cls in class_names:
            most_common_per_class.extend(
                [w for w, _ in cooc_counts[cls][iterm].most_common(top_n)]
            )
        cooc_terms.update(most_common_per_class)
    cooc_terms = list(cooc_terms)

    total_samples = {cls: len(train) for cls in class_names}
    pmi_results = compute_pmi_cooc(
        cooc_counts, term_counts, word_counts,
        total_samples, class_names, identity_terms, cooc_terms
    )

    print("Total train samples:", len(train))
    print("Identity terms:", identity_terms)
    print()

    for iterm in identity_terms:
        print(f"\nIdentity term: '{iterm}'")
        print("-" * 40)
        for other in cooc_terms:
            info = f"Other: '{other}'"
            for cls in class_names:
                pmi, count = pmi_results[iterm][other][cls]
                info += f"  | PMI({cls})={pmi:.4f} (cooc={count})"
            print(info)

if __name__ == "__main__":
    main(top_n=20)
