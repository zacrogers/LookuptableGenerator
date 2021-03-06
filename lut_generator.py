"""
  Generates lookup tables of waveforms as c header files or save as csv files
"""
import numpy as np
import matplotlib.pyplot as plot
import os
import pandas as pd


def generateHeader(name, waveform, signed):
    """ 
        Generate c header with lookup table from array of waveform\n\n

        header filename = {name}{waveform length}_{signed}.h

        Args:\n
            \tname     (string)  : Number of samples to generate
            \twaveform (list)    : Waveform to generate lookup table of
            \tsigned   (boolean) : Set sample values as signed or unsigned

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

def saveVhdlLut(name, vals, n_bits, n_samples):
    """ 
        Save waveform to vhdl file 

        Args:\n
            \t name      (string) : Name of lut to save
            \t vals      (list)   : list to save as vhdl file
            \t n_bits    (int)    : bit depth
            \t n_samples (list)   : list to save as vhdl file
    """
    df  = pd.DataFrame(vals)
    filename = f'{name}_lut.vhd'

    row = 0
    max_rows = 8
    curr_samp = 0

    with open(filename, "w") as file:

        # Write vhdl entity declaration stuff
        file.write("library ieee;\n")
        file.write("use ieee.std_logic_1164.all;\n")
        file.write("use ieee.std_logic_unsigned.all;\n\n")

        file.write(f"entity {name}_lut is\n\n")

        file.write("port (\n")
        file.write("\tclk      : in  std_logic;\n")
        file.write("\ten       : in  std_logic;\n")
        file.write(f"\taddr     : in  std_logic_vector({n_bits-1} downto 0);\n")
        file.write(f"\t{name}_out  : out std_logic_vector({n_bits-1} downto 0)\n")
        file.write(");\n\n")
        file.write("end entity;\n\n\n")

        file.write(f"architecture rtl of {name}_lut is\n\n")
        file.write(f"type rom_type is array (0 to {n_samples}) of std_logic_vector ({n_bits-1}  downto 0);\n\n")
        file.write(f"constant {name}_ROM : rom_type :=\n(\n")

        for sample in vals:
            if(sample >= 0):
                file.write(f"X\"{sample:06x}\"")
            else:
                file.write(f"X\"{((1 << n_bits) + sample):06x}\"")

            # Put a comma after every value other than the last
            if(curr_samp != n_samples-1):
                file.write(",")

            curr_samp += 1
            row += 1

            # Start new line
            if(row == max_rows-1):
                file.write("\n")
                row = 0

        file.write(");\n\n")

        # Write vhdl architecture stuff
        file.write("begin\n\n")

        file.write("rom_select: process (clk)\n")
        file.write("begin\n")
        file.write("\tif clk'event and clk = '1' then\n")
        file.write("\t\tif en = '1' then\n")
        file.write(f"\t\t\t{name}_out <= {name}_ROM(conv_integer(addr));\n")
        file.write("\t\tend if;\n")
        file.write("\tend if;\n")
        file.write("end process rom_select;\n")

        file.write("end rtl;")



def saveCsv(name, vals):
    """ 
        Save list to csv file 

        Args:\n
            \tname (string) : Name of csv to save
            \tvals (list)   : list to save as csv file
    """
    df  = pd.DataFrame(vals)
    fname = f'{name}.csv'
    df.to_csv(fname, index=False)


def loadCsv(fname):
    """ 
        Load single column csv file and return as list 

        Args:\n
            \tfname (string) : Name of csv to load
        Returns:\n
            \t      (list)   : Return list of values in csv
    """
    data = pd.read_csv(f"{fname}.csv")
    return data["0"].tolist()


def generateSine(length=256, signed=True):
    """ 
        Generate one period of sine wave 
    
        Args:\n
            \tlength (int)     : Number of samples to generate.
            \tsigned (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tsine   (list)    : List of samples representing one period of sine wave
    """
    sine = []
    for i in range(length):
        sample = (np.sin((2*np.pi*i)/length))

        if signed:
            sample = (sample+1)/2

        sine.append(sample)
    
    return sine

def generateSineInt(length=256, signed=True, n_bits = 24):
    """ 
        Generate one period of sine wave 
    
        Args:\n
            \tlength (int)     : Number of samples to generate.
            \tsigned (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tsine   (list)    : List of samples representing one period of sine wave
    """
    sine = []
    for i in range(length):
        sample = (np.sin((2*np.pi*i)/length)) * ((2**n_bits) / 2)

        if signed:
            sample = (sample+(2**n_bits))/2

        sine.append(int(sample))
    
    return sine

def generateSquare(length=256, harmonics=10, signed=True):
    """ 
        Generate one period of square wave as list to given number of harmonics 

        Args:\n
            \tlength    (int)     : Number of samples to generate.
            \tharmonics (int)     : Number of harmonics to generate.
            \tsigned    (boolean) : Set sample values as signed or unsigned

        Returns:\n
            \tsquare    (list)    : List of samples representing one period of square wave
    """
    square = []
    for i in range(length):
        sample = 0

        for h in range(harmonics):
            if(h%2):
                sample += np.sin(2*np.pi*i*h/length)/h

        square.append(sample)
    
    return square

def changeFreq(wave, scaling_factor=2):
    new_wave = []
    i = 0
    for sample in wave:
        if i%scaling_factor == 1:
            new_wave.append(sample) 
        i+=1

    return new_wave

def mapVals(x, out_min, out_max):
    """ 
        Re-map range of values in list to new range\n
        Args:\n
            \tx   (list) : List to apply mapping to
            \tmin (int)  : New minumum value
            \tmax (int)  : New maximum value

        Returns:\n
            \t    (list) : Returns list mapped to new range
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
    

def upsample():
    pass

def downsample():
    pass
