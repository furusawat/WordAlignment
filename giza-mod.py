#
# usage:
# python3 giza-mod.py -a giza.A3.final -o out.align
#

import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-a', required=True)
parser.add_argument('-o', required=True)
args = parser.parse_args()

fp = open(args.a, "r")
aligns = fp.read().split('\n')
fp.close()

outputs = ""

for i in range(1,len(aligns)-1,3):
    outputs += "\n"
    tmp = re.split("\(\{|\}\)",aligns[i+1])
    each_align = ""
    for j in range(2,len(tmp)-1,2):
        outputs += tmp[j][1:]
        for k in tmp[j+1].split(" ")[1:-1]:
            each_align += "{} {}\n".format(int((j-2)/2),int(k)-1)
    outputs += "[EOS]\n" + aligns[i] + "[EOS]\n"
    outputs += each_align

fp = open(args.o, "w")
fp.write(outputs)
fp.close()
