#
# Purpose:
# Extract word alignment information from fairseq outputs and save it in preferred format
#
# nohup.out:
# stdout logs from github.com/furusawat/fairseq
#
# usage:
# python3 extract-align.py -i nohup.out -o align.txt
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', required=True)
parser.add_argument('-o', required=True)
args = parser.parse_args()

fp = open(args.i, "r")
texts = fp.read().split("\n")
fp.close()
output_lists = []

cnt = 0

for ii in range(len(texts)-3):
    if texts[ii] == "":
        output_texts = "\n"
        i = 1
        output_texts += texts[ii + i] + " [EOS]" + "\n"
        i += 1
        output_texts += texts[ii + i] + " [EOS]" + "\n"
        i += 1
        for j in range(ii + i, len(texts)-1):
            if texts[j][0] == " ":
                continue
            elif texts[j][0] == "\t":
                output_lists += [[float(texts[j][1:]),output_texts]]
                break
            output_texts += texts[j] + "\n"
        cnt += 1

output_lists = sorted(output_lists, key=lambda x: x[0])

output_texts = ""
for ii in output_lists:
    output_texts += ii[1]

fp = open(args.o, "w")
fp.write(output_texts)
fp.close()

print(cnt)
