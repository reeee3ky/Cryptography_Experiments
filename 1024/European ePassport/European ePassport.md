```python
# coding=utf-8
# 参考：https://www.codenong.com/cs109540921/
# 中文官方文档：https://www.icao.int/publications/Documents/9303_p11_cons_zh.pdf

from Crypto.Cipher import AES
import base64
import hashlib
import libnum

# 计算到期日校验位
date = [1, 1, 1, 1, 1, 6]
data = [7, 3, 1, 7, 3, 1]
date_check_bit = 0
for i in range(len(date)):
    date_check_bit += date[i] * data[i]
date_check_bit %= 10
# date_check_bit = 7

passport_info = '12345678<811101821111167'
k_seed = hashlib.sha1(passport_info.hexdigest()[:32]
c = '00000001'
D = k_seed + c
K = hashlib.sha1(D.decode('hex')).hexdigest()
k_a = K[:16]
k_b = K[16:32]
# print(type(k_a), k_b)

def check(str):
    check_list = []
    key = ''
    for i in range(0, len(str), 2):
        check_list.append(bin(int(str[i:i+2], 16))[2:].zfill(8))
    for c in check_list:
        x = c[:-1].count('1')
        if x % 2 == 0:
            key += c[:-1] + '1'
        else:
            key += c[:-1] + '0'
    return libnum.b2s(key)

k_1 = check(k_a)
k_2 = check(k_b)  
key = k_1 + k_2
print("key = %s" %(key.encode('hex')))
cip = '9MgYwmuPrjiecPMx61O6zIuy3MtIXQQ0E59T3xB6u0Gyf1gYs2i3K9Jxaa0zj4gTMazJuApwd6+jdyeI5iGHvhQyDHGVlAuYTgJrbFDrfB22Fpil2NfNnWFBTXyf7SDI'
cip = base64.b64decode(cip)
iv = '\x00' * 16
cry = AES.new(key, AES.MODE_CBC, iv)
plain = cry.decrypt(cip)
print(plain)
```

![image-20211022150439619](https://i.loli.net/2021/10/22/rOJYAE6KZCy8kn7.png)

