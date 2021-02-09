#
# usage:
# python3 raw-aer.py -a align.txt -r ref.txt -ep pos.en -jp pos.ja
#

min_num_of_token = 3
max_num_of_token = 100

rough_load = True
tmp_replace1 = "（）＝：％－／１２３４５６７８９０"
tmp_replace2 = "()=:%-/1234567890"
ignore_space_eos = True

corpus_adjust = False
ignore_punc = False
punc = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~！”＃＄％＆’（）＊＋、ー。：；＜＝＞？＠「」＾＿‘｛｜｝～『』"

debug = False

pos_result = {}

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-a', required=True)
parser.add_argument('-r', required=True)
parser.add_argument('-ep', required=True)
parser.add_argument('-jp', required=True)
args = parser.parse_args()

def AlignMat(align, s_len, t_len):
    tmp_list = [[0 for x in range(t_len)] for y in range(s_len)]
    for i in range(len(align)):
        tmp_align = align[i].split(" ")
        tmp_list[int(tmp_align[0])][int(tmp_align[1])] = 1
    return tmp_list

class AlignMod():
    def __init__(self, align, eng, jpn):
        self.tk_eng_list = eng.split(" ")
        self.tk_jpn_list = jpn.split(" ")
        self.tk_align_mat = AlignMat(align.split("|"), len(self.tk_eng_list), len(self.tk_jpn_list))
        if rough_load == True:
            for ch in range(len(tmp_replace1)):
                self.tk_jpn_list = [x.replace(tmp_replace1[ch],tmp_replace2[ch]) for x in self.tk_jpn_list]
            self.tk_jpn_list = [x.replace("　","") for x in self.tk_jpn_list]
            self.tk_jpn_list = [x.replace("□","") for x in self.tk_jpn_list]

        self.test_eng_list = "[DUMMYVALUES]"
        self.test_jpn_list = "[DUMMYVALUES]"
        self.test_align_mat = None
        self.en_pos = None
        self.ja_pos = None

    def AddTest(self, align, eng, jpn):
        if not max_num_of_token >= len(eng.split(" ")) >= min_num_of_token and not max_num_of_token >= len(jpn.split(" ")) >= min_num_of_token:
            if debug == True:
                print("IGNORED")
                print(eng)
                print(jpn)
            return
        selftest_eng_list = eng.split(" ")
        selftest_jpn_list = jpn.split(" ")
        selftest_align_mat = AlignMat(align.split("|"), len(selftest_eng_list), len(selftest_jpn_list))
        if rough_load == True:
            for ch in range(len(tmp_replace1)):
                selftest_jpn_list = [x.replace(tmp_replace1[ch],tmp_replace2[ch]) for x in selftest_jpn_list]
            selftest_jpn_list = [x.replace("　","") for x in selftest_jpn_list]
            selftest_jpn_list = [x.replace("□","") for x in selftest_jpn_list]

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
            if debug == True:
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
        tmp_en_pos = ["x" for y in range(len(self.tk_eng_list))]
        tmp_ja_pos = ["x" for x in range(len(self.tk_jpn_list))]
        tk_eng_calc = self.tk_eng_list.copy()
        ei_tmp = 0
        for ei in range(len(tmp_list)):
            tmp_en_pos[ei_tmp] = self.en_pos.GetPOS(ei,tk_eng_calc[ei_tmp][0])
            tk_jpn_calc = self.tk_jpn_list.copy()
            ji_tmp = 0
            for ji in range(len(tmp_list[0])):
                tmp_ja_pos[ji_tmp] = self.ja_pos.GetPOS(ji,tk_jpn_calc[ji_tmp][0])
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
                if tmp_en_pos[ii] not in pos_result:
                    pos_result[tmp_en_pos[ii]] = {}
                if tmp_ja_pos[jj] not in pos_result[tmp_en_pos[ii]]:
                    pos_result[tmp_en_pos[ii]][tmp_ja_pos[jj]] = [0,0,0]
                if tmp_result[ii][jj] != 0 and self.tk_align_mat[ii][jj] != 0:
                    pos_result[tmp_en_pos[ii]][tmp_ja_pos[jj]][0] += 1
                    result[0] += 1
                if tmp_result[ii][jj] != 0:
                    pos_result[tmp_en_pos[ii]][tmp_ja_pos[jj]][1] += 1
                    result[1] += 1
                if self.tk_align_mat[ii][jj] != 0:
                    pos_result[tmp_en_pos[ii]][tmp_ja_pos[jj]][2] += 1
                    result[2] += 1
        return result

class POS:
    def __init__(self, pos):
        self.poss=[]
        self.texts=[]
        for i in range(0,len(pos),2):
            self.poss+=[pos[i]]
            self.texts+=[pos[i+1]]

    def GetPOS(self, num, char):
        tmp=0
        for i in range(len(self.texts)):
            tmp+=len(self.texts[i])
            if num < tmp:
                if self.texts[i][len(self.texts[i])-tmp+num] == char:
                    return self.poss[i]
                else:
                    return None
        return None

en_pos_dic = {}
fp = open(args.ep, "r")
tmp_pos = fp.read().split('\n')
fp.close()

for i in range(len(tmp_pos)-1):
    tmp = tmp_pos[i].split("\t")
    en_pos_dic[tmp[0]] = POS(tmp_pos[i].split("\t")[1:])

ja_pos_dic = {}
fp = open(args.jp, "r")
tmp_pos = fp.read().split('\n')
fp.close()

for i in range(len(tmp_pos)-1):
    tmp = tmp_pos[i].split("\t")
    if rough_load == True:
        for ch in range(len(tmp_replace1)):
            tmp = [x.replace(tmp_replace1[ch],tmp_replace2[ch]) for x in tmp]
        tmp = [x.replace("　","") for x in tmp]
        tmp = [x.replace("□","") for x in tmp]
    ja_pos_dic[tmp[0]] = POS(tmp[1:])

fp = open(args.a, "r")
test_aligns = fp.read().split('\n')
fp.close()

fp = open(args.r, "r")
ref_aligns = fp.read().split('\n')
fp.close()


dic = {}
for ii in range(len(ref_aligns)-3):
    if ref_aligns[ii] == "":
        i = 1
        tmp = ref_aligns[ii + i][:-5].strip()
        t_eng = ref_aligns[ii + i][:-5]
        i += 1
        t_jpn = ref_aligns[ii + i][:-5]
        i += 1
        t_align = ""
        for j in range(ii + i, len(ref_aligns)-1):
            if ref_aligns[j] == "":
                break
            t_align += ref_aligns[j] + "|"
        t_align = t_align[:-1]
        tmp = tmp.replace(" ","").lower()
        if tmp not in dic:
            dic[tmp] = AlignMod(t_align, t_eng, t_jpn)

for ii in range(len(test_aligns)-3):
    if test_aligns[ii] == "":
        i = 1
        tmp = test_aligns[ii + i][:-5].replace("▁", "").strip()
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
                if debug == True:
                    print("DUPLICATED")
                    print(t_eng)
                    print(t_jpn)
                continue
            dic[tmp].AddTest(t_align, t_eng, t_jpn)
            dic[tmp].en_pos = en_pos_dic["".join(dic[tmp].tk_eng_list)]
            dic[tmp].ja_pos = ja_pos_dic["".join(dic[tmp].tk_jpn_list)]
        elif debug == True:
            print("NOT FOUND")
            print(t_eng)
            print(t_jpn)

print(len(dic))

for k in list(dic):
    if dic[k].isAvailable() is False:
        del dic[k]

print(len(dic))

total = [0, 0, 0]
for i,k in enumerate(list(dic)):
    total = [total+x for total,x in zip(total,dic[k].TestER())]
    if i % 100 == 99:
        print(i)

print(total)
prec = total[0]/total[1]
rec = total[0]/total[2]
print("Prec: {:.3f}".format(prec))
print("Rec: {:.3f}".format(rec))
print("F1: {:.3f}".format((2*prec*rec)/(prec+rec)))
print("AER: {:.3f}".format(1-(2*total[0])/(total[1]+total[2])))

final_result = []

for k in list(pos_result):
    for l in list(pos_result[k]):
        total = pos_result[k][l]
        prec = 0.0
        rec = 0.0
        f1 = 0.0
        aer = 1.0
        if total[1] != 0:
            prec = total[0]/total[1]
        if total[2] != 0:
            rec = total[0]/total[2]
        if prec+rec != 0:
            f1 = (2*prec*rec)/(prec+rec)
        if total[1]+total[2] != 0:
            aer = 1-(2*total[0])/(total[1]+total[2])
        final_result += [[total[1]+total[2]-total[0],"{}->{}:\t{}\n(Prec: {:.3f} Rec: {:.3f} F1: {:.3f} AER: {:.3f})".format(k,l,total,prec,rec,f1,aer)]]

final_result = sorted(final_result, key=lambda x: x[0])

for i in final_result:
    if debug == True or i[0] > 100:
        print(i[1])
