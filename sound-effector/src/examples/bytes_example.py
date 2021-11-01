
frame = b'\xff\xff\xff\xffXabccc'

print(frame)
print(len(frame))
print(list(frame))
print(list(frame[0:2]))
print(int.from_bytes(frame[0:2], byteorder='little'))
values= []
for i in range(len(frame)//2):
    values.append(int.from_bytes(frame[(i*2):(i*2+2)],byteorder='little'))
print(values)
