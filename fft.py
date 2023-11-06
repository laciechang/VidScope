import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('/Users/lc/Desktop/Untitled_1.3.1.png', 0)
dft = cv2.dft(np.float32(img), flags = cv2.DFT_COMPLEX_OUTPUT)
dftshift = np.fft.fftshift(dft)
res1= np.log(cv2.magnitude(dftshift[:,:,0], dftshift[:,:,1]))
scopeSize = min(res1.shape[0]*10, res1.shape[1]*10)
res1 = cv2.resize(res1, dsize=(scopeSize, scopeSize))
res1 = res1.astype(np.float32)
value = np.sqrt(((res1.shape[0]/2.0)**2.0)+((res1.shape[1]/2.0)**2.0))
res1 = cv2.linearPolar(res1,(res1.shape[0]/2, res1.shape[1]/2), value, cv2.WARP_FILL_OUTLIERS)
plt.imshow(res1, 'gray')
plt.xscale('symlog')
plt.yscale('symlog')
plt.show()