'''
  Generates lookup tables as c header files
'''


import numpy as np

def generateSine(length, signed):
    filename = "sinewave_{}.h".format(length)
    print("float sineWave[{}] = {{".format(length))
    
    for i in range (length):
        sample = (np.sin(2*np.pi*i/length))
        if signed:
            sample = (sample+1)/2
            
        print("{},".format(sample))
    
    print("};")
    

generateSine(100, False)
