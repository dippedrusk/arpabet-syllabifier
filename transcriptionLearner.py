import nltk
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import naive_bayes
from nltk.util import ngrams

from syllabifyARPA import syllabifyARPA

def main():
    df = pd.read_csv('cmudict.txt', delimiter='\n', header=None, quoting=3, comment='#', names=['dict'])
    #df = pd.read_csv('cmusubset.txt', delimiter='\n', header=None, names=['dict']) # For testing

    # Removing all rows containing non-alphanumeric characters and spaces
    df = df[df['dict'].str.contains(r'[^A-Z0-2 ]') == False]
    df = df['dict'].str.extract(r'(?P<word>\w+) (?P<transcription>.+)', expand=True)
    split = df['transcription'].str.split()

    # TODO: Document this!!!

    df = pd.concat([df, split.apply(syllabifyARPA)], axis=1)
    #df = df.melt(id_vars=['word', 'transcription'], value_name='syllable', var_name='position')
    df.dropna(inplace=True, thresh=3)

    df.reset_index(inplace=True)

    X_train, X_test, y_train, y_test = train_test_split(df['word'], df['transcription'])
    vect = TfidfVectorizer(ngram_range=(1,4), analyzer='char_wb').fit(X_train)
    X_train_vectorized = vect.transform(X_train)

    model = naive_bayes.MultinomialNB(alpha=0.1)
    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(vect.transform(X_test))

    print('This is the final score:')
    print(trigramJaccardDist(predictions, y_test.tolist()))

def trigramJaccardDist(predictions, targets):

    length = len(targets)
    assert length == len(predictions), 'Predictions and targets not of the same length.'

    def getARPAtrigrams(transcription):
        trigrams = set()
        phonemes = transcription.split()
        for i in range(len(phonemes)):
            if i > 1:
                trigrams.add((phonemes[i-2], phonemes[i-1], phonemes[i]))
        return trigrams

    def JaccardDist(set1, set2):
        return (len(set1.union(set2)) - len(set1.intersection(set2))) / len(set1.union(set2))

    scores = []
    for i in range(length):
        trigrams = getARPAtrigrams(predictions[i])
        correcttrigrams = getARPAtrigrams(targets[i])
        scores.append(JaccardDist(set(trigrams), set(correcttrigrams)))

    total = 0
    for score in scores:
        total += score

    return total / len(scores)

if __name__ == '__main__':
    main()
