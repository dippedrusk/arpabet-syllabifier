# ARPABET Syllabifier

syllabifyARPA is a function that will take an ARPABET transcription in array or string form and return a Pandas Series with the syllables chunked.

This is a work in progress and testing is not yet complete.

## How to use
* Download and add the source `syllabifyARPA.py` to your project.
* Import the function with `from syllabifyARPA import syllabifyARPA`.
* Call it with `syllabifyARPA(transcription)` for individual transcriptions
* Use `pd.Series.apply(syllabifyARPA)` for Pandas Series.

Sample calls are in the Jupyter Notebook test.ipynb, using CMU Pronouncing Dictionary data.

## ARPABET
ARPABET is a method of transcribing General American English phonetically with only ASCII characters. Refer [here](https://en.wikipedia.org/wiki/ARPABET) for a table of mappings between IPA and ARPABET. This syllabifier accepts only the 2-letter ARPABET codes as of now.

## CMUDict
The Carnegie Mellon University Pronouncing Dictionary is an open-source pronunciation dictionary for North American English. It contains ARPABET transcriptions of 100,000+ words with lexical stress markers on the vowels. A copy of the .txt file is included in this repository along with a guide to the ARPABET representations in phoneset.txt.
