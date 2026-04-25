label = "label"
mask='13'
mask= bin(int(mask,10))[2:]
li_binary_string=[]


for x in range(0,5):
    binary_string = bin(ord(label[x]))[2:]
    li_binary_string.append(binary_string)
flag=""


for x in li_binary_string:
    tmp=int(x,2)^int(mask,2)
    flag+=chr(tmp)
print(flag)