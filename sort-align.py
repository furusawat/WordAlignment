#
# Purpose:
# Extract word alignment data among the certain range of sentence length
#
# align.txt:
# Generated from extract-align.py, giza-mod.py
#
# usage:
# python3 sort-align.py -i align.txt -o align.sorted --lower 50 --upper 100
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
parser.add_argument('-o', required=True)
parser.add_argument('--lower', default=50, type=int)
parser.add_argument('--upper', default=100, type=int)
args = parser.parse_args()

fp = open(args.i, "r")
texts = fp.read().split("\n")
fp.close()

output_lists = []
cnt=0

tmp_texts = ""
for i in range(len(texts)-1):
    if texts[i] == "":
        if tmp_texts == "":
            continue
        tmp_len = len(tmp_texts.split("\n")[0])
        if args.lower <= tmp_len <= args.upper:
            output_lists += [[tmp_len,tmp_texts+"\n"]]
            cnt+=1
        tmp_texts = ""
    else:
        tmp_texts+=texts[i]+"\n"

output_lists = sorted(output_lists, key=lambda x: x[0])

output_texts = ""
for ii in output_lists:
    output_texts += ii[1]

fp = open(args.o, "w")
fp.write(output_texts)
fp.close()

print(cnt)
