from syllabifyARPA import syllabifyARPA

def test_syllabifyARPA():
    test_string = 'HH AE NG M AE N'
    assert syllabifyARPA(test_string, return_list=True) == ['HH AE NG', 'M AE N']
