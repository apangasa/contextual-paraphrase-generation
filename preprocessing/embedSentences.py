from __future__ import annotations
from sklearn import preprocessing
import json
import numpy as np
from tqdm import tqdm
import pickle


def fit_ohe(wa_dict: dict[str, str]):
    enc = preprocessing.OneHotEncoder(handle_unknown='ignore')
    X = set()
    for key, val in tqdm(wa_dict.items()):
        X = X.union(set(w.lower()
                        for w in key.split(' ')).union(set(w.lower() for w in val.split(' '))))
    X = np.array([list(X)]).transpose()
    print(X)
    enc.fit(X)
    return enc


def embed_word(word, enc: preprocessing.OneHotEncoder):
    return enc.transform([[word]])


def main():
    with open('./data/wa/wa_dict.json', 'r') as map_file:
        wa_dict = json.load(map_file)

    enc = fit_ohe(wa_dict)

    with open('./preprocessing/ohe.pkl', 'wb') as ohe_file:
        pickle.dump(enc, ohe_file)

    embed = embed_word('monkey', enc)
    print(embed)


if __name__ == '__main__':
    main()
