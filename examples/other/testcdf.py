from pankus.intopp.make_motion_exchange_convolution import convolution_cdf
import matplotlib.pyplot as plt
import argparse
import sys

selectivity=float(sys.argv[1])
conv_a=float(sys.argv[2])
conv_b=float(sys.argv[3])
steps=int(sys.argv[4])

try:
    minimum=int(sys.argv[5])
except:
    minimum=0

x=[(t-minimum)/10.0 for t in range(steps*10)]

f=lambda s: convolution_cdf(s,selectivity,conv_a,conv_b)

plt.plot(x,map(f,x))
plt.show()

