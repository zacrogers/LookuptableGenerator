import lut_generator as gen
import numpy as np
import matplotlib.pyplot as plot

num_samples = 127

square = gen.generateSquare(num_samples, 15, True)
sine   = gen.generateSine(num_samples, True)

# gen.generateTable("square", square, True)

time = np.linspace(0, num_samples, num=num_samples)

x = gen.mapVals(sine, 0, 255)

plot.plot(time, x)
plot.show()