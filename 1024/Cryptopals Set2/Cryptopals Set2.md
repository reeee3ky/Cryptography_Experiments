# Cryptopals Set2

## Implement PKCS#7 padding

```python
def pkcs7(mess, length):
    padlen = length - len(mess)
    padding = chr(length) * padlen
    mess += padding
    return mess

mess = "YELLOW SUBMARINE"
print(pkcs7(mess, 20)), len(pkcs7(mess, 20))
```

## Implement CBC mode

```python
from Crypto.Cipher import AES

f = open('chall_10.txt', 'r')
cry = ''
while 1:
    a = f.readline().strip()
    if a:
        cry += a
    else:
        break
cry = cry.decode('base64')
cry_list = []
for i in range(0, len(cry), 16):
    cry_list.append(cry[i:i+16])

key = 'YELLOW SUBMARINE'
iv = [0] * 16
plain = ''

def aes_ecb_decrypt(key, ciphertext):
	crypto = AES.new(key, AES.MODE_ECB)
	IV = crypto.decrypt(ciphertext)
	return IV

def aes_cbc_decrypt(iv, IV):
    plaintext = ''
    for i in range(len(iv)):
        plaintext += chr(ord(IV[i]) ^ iv[i])
    return plaintext

for i in range(len(cry_list)):
    # print(iv)
    c = cry_list[i]
    IV = aes_ecb_decrypt(key, c)
    if i != 0:
        del iv[:]
        for j in range(len(cry_list[i-1])):
            iv.append(ord(cry_list[i-1][j]))
        # print(iv)
    plain += aes_cbc_decrypt(iv, IV)

print(plain)
```

![image-20211022145717215](https://i.loli.net/2021/10/22/ai3QBoLVZI7UFEp.png)

## An ECB/CBC detection oracle

```python
import random
from Crypto.Cipher import AES

def genrate_aes_key(length):
    key = ''
    for i in range(length):
        key += chr(random.randint(0, 255))
    return key

def generate_cbc_iv(length):
    iv = []
    for i in range(length):
        iv.append(random.randint(0, 255))
    return iv

def pkcs7(mess, length):
    padlen = (len(mess) // length + 1) * length - len(mess)
    padding = chr(padlen) * padlen
    mess += padding
    return mess

def aes_ecb_encrypt(key, plain):
    # print("len(padplain) = ", len(plain))
    cry = AES.new(key, AES.MODE_ECB)
    ciphertext = cry.encrypt(plain)
    # print(len(ciphertext))
    return ciphertext

def aes_cbc_encrypt(key, plain):
    iv = []
    cipher = ''
    cip_list = []
    for i in range(0, len(plain), 16):
        if i == 0:
            iv = generate_cbc_iv(16)
        else:
            del iv[:]
            for c in cip_list[len(cip_list) - 1]:
                iv.append(ord(c))

        IV = "".join(chr(x ^ ord(y)) for x, y in zip(iv, plain[i:i+16]))
        # print("IV = ", len(IV))
        cip = aes_ecb_encrypt(key, IV)
        # print(len(cip))
        cip_list.append(cip)
        cipher += cip
    return cipher

def random_enc(key, plain):
    flag = random.randint(1, 2)
    print(flag)
    if flag == 1: # 1 cbc
        cipher = aes_cbc_encrypt(key, plain)
    else: # 2 ecb 
        cipher = aes_ecb_encrypt(key, plain)
    return cipher

def detect_enc_mode(ciphertext):
    cipher_list = []
    for i in range(0, len(ciphertext), 16):
        cipher_list.append(ciphertext[i:i+16])
    detect = []
    for c in cipher_list:
        if cipher_list.count(c) > 1:
            detect.append(c)
    # print(detect, len(detect))
    if detect:
        print("ECB!!!")
    else:
        print("CBC!!!")

key = genrate_aes_key(16)
# plaintext = "Lay down and boogie and play that funky music till you die." * 10
plaintext = "I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight; and the glory of the Lord shall be revealed and all flesh shall see it together." * 10
rand_front = genrate_aes_key(random.randint(5, 10))
rand_last = genrate_aes_key(random.randint(5, 10))
plaintext += rand_front + rand_last
padplain = pkcs7(plaintext, 16)
cipher = random_enc(key, padplain)
detect_enc_mode(cipher)
```

## Byte-at-a-time ECB decryption (Simple)

```python
from Crypto.Cipher import AES
import random
import base64

def pkcs7(mess, length):
    padlen = (len(mess) // length + 1) * length - len(mess)
    padding = chr(padlen) * padlen
    mess += padding
    return mess

def aes_ecb_encrypt(key, plain):
    # print("len(padplain) = ", len(plain))
    cry = AES.new(key, AES.MODE_ECB)
    ciphertext = cry.encrypt(plain)
    # print(len(ciphertext))
    return ciphertext

def genrate_aes_key(length):
    key = ''
    for i in range(length):
        key += chr(random.randint(0, 255))
    return key

def brute(key, known_str, cip):
    plain_dic = []
    for i in range(256):
        p = aes_ecb_encrypt(key, known_str + chr(i))
        plain_dic.append(p)
    for i in range(len(plain_dic)):
        if cip == plain_dic[i]:
            return chr(i)    

unknown = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
unknown = base64.b64decode(unknown)
# print(unknown)
blocksize = 16
data_block = []
key = genrate_aes_key(16)

for i in range(0, len(unknown), 16):
    data_block.append(unknown[i:i+16])
# print data_block

res = ''
for data in data_block:
    plaintext = ''
    for i in range(1, 17):
        string = 'a' * (16 - i)
        plain = pkcs7(string + data, 16)
        cip = aes_ecb_encrypt(key, plain)[:16]
        k_str = string + plaintext
        # print "len(k_str) = ", len(k_str)
        if brute(key, k_str, cip):
            plaintext += brute(key, k_str, cip)
        else:
            break
        # print "plaintext = ", plaintext
    res += plaintext
    # print res

print(res)
```

![image-20211022145813979](https://i.loli.net/2021/10/22/ykXj7vbcGLNi24B.png)

## ECB cut-and-paste

```python
import random
from Crypto.Cipher import AES

def genrate_aes_key(length):
    key = ''
    for i in range(length):
        key += chr(random.randint(0, 255))
    return key

def pkcs7(mess, length):
    padlen = (len(mess) // length + 1) * length - len(mess)
    padding = chr(padlen) * padlen
    mess += padding
    return mess

def pkcs7_remove(mess):
    padlen = ord(mess[-1:])
    return mess[:len(mess) - padlen]

def aes_ecb_encrypt(key, plain):
    # print("len(padplain) = ", len(plain))
    cry = AES.new(key, AES.MODE_ECB)
    ciphertext = cry.encrypt(plain)
    # print(len(ciphertext))
    return ciphertext

def aes_ecb_decrypt(key, cip):
    cry = AES.new(key, AES.MODE_ECB)
    plain = cry.decrypt(cip)
    return plain

def profile_for(email):
    email = email.replace('&', '+').replace('=', '+')
    return "email=" + email + "&uid=10&role=user"

# email=ga1axy@126.com&uid=10&role=user
email = "ga1axy@126.com"
plaintext = profile_for(email)
print(plaintext)
plaintext = plaintext[:-4]
padlen = 16 - len(plaintext) % 16
plaintext = 'a' * padlen + plaintext
# print plaintext
key = genrate_aes_key(16)
cip = aes_ecb_encrypt(key, plaintext)
admin = pkcs7('admin', 16)
admin_cip = aes_ecb_encrypt(key, admin)
res_cip = cip + admin_cip
print(pkcs7_remove(aes_ecb_decrypt(key, res_cip))[padlen:])
```

![image-20211022145845910](https://i.loli.net/2021/10/22/hVdeTuO6AswUjKm.png)

## Byte-at-a-time ECB decryption (Harder)

```python
from Crypto.Cipher import AES
import random
import base64

def pkcs7(mess, length):
    padlen = (len(mess) // length + 1) * length - len(mess)
    padding = chr(padlen) * padlen
    mess += padding
    return mess

def aes_ecb_encrypt(key, plain):
    cry = AES.new(key, AES.MODE_ECB)
    ciphertext = cry.encrypt(plain)
    return ciphertext

def genrate_aes_key(length):
    key = ''
    for i in range(length):
        key += chr(random.randint(0, 255))
    return key

random_prefix = genrate_aes_key(random.randint(5, 32))
print ("generate random_prefix length = %d" %(len(random_prefix)))
key = genrate_aes_key(16)
unknown = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
unknown = base64.b64decode(unknown)

# get random_prefix length
# https://braincoke.fr/write-up/cryptopals/cryptopals-ecb-decryption-harder/
cip_list = []
max_same = 0
length = 0
for i in range(16, -1, -1):
    c_list = []
    same = 0
    plain = random_prefix + 'A'*i + unknown
    plain = pkcs7(plain, 16)
    cip = aes_ecb_encrypt(key, plain)
    for j in range(0, len(cip), 16):
        c_list.append(cip[j:j+16])
    for pos in range(len(c_list)):
        if i != 16:
            if c_list[pos] == cip_list[-1][pos]:
                same += 1
    max_same = max(max_same, same)
    cip_list.append(c_list)
    if same < max_same:
        length = i + 1
        break
random_prefix_len = max_same * 16 - length
print ("calculate random_prefix length = %d" %(random_prefix_len))

def brute(key, known_str, cip):
    plain_dic = []
    for i in range(256):
        p = aes_ecb_encrypt(key, known_str + chr(i))
        plain_dic.append(p)
    for i in range(len(plain_dic)):
        if cip == plain_dic[i]:
            return chr(i)
data_block = []
for i in range(0, len(unknown), 16):
    data_block.append(unknown[i:i+16])
# print data_block

res = ''
for data in data_block:
    plaintext = ''
    for i in range(1, 17):
        string = 'a' * (16 - i)
        plain = pkcs7(string + data, 16)
        cip = aes_ecb_encrypt(key, plain)[:16]
        k_str = string + plaintext
        # print "len(k_str) = ", len(k_str)
        if brute(key, k_str, cip):
            plaintext += brute(key, k_str, cip)
        else:
            break
        # print "plaintext = ", plaintext
    res += plaintext
    # print res

print(res)
```

![image-20211022145911597](https://i.loli.net/2021/10/22/N5l2IUMZPW1Oxpo.png)

## PKCS#7 padding validation

```python
str1 = "ICE ICE BABY\x04\x04\x04\x04"
str2 = "ICE ICE BABY\x05\x05\x05\x05"
str3 = "ICE ICE BABY\x01\x02\x03\x04"
str4 = "ICE ICE BABY\x05\x05\x05\x05\x05"

def detect_pkcs7(str):
    padlen = ord(str[-1])
    tot = 0
    for i in str:
        if i == chr(padlen):
            tot += 1
    if tot == padlen:
        print("Padding Write!!!")
    else:
        print("Padding Wrong!!!")

detect_pkcs7(str1)
detect_pkcs7(str2)
detect_pkcs7(str3)
detect_pkcs7(str4)
```

![image-20211022150038269](https://i.loli.net/2021/10/22/xHIFl76jqKoYryO.png)

## CBC bit flipping attacks

 ```python
 from Crypto.Cipher import AES
 import random
 
 def profile_for(str):
     str = str.replace(';', '-').replace('=', '+')
     return "comment1=cooking%20MCs;userdata=" + str + ";comment2=%20like%20a%20pound%20of%20bacon"
 
 def pkcs7(mess, length):
     padlen = (len(mess) // length + 1) * length - len(mess)
     padding = chr(padlen) * padlen
     mess += padding
     return mess
 
 def pkcs7_remove(mess):
     padlen = ord(mess[-1:])
     return mess[:len(mess) - padlen]
 
 def aes_ecb_decrypt(key, ciphertext):
 	crypto = AES.new(key, AES.MODE_ECB)
 	IV = crypto.decrypt(ciphertext)
 	return IV
 
 def aes_ecb_encrypt(key, plain):
     cry = AES.new(key, AES.MODE_ECB)
     ciphertext = cry.encrypt(plain)
     return ciphertext
 
 def aes_cbc_decrypt(iv, IV):
     plaintext = ''
     for i in range(len(iv)):
         plaintext += chr(ord(IV[i]) ^ iv[i])
     return plaintext
 
 def aes_cbc_encrypt(key, plain):
     iv = []
     iv_0 = []
     cipher = ''
     cip_list = []
     for i in range(0, len(plain), 16):
         if i == 0:
             iv = generate_cbc_iv(16)
             iv_0 = iv
         else:
             del iv[:]
             for c in cip_list[len(cip_list) - 1]:
                 iv.append(ord(c))
 
         IV = "".join(chr(x ^ ord(y)) for x, y in zip(iv, plain[i:i+16]))
         # print("IV = ", len(IV))
         cip = aes_ecb_encrypt(key, IV)
         # print(len(cip))
         cip_list.append(cip)
         cipher += cip
     return cipher, iv_0
 
 def genrate_aes_key(length):
     key = ''
     for i in range(length):
         key += chr(random.randint(0, 255))
     return key
 
 def generate_cbc_iv(length):
     iv = []
     for i in range(length):
         iv.append(random.randint(0, 255))
     return iv
 
 key = genrate_aes_key(16)
 userdata = ';admin=true'
 print(profile_for(userdata))
 plain = pkcs7(profile_for(userdata), 16) # -admin+true
 cip, iv = aes_cbc_encrypt(key, plain)
 cip_list = []
 for i in cip:
     cip_list.append(ord(i))
 cip_list[plain.find('-') - 16] = cip_list[plain.find('-') - 16] ^ ord('-') ^ ord(';')
 cip_list[plain.find('+') - 16] = cip_list[plain.find('+') - 16] ^ ord('+') ^ ord('=')
 cip = "".join(chr(x) for x in cip_list)
 admin_cip_list = []
 for i in range(0, len(cip), 16):
     admin_cip_list.append(cip[i:i+16])
 plain = ''
 for i in range(len(admin_cip_list)):
     # print(iv)
     c = admin_cip_list[i]
     IV = aes_ecb_decrypt(key, c)
     if i != 0:
         del iv[:]
         for j in range(len(admin_cip_list[i-1])):
             iv.append(ord(admin_cip_list[i-1][j]))
         # print(iv)
     plain += aes_cbc_decrypt(iv, IV)
 print(pkcs7_remove(plain))
 ```

![image-20211022150108323](https://i.loli.net/2021/10/22/zhQXWxPMr5Bg4CE.png)

