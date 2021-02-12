#
# Purpose:
# Get KyTea POS tagging information of KFTT alignment data to work with raw-aer.py
#
# usage:
# kytea Downloads/kftt-alignments/data/japanese.txt -in tok -tagbound "|" > kytea.txt
# python3 kytea-pos.py -j kytea.txt > pos.ja.kytea
#

import argparse
import spacy

parser = argparse.ArgumentParser()
parser.add_argument('-j',required=True)
args = parser.parse_args()

fp = open(args.j, "r")
texts = fp.read().split("\n")
fp.close()
output_lists = ["" for x in range(len(texts)-1)]

for ii in range(len(texts)-1):
    doc = texts[ii].split(" ")
    for token in doc:
        output_lists[ii] += token.split("|")[0]

    for token in doc:
        tmp = token.split("|")
        output_lists[ii] += "\t{}\t{}".format(tmp[1],tmp[0])

    output_lists[ii] = output_lists[ii].replace(" ","").replace("　","").lower()

print("\n".join(output_lists))
