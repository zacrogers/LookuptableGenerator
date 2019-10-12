'''
  Generates lookup tables as c header files
'''
import numpy as np

def generateSine(length, signed):
    is_signed = ("unsigned", "signed")[signed]
    filename  = "sine{}_{}".format(length, is_signed)
    
    print(filename + ".h")
    print("float {}[{}] = {{".format(filename, length))
    
    for i in range (length):
        sample = (np.sin((2*np.pi*i)/length))
        if signed:
            sample = (sample+1)/2
            
        print("{},".format(sample))
    
    print("};")
    
    
def getInput():
    length = input("Enter number of samples:")
    signed = input("Signed?(y/n):")
    
    if signed == "y":
        signed = True
    else:
        signed = False
        
    return (int(length), signed)
    
    
length, signed = getInput()
generateSine(length, signed)
