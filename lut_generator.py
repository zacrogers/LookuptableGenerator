"""
  Generates lookup tables of waveforms as c header files
"""
import numpy as np
import matplotlib.pyplot as plot


def generateTable(name, waveform, signed):
    """ 
        Generate c header with lookup table from array of waveform\n\n

        header filename = {name}{waveform length}_{signed}.h

        Args:\n
            \tname (string)    : Number of samples to generate
            \twaveform (list)  : Waveform to generate lookup table of
            \tsigned (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tcreates c header file containing array of waveform values between 0 and 1   
    """
    length = len(waveform)
    is_signed = ("unsigned", "signed")[signed]
    filename  = "{}{}_{}".format(name, length, is_signed)

    with open(f"{filename}.h", "w") as file:
        file.write(f"#ifndef {filename.upper()}\n")
        file.write(f"#define {filename.upper()}\n\n")
        file.write("static const float {}[{}] = \n{{\n\t\t\t".format(filename, length))
    
        i = 0 # To set linebreaks for array values
        for sample in waveform:
            if signed:
                sample = (sample+1)/2

            if i != length-1:
                file.write("{0:.2f},".format(sample))
            else:
                file.write("{0:.2f}".format(sample))
                
            if i%10 == 0:
                file.write("\n\t\t\t")

            i += 1
    
        file.write("\n};\n")
        file.write("#endif")

    
def generateSine(length, signed):
    """ 
        Generate one period of sine wave 
    
        Args:\n
            \tlength (int)     : Number of samples to generate.
            \tsigned (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tsine (list)    : List of samples representing one period of sine wave
    """
    sine = []
    for i in range(length):
        sample = (np.sin((2*np.pi*i)/length))

        if signed:
            sample = (sample+1)/2

        sine.append(sample)
    
    return sine


def generateSquare(length, harmonics, signed):
    """ 
        Generate one period of square wave as list to given number of harmonics 

        Args:\n
            \tlength (int)     : Number of samples to generate.
            \tharmonics (int)  : Number of harmonics to generate.
            \tsigned (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tsquare (list)    : List of samples representing one period of square wave
    """
    square = []
    for i in range(length):
        sample = 0

        for h in range(harmonics):
            if(h%2):
                sample += np.sin(2*np.pi*i*h/length)/h

        square.append(sample)
    
    return square


def mapVals(x, out_min, out_max):
    """ 
        Re-map range of list to new range\n
        Args:\n
            \tx(list)  : List to apply mapping to
            \tmin(int) : New minumum value
            \tmax(int) : New maximum value

        Returns:\n
            \t(list)       : Returns list mapped to new range
    """
    return (x - min(x)) * (out_max - out_min) / (max(x) - min(x)) + out_min


def getInput():
    """ Get command line input to create c header, returns values as tuple """
    length = input("Enter number of samples(default:1024):")
    w_type = input()
    signed = input("Signed?(y/n):")
    
    if signed == "y":
        signed = True
    else:
        signed = False
        
    return (int(length), signed)
    