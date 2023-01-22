import struct

aa = [2, 17038]
bb = [37984, 16171]
cc = [36344, 17470]

# 0: [2]
#                         1: [17038]
#                         2: [37984]
#                         3: [16171]
#                         4: [36344]
#                         5: [17470]


def foo(a):
    raw_bytes = struct.pack('>HH', a[1], a[0])
    [res] = struct.unpack('>f', raw_bytes)
    return res
    
humidity = foo(aa) # относительная влажность. округлить в большую сторону.
temp = foo(bb) # температура окружающей среды. округлить в большую сторону
pressure = foo(cc) # атмосферное давление. округлить в большую сторону

print(int(humidity))
print(round(temp, 1))
print(round(pressure, 1))