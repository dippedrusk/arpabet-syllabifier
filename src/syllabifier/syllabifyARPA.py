#!/usr/bin/env python3

# syllabifyARPA:
# Syllabify ARPABET transcriptions using General American English syllabification rules
# as found in https://en.wikipedia.org/wiki/English_phonology#Syllable_structure
# TODO:DOC caveat with morphological and word boundaries (e.g., mistreat, sesame street)

# Vasundhara Gautam
# October 3rd, 2017

import re
import sys

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

def syllabifyARPA(arpa_arr, silence_warnings=False):
    """
    Syllabifies ARPABET transcriptions according to General American English
    syllabification rules.

    Args:
        arpa_arr: A string or array of ARPABET phones with optional stress markers
        on the vowels.
        silence_warnings: Boolean (default False) to suppress ValueErrors

    Returns:
        List of strings with syllables in each row.
        In case the input is unsyllabifiable, an empty list is returned.

    Raises:
        ValueError if input contains non-ARPABET phonemes, no vowels or if it
        cannot be syllabified according to English syllabification rules.
    """

    def handleError(string):
        if not silence_warnings:
            raise ValueError(string)

    ret = []

    try:
        arpa_arr = arpa_arr.split() # Allows for phoneme array and string input
    except:
        pass

    for i in range(len(arpa_arr)):
        arpa_arr[i] = arpa_arr[i].upper()

    word = ' '.join(arpa_arr)

    if not (testInPhoneset(arpa_arr)):
        handleError('Input %s contains non-ARPABET phonemes' % word)
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
            handleError('Input error - no vowel in %s' % word)
            return ret
        final_arr[-1].append(temp_arr[i])

    # All onsets are maximized, some are illegal - fixing that
    for i in range(len(final_arr)):
        while testLegalOnset(final_arr[i]):
            if i == 0:
                handleError('Bad onset cluster in %s' % word)
                return ret
            c = testLegalOnset(final_arr[i])
            final_arr[i].remove(c)
            final_arr[i-1].append(c)

    for i in range(len(final_arr)):
        if not testLegalCoda(final_arr[i]):
            handleError('Impossible to syllabify %s according to English '
                          'syllabification rules.' % word)
            return ret

    ret = [' '.join(syllable) for syllable in final_arr]

    return ret

def testInPhoneset(arr):
    """
    Tests if input consists of 2-letter ARPABET phonemes. Does not require stress
    markers on the vowels.

    Args:
        arr: An array of strings

    Returns:
        True if input array consists of 2-letter ARPABET phones with optional
        stress markers.
    """
    for i in range(len(arr)):
        if not (arr[i] in PHONESET or re.match(VOWELS_REGEX, arr[i])):
            return False
    return True

def testLegalOnset(syllable):
    """
    Function to test for legal onset clusters.

    Args:
        syllable: An array of phones in a transcription containing a vowel

    Returns:
        None if the input's onset is legal. Otherwise, returns the first
        phone of the onset for removal and subsequent appendage to the previous
        syllable's coda.
    """

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
    """
    Function to test for legal coda clusters.

    Args:
        syllable: An array of phones in a transcription containing a vowel

    Returns:
        True if the coda cluster (phones after the vowel in the syllable) is
        legal according to English syllabification rules.
    """

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

    # English disallows 5+ length coda clusters
    elif length > 4:
        return False

    elif length == 4:
        # 4-phoneme codas must have /s/, /z/, /t/ or /d/ at the end
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

    # if instead of elif to check s-, z-, t-, d-appended clusters

    if length == 3:
        if ((cluster[2] == 'S' and cluster[1] in S_EXTENDED_CODAS)
            or
        (cluster[2] == 'Z' and cluster[1] in Z_EXTENDED_CODAS)
            or
        (cluster[2] == 'T' and cluster[1] in T_EXTENDED_CODAS)
            or
        (cluster[2] == 'D' and cluster[1] in D_EXTENDED_CODAS)):
            length -= 1

        # 3-phone clusters beginning with L, e.g., Alps, milked
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

        # 3-phone clusters beginning with R, e.g., carts, worst
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

        # 3-phone clusters beginning with M, e.g., mumps
        elif cluster[0] == 'M' and (
        (cluster[1] == 'P' and cluster[2] == 'T')
            or
        (cluster[1] == 'P' and cluster[2] == 'S')):
            return True

        # 3-phone clusters beginning with N, e.g., thousandth
        elif cluster[0] == 'N' and (
        (cluster[1] == 'D' and cluster[2] == 'TH')):
            return True

        # 3-phone clusters beginning with NG, e.g., angst
        elif cluster[0] == 'NG' and (
        (cluster[1] == 'K' and cluster[2] == 'T')
            or
        (cluster[1] == 'K' and cluster[2] == 'S')
            or
        (cluster[1] == 'K' and cluster[2] == 'TH')
            or
        (cluster[1] == 'S' and cluster[2] == 'T')):
            return True

        # 3-phone clusters beginning with K, e.g., sixth
        elif (
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'TH')
            or
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'T')):
            return True

    if length == 2:
        if ((cluster[1] == 'S' and cluster[0] in S_EXTENDED_CODAS)
            or
        (cluster[1] == 'Z' and cluster[0] in Z_EXTENDED_CODAS)
            or
        (cluster[1] == 'T' and cluster[0] in T_EXTENDED_CODAS)
            or
        (cluster[1] == 'D' and cluster[0] in D_EXTENDED_CODAS)):
            length -= 1

        # 2-phone clusters beginning with L, e.g., elk, health
        if cluster[0] == 'L' and (
        cluster[1] in STOPS.difference(['G'])
            or
        cluster[1] in AFFRICATES
            or
        cluster[1] in set(['F', 'S', 'SH', 'TH', 'V'])
            or
        cluster[1] in NASALS.difference(['NG'])):
            return True

        # 2-phone clusters beginning with R, e.g., arc, yarn
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

        # 2-phone clusters beginning with nasals, e.g., bent, ink
        elif cluster[0] == 'M' and cluster[1] in set(['P', 'F', 'TH', 'B']):
            return True
        elif cluster[0] == 'N' and cluster[1] in set(['T', 'D', 'CH', 'JH', 'TH', 'S', 'Z', 'F']):
            return True
        elif cluster[0] == 'NG' and cluster[1] in set(['K', 'TH', 'G']):
            return True

        # 2-phone clusters beginning with stops, e.g., pact, width
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
