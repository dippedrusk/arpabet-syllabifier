#import nltk
import numpy as np
import pandas as pd
import re

#df = pd.read_csv("cmudict.txt", delimiter="\n", header=None, quoting=3, comment="#", names=["dict"])
df = pd.read_csv("cmusubset.txt", delimiter="\n", header=None, names=["dict"])
df = df[df['dict'].str.contains(r"[^A-Z0-2 ]") == False]
df = df['dict'].str.extract(r"(?P<word>\w+) (?P<transcription>.+)", expand=True)

vowelsregex = re.compile(r'(?:AA|AE|AH|AO|AW|AY|EH|ER|EY|IH|IY|OW|OY|UW|UH)[012]')

df['transcriptionsplit'] = df['transcription'].str.split()

def syllabifyARPA(arpa_arr):

    final_arr = []
    temp_arr = []

    # Append till and including vowels
    for i in range(len(arpa_arr)):
        temp_arr.append(arpa_arr[i])
        if re.match(vowelsregex, arpa_arr[i]):
            final_arr.append(temp_arr)
            temp_arr = []

    # Handle potential remaining coda consonants
    for i in range(len(temp_arr)):
        if len(final_arr) < 1:
            print("Input error - no vowel. Transcription /", ' '.join(arpa_arr), "/ cannot be syllabified.")
            return None
        final_arr[-1].append(temp_arr[i])

    # All onsets are maximized, some are illegal - fixing that
    for i in range(len(final_arr)):
        c = testLegalOnset(final_arr[i])
        if c:
            print("There is a bad onset cluster in /", ' '.join(final_arr[i]), "/.")

    return [' '.join(syllable) for syllable in final_arr]

def testLegalOnset(syllable):


    for i in range(len(syllable)):
        c = syllable[i]
        if re.match(vowelsregex, c):
            return None
        else:
            

df['syllables'] = df['transcriptionsplit'].apply(syllabifyARPA)
df.dropna(inplace=True)

plosives = set(['B', 'D', 'G', 'K', 'P', 'T'])
fricatives = set(['F', 'DH', 'HH', 'S', 'SH', 'TH', 'V', 'Z', 'ZH'])
"""
F	fee	F IY
DH	thee	DH IY
HH	he	HH IY
S	sea	S IY
SH	she	SH IY
TH	theta	TH EY T AH
V	vee	V IY
Z	zee	Z IY
ZH	seizure	S IY ZH ER

CH	cheese	CH IY Z
JH	gee	JH IY

M	me	M IY
N	knee	N IY
NG	ping	P IY NG

L	lee	L IY

R	read	R IY D

W	we	W IY
Y	yield	Y IY L D
"""

All single consonant phonemes except /ŋ/

Stop plus approximant other than /j/:
/pl/, /bl/, /kl/, /ɡl/, /pr/, /br/, /tr/,[1] /dr/,[1] /kr/, /ɡr/, /tw/, /dw/, /ɡw/, /kw/, /pw/
	play, blood, clean, glove, prize, bring, tree,[1] dream,[1] crowd, green, twin, dwarf, language, quick, puissance

Voiceless fricative or /v/ plus approximant other than /j/:[2]
/fl/, /sl/, /θl/,[3] /fr/, /θr/, /ʃr/, /hw/,[4] /sw/, /θw/, /vw/
	floor, sleep, thlipsis,[3] friend, three, shrimp, what,[4] swing, thwart, reservoir

Consonant plus /j/ (before /uː/ or its modified/reduced forms[5]):
/pj/, /bj/, /tj/,[5] /dj/,[5] /kj/, /ɡj/, /mj/, /nj/,[5] /fj/, /vj/, /θj/,[5] /sj/,[5] /zj/,[5] /hj/, /lj/[5]
	pure, beautiful, tube,[5] during,[5] cute, argue, music, new,[5] few, view, thew,[5] suit,[5] Zeus,[5] huge, lurid[5]

/s/ plus voiceless stop:[6]
/sp/, /st/, /sk/
	speak, stop, skill

/s/ plus nasal other than /ŋ/:[6]
/sm/, /sn/
	smile, snow

/s/ plus voiceless fricative:[3]
/sf/, /sθ/
	sphere, sthenic

/s/ plus voiceless stop plus approximant:[6]
/spl/, /skl/,[3] /spr/, /str/, /skr/, /skw/, /smj/, /spj/, /stj/,[5] /skj/
	split, sclera, spring, street, scream, square, smew, spew, student,[5] skewer

/s/ plus voiceless fricative plus approximant:[3]
/sfr/
