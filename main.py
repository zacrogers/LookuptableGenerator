import lut_generator as gen
import numpy as np
import matplotlib.pyplot as plt

num_samples = 255

square = gen.generateSquare(num_samples, 10, True)
sine   = gen.generateSine(num_samples, True)
time   = np.linspace(0, num_samples, num=num_samples)
x      = gen.mapVals(square, 0, 255)

c = gen.loadCsv("sine")

for i in c:
    print(i)
# gen.saveCsv("sine", sine)

# gen.generateTable("sine", x, True)
# plt.plot(time, x)
# plt.show()