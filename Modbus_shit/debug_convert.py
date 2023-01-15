import struct

a = [62607, 63517, 64382, 63149, 62554, 63386, 64570, 63644, 62643, 63276, 62638, 64701, 65389, 65502, 65438, 65380, 65324]

b = 65534

counter = 0

for i in a:
    num_2 = b
    num_1 = i
    raw_bytes = struct.pack('>HH', num_1, num_2)
    res = struct.unpack('>f', raw_bytes)
    print(res)
    counter += 2
    
