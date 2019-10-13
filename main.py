import lut_generator as gen
import numpy as np
import matplotlib.pyplot as plt

num_samples = 255

square = gen.generateSquare(num_samples, 10, True)
sine   = gen.generateSine(num_samples, signed=False)
time   = np.linspace(0, num_samples, num=num_samples)
x      = gen.mapVals(square, 0, 255)

# gen.saveCsv("sine", sine)
# c = gen.loadCsv("sine")
# gen.generateTable("sine", x, True)

# plt.plot(time, sine)

new = gen.changeFreq(sine,3)

new2 = []

j = 0
for i in range(len(sine)):
    if j == len(new):
        j = 0
    new2.append(new[j])
    j+=1

plt.plot(np.linspace(0, len(new2), num=len(new2)), new2)
plt.show()