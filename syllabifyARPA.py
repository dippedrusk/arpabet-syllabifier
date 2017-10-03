#!/usr/bin/env python3

# syllabifyARPA:
# Syllabify ARPABET transcriptions using General American English syllabification rules

# Vasundhara Gautam
# October 3rd, 2017

import pandas as pd
import re
import logging

# Sets required to check for valid onset and coda clusters
VOICELESS = set(['K', 'P', 'T', 'F', 'HH', 'S', 'SH', 'TH', 'CH'])
VOICED = set(['G', 'B', 'D', 'DH', 'V', 'Z', 'ZH', 'JH'])

STOPS = set(['K', 'P', 'T', 'G', 'B', 'D'])
FRICATIVES = set(['F', 'DH', 'HH', 'S', 'SH', 'TH', 'V', 'Z', 'ZH'])
AFFRICATES = set(['CH', 'JH'])
NASALS = set(['M', 'N', 'NG'])
APPROXIMANTS = set(['L', 'R', 'W', 'Y'])
CONSONANTS = STOPS.union(FRICATIVES).union(AFFRICATES).union(NASALS).union(APPROXIMANTS)

S_EXTENDED_CODAS = set(['K', 'P', 'T', 'F', 'TH', 'D', 'NG'])
Z_EXTENDED_CODAS = set(['G', 'B', 'D', 'DH', 'V', 'M', 'N', 'NG', 'L'])

T_EXTENDED_CODAS = set(['K', 'P', 'F', 'S', 'SH', 'TH', 'CH', 'N'])
D_EXTENDED_CODAS = set(['G', 'B', 'DH', 'V', 'Z', 'ZH', 'JH', 'M', 'N', 'NG'])

PHONESET = set(['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B',
                'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G',
                'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N',
                'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T',
                'TH', 'UH', 'UW', 'V', 'W', 'Y', 'Z', 'ZH'])

# Optional stress markers (0,1,2) after the vowel for flexibility
VOWELS_REGEX = re.compile(r'(?:AA|AE|AH|AO|AW|AY|EH|ER|EY|IH|IY|OW|OY|UW|UH)[012]?')

def syllabifyARPA(arpa_arr, return_list=False, silence_warnings=False):
    """
    Syllabifies ARPABET transcriptions according to General American English
    syllabification rules.

    Args:
        arpa_arr: A string or array of ARPABET phones.
        return_list: Boolean (default False) to return list of syllable strings
        silence_warnings: Boolean (default False) to suppress printing to stderr

    Returns:
        Pandas Series of dtype 'Object' with syllables in each row.
        If return_list set to True, returns a Python list of strings containing
        the syllables.
        In case the input is unsyllabifiable, an empty Series or list is
        returned.

    Raises:
        Critical error: Input contains non-ARPABET phonemes.
        Warning: Clusters with no vowels or bad onsets.
        Error: Impossible to syllabify according to English rules.
    """


    logging.basicConfig()

    if silence_warnings:
        logging.raiseExceptions=False

    ret = pd.Series(None)
    if return_list:
        ret = []

    try:
        arpa_arr = arpa_arr.split() # Allows for phoneme array and string input
    except:
        pass

    for i in range(len(arpa_arr)):
        arpa_arr[i] = arpa_arr[i].upper()

    word = ' '.join(arpa_arr)

    if not (testInPhoneset(arpa_arr)):
        logging.critical('Input %s contains non-ARPABET phonemes' % word)
        return ret

    final_arr = []
    temp_arr = []

    # Append till and including vowels
    for i in range(len(arpa_arr)):
        temp_arr.append(arpa_arr[i])
        if re.match(VOWELS_REGEX, arpa_arr[i]):
            final_arr.append(temp_arr)
            temp_arr = []

    # Handle potential remaining coda consonants
    for i in range(len(temp_arr)):
        if len(final_arr) < 1:
            logging.warning('Input error - no vowel in %s' % word)
            return ret
        final_arr[-1].append(temp_arr[i])

    # All onsets are maximized, some are illegal - fixing that
    for i in range(len(final_arr)):
        while testLegalOnset(final_arr[i]):
            if i == 0:
                logging.warning('Bad onset cluster in %s' % word)
                return ret
            c = testLegalOnset(final_arr[i])
            final_arr[i].remove(c)
            final_arr[i-1].append(c)

    for i in range(len(final_arr)):
        if not testLegalCoda(final_arr[i]):
            logging.error('Impossible to syllabify %s according to English '
                          'syllabification rules.' % word)
            return ret

    ret = pd.Series([' '.join(syllable) for syllable in final_arr])
    if return_list:
        ret = list(ret)

    return ret

def testInPhoneset(arr):
    for i in range(len(arr)):
        if not (arr[i] in PHONESET or re.match(VOWELS_REGEX, arr[i])):
            return False
    return True

def testLegalOnset(syllable):
    cluster = []

    for i in range(len(syllable)):
        if re.match(VOWELS_REGEX, syllable[i]):
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
        (cluster[1] in VOICELESS.intersection(STOPS) and cluster[2] in APPROXIMANTS)
            or
        (cluster[1] in VOICELESS.intersection(FRICATIVES) and cluster[2] == 'R')):
            return cluster[0]

    elif length == 2:
        if not (
        # Valid length-2 consonant clusters are consonant-Y, stop-approximant
        # and voiceless_fricative_or_V-approximant
        (cluster[0] in CONSONANTS and cluster[1] == 'Y')
            or
        (cluster[0] in STOPS and cluster[1] in APPROXIMANTS)
            or
        (cluster[0] in VOICELESS.intersection(FRICATIVES).union(['V']) and
        cluster[1] in APPROXIMANTS)
            or
        # Only s-voiceless_stop, s-voiceless_fricative and s-non_NG_nasals
        # are valid length-2 s-clusters
        (cluster[0] == 'S' and cluster[1] in VOICELESS.difference(AFFRICATES))
            or
        (cluster[0] == 'S' and cluster[1] in NASALS.difference(['NG']))
            or
        # Other clusters normalized through loanwords, e.g. SH-N, S-V, NW, MR
        (cluster[0] == 'SH' and cluster[1] in NASALS and cluster != 'NG')
            or
        (cluster[0] == 'S' and cluster[1] == 'V')
            or
        (cluster[0] == 'M' and cluster[1] in APPROXIMANTS)
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
        if re.match(VOWELS_REGEX, syllable[i]):
            postvowel = True

    length = len(cluster)

    if length == 0:
        return True

    elif length > 4:
        return False

    elif length == 4:
        # 4-phoneme codas have to have /s/ or /z/ as an appendix
        if ((cluster[3] == 'S' and cluster[2] in S_EXTENDED_CODAS)
            or
        (cluster[3] == 'Z' and cluster[2] in Z_EXTENDED_CODAS)
            or
        (cluster[3] == 'T' and cluster[2] in T_EXTENDED_CODAS)
            or
        (cluster[3] == 'D' and cluster[2] in D_EXTENDED_CODAS)):
            length -= 1
        else:
            return False

    if length == 3: # if instead of elif to check s-, z-, t-, d-appended clusters
        if ((cluster[2] == 'S' and cluster[1] in S_EXTENDED_CODAS)
            or
        (cluster[2] == 'Z' and cluster[1] in Z_EXTENDED_CODAS)
            or
        (cluster[2] == 'T' and cluster[1] in T_EXTENDED_CODAS)
            or
        (cluster[2] == 'D' and cluster[1] in D_EXTENDED_CODAS)):
            length -= 1

        elif cluster[0] == 'L' and (
        (cluster[1] == 'P' and cluster[2] == 'T')
            or
        (cluster[1] == 'P' and cluster[2] == 'S')
            or
        (cluster[1] == 'F' and cluster[2] == 'TH')
            or
        (cluster[1] == 'T' and cluster[2] == 'S')
            or
        (cluster[1] == 'K' and cluster[2] == 'T')
            or
        (cluster[1] == 'K' and cluster[2] == 'S')
            or
        (cluster[1] == 'S' and cluster[2] == 'T')):
            return True

        elif cluster[0] == 'R' and (
        (cluster[1] == 'P' and cluster[2] == 'T')
            or
        (cluster[1] == 'P' and cluster[2] == 'S')
            or
        (cluster[1] == 'M' and cluster[2] == 'TH')
            or
        (cluster[1] == 'T' and cluster[2] == 'S')
            or
        (cluster[1] == 'K' and cluster[2] == 'T')
            or
        (cluster[1] == 'S' and cluster[2] == 'T')):
            return True

        elif cluster[0] == 'M' and (
        (cluster[1] == 'P' and cluster[2] == 'T')
            or
        (cluster[1] == 'P' and cluster[2] == 'S')):
            return True

        elif cluster[0] == 'N' and (
        (cluster[1] == 'D' and cluster[2] == 'TH')):
            return True

        elif cluster[0] == 'NG' and (
        (cluster[1] == 'K' and cluster[2] == 'T')
            or
        (cluster[1] == 'K' and cluster[2] == 'S')
            or
        (cluster[1] == 'K' and cluster[2] == 'TH')
            or
        (cluster[1] == 'S' and cluster[2] == 'T')):
            return True

        elif (
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'TH')
            or
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'T')):
            return True

    if length == 2: # if instead of elif to check s-, z-, t-, d-appended clusters
        if ((cluster[1] == 'S' and cluster[0] in S_EXTENDED_CODAS)
            or
        (cluster[1] == 'Z' and cluster[0] in Z_EXTENDED_CODAS)
            or
        (cluster[1] == 'T' and cluster[0] in T_EXTENDED_CODAS)
            or
        (cluster[1] == 'D' and cluster[0] in D_EXTENDED_CODAS)):
            length -= 1

        if cluster[0] == 'L' and (
        cluster[1] in STOPS.difference(['G'])
            or
        cluster[1] in AFFRICATES
            or
        cluster[1] in set(['F', 'S', 'SH', 'TH', 'V'])
            or
        cluster[1] in NASALS.difference(['NG'])):
            return True

        elif cluster[0] == 'R' and (
        cluster[1] in STOPS
            or
        cluster[1] in AFFRICATES
            or
        cluster[1] in set(['F', 'S', 'SH', 'TH', 'V', 'Z'])
            or
        cluster[1] in NASALS.difference(['NG'])
            or
        cluster[1] == 'L'):
            return True

        elif cluster[0] == 'M' and cluster[1] in set(['P', 'F', 'TH', 'B']):
            return True

        elif cluster[0] == 'N' and cluster[1] in set(['T', 'D', 'CH', 'JH', 'TH', 'S', 'Z', 'F']):
            return True

        elif cluster[0] == 'NG' and cluster[1] in set(['K', 'TH', 'G']):
            return True

        elif (
        (cluster[0] == 'F' and cluster[1] in set(['T', 'TH']))
            or
        (cluster[0] == 'S' and cluster[1] in set(['P', 'T', 'K']))
            or
        (cluster[0] == 'P' and cluster[1] in set(['T', 'TH', 'S', 'F']))
            or
        (cluster[0] == 'K' and cluster[1] in set(['T', 'S', 'SH']))
            or
        (cluster[0] == 'T' and cluster[1] in set(['S', 'TH']))
            or
        (cluster[0] == 'D' and cluster[1] == 'TH')):
            return True

    if length == 1:
        # These phonemes cannot exist as codas by themselves
        if cluster[0] not in set(['HH', 'W', 'Y']):
            return True

    return False
