# Syllabifier

[![Build Status](https://img.shields.io/github/workflow/status/vgautam/arpabet-syllabifier/Test/main)](https://coveralls.io/github/vgautam/arpabet-syllabifier?branch=main) [![Coverage Status](https://coveralls.io/repos/github/vgautam/arpabet-syllabifier/badge.svg?branch=main)](https://coveralls.io/github/vgautam/arpabet-syllabifier?branch=main)

Syllabifier is a Python module to syllabify your English pronunciations. Currently only
ARPABET syllabification is supported.
It will take an ARPABET transcription in array or string form and return a list with the syllables
chunked.

## Dependencies

* python>=3.5
* jupyter>=1.0.0 (only if you want to run the test notebook locally)

## How to Use

* Install `syllabifier` by running `python setup.py install`
* Import the function `from syllabifier import syllabifyARPA`.
* Function parameters
  * A 2-letter ARPABET transcription in string form (with phones delimited by spaces) or as a Python list (stress markers on the vowels are optional)
  * (Optional) bool silence_warnings to suppress ValueErrors thrown because of unsyllabifiable input
* Sample calls are in the Jupyter Notebook test.ipynb, using CMU Pronouncing Dictionary data.

## Contents
* **syllabifier.py**: Core module of this repository which contains all the code that syllabifies an ARPABET transcription
* **tests/test.ipynb**: Jupyter Notebook demonstrating sample calls to syllabifyARPA using CMUDict data
* **tests/cmudict.txt**: Very large text file containing over 100,000 ARPABET-syllabified English words
* **tests/cmusubset.txt**: Subset of ~60 words and transcriptions from the CMU Dictionary text file for testing convenience
* **tests/test_syllabifier.py**: Unit and integration tests for the package

## ARPABET
ARPABET is a method of transcribing General American English phonetically with only ASCII characters. Refer [here](https://en.wikipedia.org/wiki/ARPABET) for a table of mappings between IPA and ARPABET. This syllabifier accepts only the 2-letter ARPABET codes but case does not matter.

## CMUDict
The [Carnegie Mellon University Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) is an open-source pronunciation dictionary for North American English. It contains ARPABET transcriptions of 100,000+ words with lexical stress markers on the vowels.

## English Syllabification Rules
The syllabification rules that this function is based on are from [this Wikipedia article](https://en.wikipedia.org/wiki/English_phonology#Syllable_structure), so they should be treated with some suspicion. In addition, I added a few clusters as being acceptable at my own discretion based on my judgment as a native English speaker and errors thrown when running the code on the CMUDict data. Most of these correspond to clusters that have come from loanwords, e.g., SH-N as in schnappes.

## Learning Log

* Tried to use a sonority-based approach to syllabification but found the explicit lists of acceptable clusters much easier to deal with
* Had some fun with Python regex before deciding to go with sets to group phones (except for vowels)
* Used Python sets for the first time
* Experimented with the logging module and debugged most of the program using the log files I generated
* Created a function in Python with optional parameters for the first time - this was more exciting than it perhaps should have been
* Did some good documentation of my code based on the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#Comments)
* Literally my first time adding CI to a repo
