'''
  Generates lookup tables as c header files
'''
import numpy as np
import matplotlib.pyplot as plot

'''
    Generate c header with lookup table from array of waveform
'''
def generateTable(name, waveform, signed):
    length = len(waveform)
    is_signed = ("unsigned", "signed")[signed]
    filename  = "{}{}_{}".format(name, length, is_signed)

    with open(f"{filename}.h", "w") as file:
        file.write(f"#ifndef {filename.upper()}\n")
        file.write(f"#define {filename.upper()}\n\n")
        file.write("static const float {}[{}] = \n{{\n\t\t\t".format(filename, length))
    
        i = 0
        for sample in waveform:
            if signed:
                sample = (sample+1)/2

            if i != length-1:
                file.write("{0:.4f},".format(sample))
            else:
                file.write("{0:.4f}".format(sample))
                
            if i%10 == 0:
                file.write("\n\t\t\t")

            i += 1
    
        file.write("\n};\n")
        file.write("#endif")

    
def generateSine(length, signed):
    sine = []
    for i in range(length):
        sample = (np.sin((2*np.pi*i)/length))

        if signed:
            sample = (sample+1)/2

        sine.append(sample)
    
    return sine

def generateSquare(length, signed):
    square = []
    coeffs = [1, 3, 5, 7, 9, 11]

    for i in range(length):
        sample = 0

        for coeff in coeffs:
            sample += np.sin(2*np.pi*i*coeff/length)/coeff

        square.append(sample)
    
    return square


# def mapVals(x, in_min, in_max, out_min, out_max):
#     return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def getInput():
    length = input("Enter number of samples(default:1024):")
    signed = input("Signed?(y/n):")
    
    if signed == "y":
        signed = True
    else:
        signed = False
        
    return (int(length), signed)
    
    
# length, signed = getInput()
generateTable("square", generateSquare(255, True), True)

time = np.linspace(0,255, num=255)
x = generateSquare(255, True)

plot.plot(time, x)
plot.show()