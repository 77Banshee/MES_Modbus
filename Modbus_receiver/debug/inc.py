import struct
import time

if __name__ == '__main__':
    #inc 17
    #80317
    #slave 27
    # - 0 0' ~50" -0.235
    # - 0 0' ~50" +0.286
    
    #x_raw: high 49175 low 41844
    #y_raw: high 49340 low 48542


    
    x = [49175, 41844] # 5124 = -8480 
    y = [49340, 48542] # 5125 = -21292
    
    x_b = struct.pack('>HH', x[0], x[1])
    y_b = struct.pack('>HH', y[0], y[1])
    
    [x_res] = struct.unpack('>f', x_b)
    [y_res] = struct.unpack('>f', y_b)
    
    print(x_res * 3600) # - 8480
    print(y_res * 3600) # - 21292