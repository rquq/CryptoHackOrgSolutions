data="0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
data_bytes=bytes.fromhex(data)
cnt=0
for x in data_bytes:
    cnt+=1


res="crypto{"
res_bytes=bytearray()
for i in res:
    res_bytes.append(ord(i))


key="myXORkeymyXORkeymyXORkeymyXORkeymyXORkeymyXORkey"
hex_str=""
for x in key:
    hex_str = "".join([hex(ord(c))[2:] for c in key]) #
hex_str=bytes.fromhex(hex_str)
flag=""
for i in range(len(data_bytes)):
    flag+=chr(hex_str[i]^data_bytes[i])
print(flag)
