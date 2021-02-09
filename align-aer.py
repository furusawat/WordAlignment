#
# usage:
# python3 align-aer.py -a align.txt -d Downloads/kftt-alignments
#

min_num_of_token = 3
max_num_of_token = 100
ignore_space_eos = True
corpus_adjust = True

rough_load = True

ignore_punc = False
punc = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~！”＃＄％＆’（）＊＋、ー。：；＜＝＞？＠「」＾＿‘｛｜｝～『』"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', required=True)
parser.add_argument('-d', required=True)
args = parser.parse_args()

def AlignMat(align, s_len, t_len, spr=" ", reverse=False):
    tmp_list = [[0 for x in range(t_len)] for y in range(s_len)]
    for i in range(len(align)):
        tmp_align = align[i].split(spr)
        if reverse is False:
            tmp_list[int(tmp_align[0])][int(tmp_align[1])] = 1
        else:
            tmp_list[int(tmp_align[1])][int(tmp_align[0])] = 1
    return tmp_list

class AlignMod():
    def __init__(self, align, eng, jpn):
        self.tk_eng_list = eng.split(" ")
        self.tk_jpn_list = jpn.split(" ")
        self.tk_align_mat = AlignMat(align.split(), len(self.tk_eng_list), len(self.tk_jpn_list), spr="-", reverse=True)
        if rough_load == True:
            tmp_replace1 = "（）＝：％－／１２３４５６７８９０"
            tmp_replace2 = "()=:%-/1234567890"
            for ch in range(len(tmp_replace1)):
                self.tk_jpn_list = [x.replace(tmp_replace1[ch],tmp_replace2[ch]) for x in self.tk_jpn_list]

            self.tk_jpn_list = [x.replace("\u3000","") for x in self.tk_jpn_list]

        self.test_eng_list = "[DUMMYVALUES]"
        self.test_jpn_list = "[DUMMYVALUES]"
        self.test_align_mat = None

    def DebugPrint(self,v=False):
        print(self.tk_eng_list)
        print(self.tk_jpn_list)
        print(self.test_eng_list)
        print(self.test_jpn_list)
        if v is True:
            print(self.tk_align_mat)
            print(self.test_align_mat)

    def AddTest(self, align, eng, jpn):
        if not max_num_of_token >= len(eng.split()) >= min_num_of_token and not max_num_of_token >= len(jpn.split()) >= min_num_of_token:
            print("IGNORED")
            print(eng.split())
            print(jpn.split())
            return
        selftest_eng_list = eng.split(" ")
        selftest_jpn_list = jpn.split(" ")
        selftest_align_mat = AlignMat(align.split("|"), len(selftest_eng_list), len(selftest_jpn_list))
        selftest_eng_list = [x.replace("▁","") for x in selftest_eng_list]
        selftest_jpn_list = [x.replace("▁","") for x in selftest_jpn_list]
        selftest_eng_list[-1] = ""
        selftest_jpn_list[-1] = ""
        if ignore_space_eos is True:
            for ii in range(len(selftest_eng_list)):
                if selftest_eng_list[ii] == "":
                    for j in range(len(selftest_align_mat[0])):
                        selftest_align_mat[ii][j] = 0
            for ii in range(len(selftest_jpn_list)):
                if selftest_jpn_list[ii] == "":
                    for j in range(len(selftest_align_mat)):
                        selftest_align_mat[j][ii] = 0
        selftest_eng_list = [x.lower() for x in selftest_eng_list]
        selftest_jpn_list = [x.lower() for x in selftest_jpn_list]

        if "".join(self.tk_eng_list) != "".join(selftest_eng_list) or "".join(self.tk_jpn_list) != "".join(selftest_jpn_list):
            print("MISMATCHED")
            print(self.tk_eng_list)
            print(selftest_eng_list)
            print(self.tk_jpn_list)
            print(selftest_jpn_list)
            return

        self.test_eng_list = selftest_eng_list
        self.test_jpn_list = selftest_jpn_list
        self.test_align_mat = selftest_align_mat

    def isAvailable(self):
        if "".join(self.tk_eng_list) == "".join(self.test_eng_list) or "".join(self.tk_jpn_list) == "".join(self.test_jpn_list):
            return True
        else:
            return False

    def TestER(self):
        tmp_list = [[0 for x in range(len("".join(self.test_jpn_list)))] for y in range(len("".join(self.test_eng_list)))]
        test_eng_calc = self.test_eng_list.copy()
        ei_tmp = 0
        for ei in range(len(tmp_list)):
            while test_eng_calc[ei_tmp] == "":
                ei_tmp += 1
                if ei_tmp >= len(test_eng_calc):
                    break
            test_jpn_calc = self.test_jpn_list.copy()
            ji_tmp = 0
            for ji in range(len(tmp_list[0])):
                while test_jpn_calc[ji_tmp] == "":
                    ji_tmp += 1
                    if ji_tmp >= len(test_jpn_calc):
                        break
                tmp_list[ei][ji] = self.test_align_mat[ei_tmp][ji_tmp]
                test_jpn_calc[ji_tmp] = test_jpn_calc[ji_tmp][1:]
            test_eng_calc[ei_tmp] = test_eng_calc[ei_tmp][1:]

        tmp_result = [[0 for x in range(len(self.tk_jpn_list))] for y in range(len(self.tk_eng_list))]
        tk_eng_calc = self.tk_eng_list.copy()
        ei_tmp = 0
        for ei in range(len(tmp_list)):
            tk_jpn_calc = self.tk_jpn_list.copy()
            ji_tmp = 0
            for ji in range(len(tmp_list[0])):
                tmp_result[ei_tmp][ji_tmp] += tmp_list[ei][ji]
                tk_jpn_calc[ji_tmp] = tk_jpn_calc[ji_tmp][1:]
                while tk_jpn_calc[ji_tmp] == "":
                    ji_tmp += 1
                    if ji_tmp >= len(tk_jpn_calc):
                        break
            tk_eng_calc[ei_tmp] = tk_eng_calc[ei_tmp][1:]
            if tk_eng_calc[ei_tmp] == "":
                ei_tmp += 1
                while ei_tmp >= len(tk_eng_calc):
                    break
        result = [0,0,0]
        for ii in range(len(tmp_result)):
            for jj in range(len(tmp_result[0])):
                if corpus_adjust is True and (self.tk_eng_list[ii] in ["a","an","the"] or self.tk_jpn_list[jj] in ["が","を","は"]):
                    continue
                if ignore_punc is True and (self.tk_eng_list[ii] in punc or self.tk_jpn_list[jj] in punc):
                    continue
                if tmp_result[ii][jj] != 0 and self.tk_align_mat[ii][jj] != 0:
                    result[0] += 1
                if tmp_result[ii][jj] != 0:
                    result[1] += 1
                if self.tk_align_mat[ii][jj] != 0:
                    result[2] += 1
        return result

fp = open(args.a, "r")
test_aligns = fp.read().split('\n')
fp.close()

fp = open(args.d + "/original/english.txt", "r")
orig_sent = fp.read().split('\n')
fp.close()

fp = open(args.d + "/data/align.txt", "r")
real_aligns = fp.read().split('\n')
fp.close()

fp = open(args.d + "/data/english.txt", "r")
tk_eng = fp.read().split('\n')
fp.close()

fp = open(args.d + "/data/japanese.txt", "r")
tk_jpn = fp.read().split('\n')
fp.close()

dic = {}
for i in range(len(orig_sent)-1):
    if orig_sent[i] not in dic:
        dic[orig_sent[i].replace(" ","").lower()] = AlignMod(real_aligns[i], tk_eng[i], tk_jpn[i])

for ii in range(len(test_aligns)-3):
    if test_aligns[ii] == "":
        i = 1
        tmp = test_aligns[ii + i][:-5].replace(" ","").replace("▁", " ").strip()
        t_eng = test_aligns[ii + i]
        i += 1
        t_jpn = test_aligns[ii + i]
        i += 1
        t_align = ""
        for j in range(ii + i, len(test_aligns)-1):
            if test_aligns[j] == "":
                break
            t_align += test_aligns[j] + "|"
        t_align = t_align[:-1]
        tmp = tmp.replace(" ","").lower()
        if tmp in dic:
            if dic[tmp].isAvailable() is True:
                print("DUPLICATED")
                print(t_eng.split())
                print(t_jpn.split())
                continue
            dic[tmp].AddTest(t_align, t_eng, t_jpn)
        else:
            print("NOT FOUND")
            print(t_eng.split())
            print(t_jpn.split())


print(len(dic))

for k in list(dic):
    if dic[k].isAvailable() is False:
        del dic[k]

print(len(dic))

total = [0, 0, 0]
for i,k in enumerate(list(dic)):
    total = [total+x for total,x in zip(total,dic[k].TestER())]

print(total)
prec = total[0]/total[1]
rec = total[0]/total[2]
print("Prec: {:.3f}".format(prec))
print("Rec: {:.3f}".format(rec))
print("F1: {:.3f}".format((2*prec*rec)/(prec+rec)))
print("AER: {:.3f}".format(1-(2*total[0])/(total[1]+total[2])))
