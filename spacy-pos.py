#
# Purpose:
# Get SpaCy POS tagging information of KFTT alignment data to work with raw-aer.py
#
# usage:
# python3 spacy-pos.py -e kftt-alignments/original/english.txt > pos.en
# python3 spacy-pos.py -j kftt-alignments/original/japanese.txt > pos.ja
#

import argparse
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('-e')
parser.add_argument('-j')
args = parser.parse_args()

if args.e is not None:
    nlp = spacy.load("en_core_web_sm")
    fp = open(args.e, "r")
elif args.j is not None:
    nlp = spacy.load("ja_core_news_sm")
    fp = open(args.j, "r")
else:
    quit()

texts = fp.read().split("\n")
fp.close()
output_lists = texts[:-1]

for ii in range(len(texts)-1):
    doc = nlp(texts[ii])

    for token in doc:
        output_lists[ii] += "\t{}\t{}".format(token.pos_,token.text)

    output_lists[ii] = output_lists[ii].replace(" ","").replace("　","").lower()

print("\n".join(output_lists))
