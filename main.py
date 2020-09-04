import lut_generator as gen
import numpy as np
import matplotlib.pyplot as plt

num_samples = 4096

square = gen.generateSquare(num_samples, 10, True)
# sine   = gen.generateSine(num_samples, signed=False)
time   = np.linspace(0, num_samples, num=num_samples)
x      = gen.mapVals(square, 0, 255)

sine   = gen.generateSineInt(num_samples, signed=False)
gen.saveVhdlLut("sin", sine, 24, num_samples)

# gen.saveCsv("sine", sine)
# c = gen.loadCsv("sine")
# gen.generateHeader("sine", x, True)

# plt.plot(time, sine)

# new = gen.changeFreq(sine,3)

# new2 = []

# j = 0
# for i in range(len(sine)):
#     if j == len(new):
#         j = 0
#     new2.append(new[j])
#     j+=1

plt.plot(np.linspace(0, len(sine), num=len(sine)), sine)
plt.show()
