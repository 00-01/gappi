import numpy as np
import cv2


filename = "IR_MVPC10_0004_20211213-13_43_46.bin"

raw = np.fromfile(filename, dtype=np.uint16).astype(np.uint8)

raw_to_shape = np.reshape(raw[:6400], (80, 80))

cv2.imwrite("0.png", raw_to_shape)

cv2.waitKey()
