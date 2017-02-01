# text_utils


1. generate lists of potential affixes with `./1affix_finder.py`. Outputs to `/1_affixes/`. Add your selection of those affixes in `/1b_affixes_selection/`. 
2.  find all words containing an affix with `./2find_root_suffixes.py`. Outputs to `/2a_roots_suffixes/`. Add your selection to `/2b_roots_suffixes_selection/`.
3. with `/3additions.py` format Monlam verbs and particles (found in `/3ressources/`)for `families.txt` and writes to `/3additions/lemmas.txt`
4. [TODO] format `2b_roots_suffixes_selection` content for `families.txt`, appending  `/3additions/lemmas.txt`.
5. generate raw headword lists with `/5stemmer.py`
6. check your headwords manually and you're done!
...

In progress:

...

To do:

File Pre-processing for Corpus Analysis - A script that takes a sub-set of corpus files (the 95 separate files that are all "Speech_Dialogs", for example) and dumps all their content into a single .txt file (Speech_Dialogs.txt in this case). Should be able to handle multiple input encodings and output should be in Unicode (a tool like WordSmith, for example, only likes Unicode). 

Pre-processing Tsheg-stripper: Takes any series of half-spaces, spaces, returns, line breaks, and line starts and normalizes them to a normal single space. Strips end tshegs and/or double tshegs. (The goal being a very standardized text where a single white space separates each and every Tibetan word).

Lemmatizer & POS tagger: A script that adds POS & Lemma info tags to text. 
