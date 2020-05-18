#!/usr/bin/env python3
import itertools
import pytest
from syllabifier import syllabifyARPA
from syllabifier.constants import CONSONANTS
from syllabifier.constants import PHONESET

VOWELS = PHONESET - CONSONANTS
legal_codas = CONSONANTS - {'HH', 'W', 'Y'}
legal_onsets = CONSONANTS - {'NG'}


def test_syllabifyARPA():
    test_string = 'HH AE NG M AE N'
    assert syllabifyARPA(test_string) == ['HH AE NG', 'M AE N']


def test_non_ARPABET_phones():
    test_string = 'banana'
    with pytest.raises(ValueError, match='contains non-ARPABET phones'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_no_vowel():
    test_string = 'K R F JH'
    with pytest.raises(ValueError, match='no vowel in'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)
    test_string = 'K S'
    with pytest.raises(ValueError, match='no vowel in'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_bad_onset_cluster():
    test_string = 'M G L AA'
    with pytest.raises(ValueError, match='Bad onset cluster'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_NG_onset():
    test_string = 'NG OW'
    with pytest.raises(ValueError, match='Bad onset cluster'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_bad_coda():
    test_string = 'AE G R P'
    with pytest.raises(ValueError, match='Bad coda cluster'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_length_5_coda():
    test_string = 'AE N G L S F'
    with pytest.raises(ValueError, match='Bad coda cluster'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_length_4_coda():
    test_string = 'AE N S G F'
    with pytest.raises(ValueError, match='Bad coda cluster'):
        syllabifyARPA(test_string)
    assert not syllabifyARPA(test_string, silence_warnings=True)
    test_string = 'S IH K S TH S'
    assert syllabifyARPA(test_string) == [test_string]


def test_empty():
    test_string = ''
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_sixths():
    test_string = 'S IH K S TH S'
    assert syllabifyARPA(test_string) == ['S IH K S TH S']


def test_lowercase():
    test_string = 'ow'
    assert syllabifyARPA(test_string) == ['OW']


def test_mixedcase():
    test_string = 'oW'
    assert syllabifyARPA(test_string) == ['OW']


def test_non_arpabet():
    test_string = 'GH IY'
    assert not syllabifyARPA(test_string, silence_warnings=True)


def test_array():
    test_array = ['K', 'AE', 'T']
    assert syllabifyARPA(test_array) == ['K AE T']


def test_weird_array():
    test_array = ['K AE', 'T']
    assert not syllabifyARPA(test_array, silence_warnings=True)


def test_CVC_syllables():
    for syllable in itertools.product(legal_onsets, VOWELS, legal_codas):
        assert syllabifyARPA(list(syllable))


def test_SZ_extension():
    not_sz_extendable = {'S', 'SH', 'Z', 'ZH', 'CH', 'JH'}
    sz_extendable_codas = legal_codas - not_sz_extendable
    for syllable in itertools.product(legal_onsets, VOWELS, sz_extendable_codas):
        s_extended = list(syllable) + ['S']
        z_extended = list(syllable) + ['Z']
        assert (syllabifyARPA(s_extended, silence_warnings=True) !=
                syllabifyARPA(z_extended, silence_warnings=True))


def test_TD_extension():
    not_td_extendable = {'T', 'D'}
    td_extendable_codas = legal_codas - not_td_extendable
    for syllable in itertools.product(legal_onsets, VOWELS, td_extendable_codas):
        t_extended = list(syllable) + ['T']
        d_extended = list(syllable) + ['D']
        assert (syllabifyARPA(t_extended, silence_warnings=True) !=
                syllabifyARPA(d_extended, silence_warnings=True))


def test_CCVC_syllables():
    syllables = ['P L EY', 'D R IY M', 'HH Y UW JH', 'S L IY P', 'G W AA M', 'T W IH N', 'K R AW D']
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_CVCC_syllables():
    syllables = ['HH EH L P', 'W EH L SH', 'F IH F TH', 'L AH NG Z', 'B EH L T', 'T AE K T']
    # TODO:FIX for mensch
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_V_syllables():
    syllables = ['OW', 'AY', 'UW', 'AA', 'EY']
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_CVCCC_syllables():
    syllables = [
        'Y EH L P S', 'K AE L K S', 'W AO R M TH', 'W IH L S T', 'JH IH NG K S', 'M IH L K T',
        'P AH M P T'
    ]
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_CCVCCC_syllables():
    syllables = [
        'K R AE M P T', 'B L IH NG K T', 'T W AE NG G D'
    ]
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_CCVCC_syllables():
    syllables = [
        'TH W AO R T', 'K L AH T S', 'B L AH N T', 'F Y OW R D', 'G R IH N CH'
    ]
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]


def test_s_clusters():
    syllables = [
        'S P OW R T', 'S M AY L', 'S F IH NG K S', 'S P Y UW', 'S T AH D', 'S K W EY R',
        'S T R AY K']
    for syllable in syllables:
        assert syllabifyARPA(syllable) == [syllable]
    prons_syllabified = {
        'S F R AH JH IH S T IH K S': ['S F R AH', 'JH IH', 'S T IH K S'],
        'B L AE S T IH D': ['B L AE', 'S T IH D'],
        'S K L EY R AH': ['S K L EY', 'R AH'],
        'S T EH TH AH S K OW P': ['S T EH', 'TH AH', 'S K OW P']
    }
    for pron, syllabification in prons_syllabified.items():
        assert syllabifyARPA(pron) == syllabification


def test_long_words():
    prons_syllabified = {
        'AH S F IH K S IY EY T AH D': ['AH', 'S F IH K', 'S IY', 'EY', 'T AH D'],
        'M AY K R AH S K AA P IH K': ['M AY', 'K R AH', 'S K AA', 'P IH K'],
        'N Y UH M AE T IH K S': ['N Y UH', 'M AE', 'T IH K S'],
        'F L AE JH AH L EY SH AH N Z': ['F L AE', 'JH AH', 'L EY', 'SH AH N Z'],
        'CH AA R L S T AH N': ['CH AA R L', 'S T AH N'],
        'JH AH M P T B AE K': ['JH AH M P T', 'B AE K'],
        'K R UW S CH Y AO F': ['K R UW S', 'CH Y AO F'],
        'TH AW Z AH N D TH': ['TH AW', 'Z AH N D TH'],
    }
    for pron, syllabification in prons_syllabified.items():
        assert syllabifyARPA(pron) == syllabification


# def test_word_boundaries():
# TODO:ADD this feature
#        'S W IY P S T EY K S': ['S W IY P', 'S T EY K S']
#        'S EH S AH M IY S T R IY T': ['S EH', 'S AH', 'M IY', 'S T R IY T'

# def test_syllabic_consonant_nuclei():
# TODO: ADD this feature
# len(syllabifyARPA('B IY T L') == len(syllabifyARPA('B IY T AH L')
# syllabifyARPA('B IY T L') == ['B IY', 'T L']
