dic_e = []
for i in range(21):
    # print(f + str(i))
    f = 'Frame' + str(i)
    fi = open('./' + f, 'r').read().strip()
    a = int(fi[256*1:256*2], 16)
    if a not in dic_e:
        dic_e.append(a)
print(dic_e)

dic_3 = []
dic_5 = []
dic_65537 = []
dic_4678 = []
dic_1522 = []
for i in range(21):
    f = 'Frame' + str(i)
    fi = open('./' + f, 'r').read().strip()
    a = int(fi[256*1:256*2], 16)
    if a == 3:
        dic_3.append(f)
    if a == 5:
        dic_5.append(f)
    if a == 65537:
        dic_65537.append(f)
    if str(a)[:4] == '4678':
        dic_4678.append(f)
    if str(a)[:4] == '1522':
        dic_1522.append(f)
print(dic_3)
print(dic_5)
print(dic_65537)
print(dic_4678)
print(dic_1522)