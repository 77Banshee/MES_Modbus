import struct

a = [62378, 62511, 62406, 62305, 62357, 62457, 62707, 62514, 62441, 63165, 63913, 64612, 65082, 65234, 65258, 65252]

#slave 26 TK
counter = 0

for i in a:
    raw_bytes = struct.pack('>H', i)
    [res] = struct.unpack('>h', raw_bytes)
    print(res / 100)
    
