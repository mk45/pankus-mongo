from pankus.intopp.make_motion_exchange import convolution_mix
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import argparse
import sys


steps=int(sys.argv[1])
selectivity=float(sys.argv[2])
conv_a=float(sys.argv[3])
conv_b=float(sys.argv[4])
alpha=float(sys.argv[5])


try:
    filename=str(sys.argv[6])
    image=mpimg.imread(filename)

except:
    # white as background image
    image=[[[1.0,1.0,1.0]]]

x=[(t-0.0)/10.0 for t in range(steps*10)]

f=lambda s: convolution_mix(s,selectivity,conv_a,conv_b,alpha)

plt.plot(x,map(f,x),zorder=1)
plt.imshow(image,zorder=0,extent=[0.0,steps,0.0,1.0],aspect='auto')
plt.show()

