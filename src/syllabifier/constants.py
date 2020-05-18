#!/usr/bin/env python3
import re

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
