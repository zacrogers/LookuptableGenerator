'''
  Generates lookup tables as c header files
'''
import numpy as np

def generateSine(length, signed):
    is_signed = ("unsigned", "signed")[signed]
    filename  = "sine{}_{}".format(length, is_signed)
    
    # Filename
    print(filename + ".h")
    
    # Text to write to file
    print("#ifndef {}".format(filename.upper()))
    print("#def {}\n".format(filename.upper()))
    print("float {}[{}] = {{".format(filename, length))
    
    for i in range(length):
        sample = (np.sin((2*np.pi*i)/length))
        if signed:
            sample = (sample+1)/2
            
        print("{},".format(sample))
    
    print("};")
    print("#endif")
    
    
def mapVals(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;


def getInput():
    length = input("Enter number of samples(default:1024):")
    signed = input("Signed?(y/n):")
    
    if signed == "y":
        signed = True
    else:
        signed = False
        
    return (int(length), signed)
    
    
length, signed = getInput()
generateSine(length, signed)

