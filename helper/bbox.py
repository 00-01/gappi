from io import BytesIO

from matplotlib import cm
from matplotlib.patches import Rectangle
from matplotlib.pyplot import subplots
from numpy import asarray
from PIL import Image


ir_file = ""
det_data = [[34.8685, 40.00106, 49.837486, 46.854866], [51.45089, 28.69755, 64.22715, 37.239586]]

img = Image.open(ir_file)
box = det_data.split(",")
box = box[1:]
fig, ax = subplots()
ax.imshow(img, cmap=cm.magma, vmin=args.min, vmax=args.max, )
for i in box:
    i = i.split('x')
    rect = Rectangle((int(i[0]), int(i[1])), int(i[2]), int(i[3]), edgecolor='w', facecolor="none")
    ax.add_patch(rect)
    ax.axis('off')
img_buf = BytesIO()
fig.savefig(img_buf, format='png')
im = Image.open(img_buf)
arr = asarray(im, dtype='uint8')
w1, h1, c1 = arr.shape
w2, h2 = 60, 140
arr = arr[w2:w1-w2, h2:h1-h2, :]
im = Image.fromarray(arr)
im.save(ir_file)