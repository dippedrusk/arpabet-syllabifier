import pandas as pd
import re
import logging

logging.basicConfig(filename = 'syllabifier.log',level = logging.WARNING)

# Sets required to check for valid onset and coda clusters
voiceless = set(['K', 'P', 'T', 'F', 'HH', 'S', 'SH', 'TH', 'CH'])
voiced = set(['G', 'B', 'D', 'DH', 'V', 'Z', 'ZH', 'JH'])
stops = set(['K', 'P', 'T', 'G', 'B', 'D'])
fricatives = set(['F', 'DH', 'HH', 'S', 'SH', 'TH', 'V', 'Z', 'ZH'])
affricates = set(['CH', 'JH'])
nasals = set(['M', 'N', 'NG'])
approximants = set(['L', 'R', 'W', 'Y'])
consonants = stops.union(fricatives).union(affricates).union(nasals).union(approximants)
# Optional stress markers (0,1,2) after the vowel for flexibility
vowelsregex = re.compile(r'(?:AA|AE|AH|AO|AW|AY|EH|ER|EY|IH|IY|OW|OY|UW|UH)[012]?')

def syllabifyARPA(arpa_arr):

    word = ' '.join(arpa_arr)

    final_arr = []
    temp_arr = []
    valid = True

    # Append till and including vowels
    for i in range(len(arpa_arr)):
        temp_arr.append(arpa_arr[i])
        if re.match(vowelsregex, arpa_arr[i]):
            final_arr.append(temp_arr)
            temp_arr = []

    # Handle potential remaining coda consonants
    for i in range(len(temp_arr)):
        if len(final_arr) < 1:
            logging.warning('Input error - no vowel in %s' % word)
            return pd.Series(None)
        final_arr[-1].append(temp_arr[i])

    # All onsets are maximized, some are illegal - fixing that
    for i in range(len(final_arr)):
        while testLegalOnset(final_arr[i]):
            if i == 0:
                logging.warning('Bad onset cluster in %s' % word)
                valid = False
            c = testLegalOnset(final_arr[i])
            final_arr[i].remove(c)
            final_arr[i-1].append(c)

    for i in range(len(final_arr)):
        if not testLegalCoda(final_arr[i]):
            logging.error('Impossible to syllabify %s according to English '
                          'syllabification rules.' % word)
            valid = False

    if not valid:
        return pd.Series(None)
    return pd.Series([' '.join(syllable) for syllable in final_arr])

def testLegalOnset(syllable):
    cluster = []

    for i in range(len(syllable)):
        if re.match(vowelsregex, syllable[i]):
            break
        else:
            cluster.append(syllable[i])

    length = len(cluster)

    if length > 3:
        return cluster[0]

    elif length == 3:
        # Only s-clusters can be length 3
        if not (cluster[0] == 'S'):
            return cluster[0]
        # Clusters beginning with s can only be of the forms
        # s-voiceless_stop-approximant or s-voiceless_fricative-r
        elif not (
        (cluster[1] in voiceless.intersection(stops) and cluster[2] in approximants)
            or
        (cluster[1] in voiceless.intersection(fricatives) and cluster[2] == 'R')):
            return cluster[0]

    elif length == 2:
        if not (
        # Valid length-2 consonant clusters are consonant-Y, stop-approximant
        # and voiceless_fricative_or_V-approximant
        (cluster[0] in consonants and cluster[1] == 'Y')
            or
        (cluster[0] in stops and cluster[1] in approximants)
            or
        (cluster[0] in voiceless.intersection(fricatives).union(['V']) and
        cluster[1] in approximants)
            or
        # Only s-voiceless_stop, s-voiceless_fricative and s-non_NG_nasals
        # are valid length-2 s-clusters
        (cluster[0] == 'S' and cluster[1] in voiceless.difference(affricates))
            or
        (cluster[0] == 'S' and cluster[1] in nasals.difference(['NG']))
            or
        # Other clusters normalized through loanwords, e.g. SH-N, S-V, NW, MR
        (cluster[0] == 'SH' and cluster[1] in nasals and cluster != 'NG')
            or
        (cluster[0] == 'S' and cluster[1] == 'V')
            or
        (cluster[0] == 'M' and cluster[1] in approximants)
            or
        (cluster[0] == 'N' and cluster[1] == 'W')):
            return cluster[0]

    elif length == 1 and cluster[0] == 'NG':
        # Single-consonant-onsets are valid except for NG
        return cluster[0]

    return None

def testLegalCoda(syllable):
    cluster = []

    postvowel = False
    for i in range(len(syllable)):
        if postvowel:
            cluster.append(syllable[i])
        if re.match(vowelsregex, syllable[i]):
            postvowel = True

    # TODO: Code this

    return True
