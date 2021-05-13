#
# usage:
# python3 raw-aer-diff.py -first result1.txt -second result2.txt > out.html
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-first', required=True)
parser.add_argument('-second', required=True)
args = parser.parse_args()

fp = open(args.first)
first = fp.read().split("\n")[:-1]
firstname = args.first
fp.close()
fp = open(args.second)
second = fp.read().split("\n")[:-1]
secondname = args.second
fp.close()

table = []

for i in range(1,41):
    tmp = first[-2*i].split(":")[0]
    for j in range(1,41):
        if tmp == second[-2*j].split(":")[0]:
            entry = {}
            entry["pair"] = tmp
            index = 0
            for jj in range(3):
                index = first[-2*i+1].find(":",index+1)
                entry["first"+str(jj)] = first[-2*i+1][index+2:index+7]
            index = 0
            for jj in range(3):
                index = second[-2*j+1].find(":",index+1)
                entry["second"+str(jj)] = second[-2*j+1][index+2:index+7]
            for jj in range(3):
                entry["diff"+str(jj)] = float(entry["first"+str(jj)]) - float(entry["second"+str(jj)])
            table += [entry]

print("<!DOCTYPE html><html><head><style>")
print("table,tr,td{border:1px solid black}</style></head>")
print("<body>")

print("<table>")
for k in table:
    print("<tr><td colspan='9'>{}</td></tr>".format(k["pair"]))
    print("<tr>")
    print("<td colspan='3'>{}</td>".format(firstname))
    print("<td colspan='3'>{}</td>".format(secondname))
    print("<td colspan='3'>diff</td>")
    print("</tr>")
    print("<tr>")
    for i in range(3):
        print("<td>{}</td>".format(k["first"+str(i)]))
    for i in range(3):
        print("<td>{}</td>".format(k["second"+str(i)]))
    for i in range(3):
        print("<td>{}</td>".format(k["diff"+str(i)]))
    print("</tr>")

print("</table>")

print("</body></html>")
