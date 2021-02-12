#
# Purpose:
# Get word alignment data of KFTT to work with raw-aer.py
#
# usage:
# python3 align-aer.py -d Downloads/kftt-alignments > ref.txt
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', required=True)
args = parser.parse_args()

fp = open(args.d + "/data/align.txt", "r")
real_aligns = fp.read().split('\n')
fp.close()

fp = open(args.d + "/data/english.txt", "r")
tk_eng = fp.read().split('\n')
fp.close()

fp = open(args.d + "/data/japanese.txt", "r")
tk_jpn = fp.read().replace("　","□").split('\n')
fp.close()

for i in range(len(real_aligns)-1):
    print()
    print(tk_eng[i] + " [EOS]")
    print(tk_jpn[i] + " [EOS]")
    tmp_aligns = real_aligns[i].split()
    for j in range(len(tmp_aligns)):
        swap_align = tmp_aligns[j].split("-")
        print(swap_align[1] + " " + swap_align[0])
