#
# Required resources can be downloaded from https://tatoeba.org/jpn/downloads
#

fp1=open("jpn_sentences.tsv")
fp2=open("eng_sentences.tsv")
fpL=open("links.csv")

result=""

dic1={}
dic2={}
dicL={}

while True:
    tmp=fp1.readline()[:-1].split("\t")
    if(tmp==[""]):
        break
    dic1[tmp[0]]=tmp[2]

while True:
    tmp=fp2.readline()[:-1].split("\t")
    if(tmp==[""]):
        break
    dic2[tmp[0]]=tmp[2]

while True:
    tmp=fpL.readline()[:-1].split("\t")
    if(tmp==[""]):
        break
    if tmp[0] not in dicL.keys():
        dicL[tmp[0]]=[tmp[1]]
    else:
        dicL[tmp[0]]+=[tmp[1]]

for k,v in dic1.items():
    if k in dicL.keys():
        for vtmp in dicL[k]:
            if vtmp in dic2.keys():
                result+="{}\t{}\n".format(v,dic2[vtmp])
        
print(result,end="")

fp1.close()
fp2.close()
fpL.close()
