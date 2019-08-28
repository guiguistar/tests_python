import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

path="standard_test_images/"
filename="lena_gray_256.tif"
filepath = os.path.join(path,filename)

with open(filepath, 'rb') as f:
    alldata = np.fromfile(f,dtype=np.uint8)

img = alldata[8:8+256*256].reshape(256,256)

print(img)

#plt.imshow(img,cmap='gray')
#plt.show()

u, s, vh = np.linalg.svd(img, full_matrices=True)

print(u)


S = np.zeros(256)

plt.imshow(img,cmap='gray')

img = np.zeros(256*256,dtype=np.uint8).reshape(256,256)

fig = plt.figure()

def update(n):
    print(n)
    #n = random.randrange(0,256)
    #S[255-n] = s[255-n]
    S[n] = s[n]

    """
    print(n,S.shape)
    print(S)
    print(n,s.shape)
    print(s)
    """
    
    img = np.dot(u*S,vh)
    im = plt.imshow(img,cmap='gray')
    fig.show(im)

#plt.imshow(img,cmap='gray')
#plt.show()


ani = FuncAnimation(fig,update,interval=200)

plt.show()

