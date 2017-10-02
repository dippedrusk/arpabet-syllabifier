import pandas as pd
import re
import logging

logging.basicConfig(filename = 'syllabifier.log',level = logging.WARNING)

# Sets required to check for valid onset and coda clusters
VOICELESS = set(['K', 'P', 'T', 'F', 'HH', 'S', 'SH', 'TH', 'CH'])
VOICED = set(['G', 'B', 'D', 'DH', 'V', 'Z', 'ZH', 'JH'])

STOPS = set(['K', 'P', 'T', 'G', 'B', 'D'])
FRICATIVES = set(['F', 'DH', 'HH', 'S', 'SH', 'TH', 'V', 'Z', 'ZH'])
AFFRICATES = set(['CH', 'JH'])
NASALS = set(['M', 'N', 'NG'])
APPROXIMANTS = set(['L', 'R', 'W', 'Y'])
CONSONANTS = STOPS.union(FRICATIVES).union(AFFRICATES).union(NASALS).union(APPROXIMANTS)

S_EXTENDED_CODAS = set(['K', 'P', 'T', 'F', 'TH'])
Z_EXTENDED_CODAS = set(['G', 'B', 'D', 'DH', 'V', 'M', 'N', 'NG', ])

T_EXTENDED_CODAS = set(['K', 'P', 'F', 'S', 'SH', 'TH', 'CH'])
D_EXTENDED_CODAS = set(['G', 'B', 'DH', 'V', 'Z', 'ZH', 'JH'])

# Optional stress markers (0,1,2) after the vowel for flexibility
VOWELS_REGEX = re.compile(r'(?:AA|AE|AH|AO|AW|AY|EH|ER|EY|IH|IY|OW|OY|UW|UH)[012]?')

def syllabifyARPA(arpa_arr):

    word = ' '.join(arpa_arr)

    final_arr = []
    temp_arr = []
    valid = True

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

    # TODO: Code this

    if length == 0:
        return True

    elif length > 4:
        return False

    elif length == 4:
        # 4-phoneme codas have to have /s/ or /z/ as an appendix
        if ((cluster[3] == 'S' and cluster[2] in S_EXTENDED_CODAS)
            or
        (cluster[3] == 'Z' and cluster[2] in Z_EXTENDED_CODAS)):
            length -= 1
        else:
            return False

    elif length == 1:
        # These phonemes cannot exist as codas by themselves
        if cluster[0] in set(['HH', 'W', 'Y']):
            return False

    if length == 3: # if instead of elif to allow checking of s-appended clusters
        if ((cluster[2] == 'S' and cluster[1] in S_EXTENDED_CODAS)
            or
        (cluster[2] == 'Z' and cluster[1] in Z_EXTENDED_CODAS)
            or
        (cluster[2] == 'T' and cluster[1] in T_EXTENDED_CODAS)
            or
        (cluster[2] == 'D' and cluster[1] in D_EXTENDED_CODAS)):
            length -= 1

        elif cluster[0] == 'L' and not (
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
            return False

        elif cluster[0] == 'R' and not (
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
            return False

        elif cluster[0] == 'M' and not (
        (cluster[1] == 'P' and cluster[2] == 'T')
            or
        (cluster[1] == 'P' and cluster[2] == 'S')):
            return False

        elif cluster[0] == 'N' and not (
        (cluster[1] == 'D' and cluster[2] == 'TH')):
            return False

        elif cluster[0] == 'NG' and not (
        (cluster[1] == 'K' and cluster[2] == 'T')
            or
        (cluster[1] == 'K' and cluster[2] == 'S')
            or
        (cluster[1] == 'K' and cluster[2] == 'TH')):
            return False

        elif not (
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'TH')
            or
        (cluster[0] == 'K' and cluster[1] == 'S' and cluster[2] == 'T')):
            return False

    if length == 2: # if instead of elif to allow checking of s-appended clusters
        return True

    return True

"""
STOPS = set(['K', 'P', 'T', 'G', 'B', 'D'])
FRICATIVES = set(['F', 'DH', 'HH', 'S', 'SH', 'TH', 'V', 'Z', 'ZH'])
AFFRICATES = set(['CH', 'JH'])
NASALS = set(['M', 'N', 'NG'])
APPROXIMANTS = set(['L', 'R', 'W', 'Y'])

Lateral approximant plus stop or affricate: /lp/, /lb/, /lt/, /ld/, /ltʃ/, /ldʒ/, /lk/ 	help, bulb, belt, hold, belch, indulge, milk
In rhotic varieties, /r/ plus stop or affricate: /rp/, /rb/, /rt/, /rd/, /rtʃ/, /rdʒ/, /rk/, /rɡ/ 	harp, orb, fort, beard, arch, large, mark, morgue
Lateral approximant + fricative: /lf/, /lv/, /lθ/, /ls/, /lʃ/ 	golf, solve, wealth, else, Welsh
In rhotic varieties, /r/ + fricative: /rf/, /rv/, /rθ/, /rs/, /rz/, /rʃ/ 	dwarf, carve, north, force, Mars, marsh
Lateral approximant + nasal: /lm/, /ln/ 	film, kiln
In rhotic varieties, /r/ + nasal or lateral: /rm/, /rn/, /rl/ 	arm, born, snarl
Nasal + homorganic stop or affricate: /mp/, /nt/, /nd/, /ntʃ/, /ndʒ/, /ŋk/ 	jump, tent, end, lunch, lounge, pink
Nasal + fricative: /mf/, /mθ/, /nθ/, /ns/, /nz/, /ŋθ/ in some varieties 	triumph, warmth, month, prince, bronze, length
Voiceless fricative plus voiceless stop: /ft/, /sp/, /st/, /sk/ 	left, crisp, lost, ask
Two voiceless fricatives: /fθ/ 	fifth
Two voiceless stops: /pt/, /kt/ 	opt, act
Stop plus voiceless fricative: /pθ/, /ps/, /tθ/, /ts/, /dθ/, /ks/ 	depth, lapse, eighth, klutz, width, box
"""
