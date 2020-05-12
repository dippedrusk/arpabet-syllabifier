from syllabifier import syllabifyARPA

def test_syllabifyARPA():
    test_string = 'HH AE NG M AE N'
    assert syllabifyARPA(test_string, return_list=True) == ['HH AE NG', 'M AE N']

def test_unsyllabifiable():
    test_string = 'M G L AA'
    assert not syllabifyARPA(test_string, return_list=True, silence_warnings=True)

def test_empty():
    test_string = ''
    assert not syllabifyARPA(test_string, return_list=True, silence_warnings=True)

def test_sixths():
    test_string = 'S IH K S TH S'
    assert syllabifyARPA(test_string, return_list=True) == ['S IH K S TH S']

def test_lowercase():
    test_string = 'ow'
    assert syllabifyARPA(test_string, return_list=True) == ['OW']

def test_mixedcase():
    test_string = 'oW'
    assert syllabifyARPA(test_string, return_list=True) == ['OW']

def test_non_arpabet():
    test_string = 'GH IY'
    assert not syllabifyARPA(test_string, return_list=True, silence_warnings=True)

def test_array():
    test_array = ['K', 'AE', 'T']
    assert syllabifyARPA(test_array, return_list=True) == ['K AE T']

def test_weird_array():
    test_array = ['K AE', 'T']
    assert not syllabifyARPA(test_array, return_list=True, silence_warnings=True)
