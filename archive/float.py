import struct

bs=struct.pack('>HH', 49145, 14092)
fl=struct.unpack('>f', bs)
#print(bs)
print(fl[0])