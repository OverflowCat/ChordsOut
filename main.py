from PIL import Image
im = Image.open('./framesel/frame3.png')
w, h = im.size
print('Original image size: %sx%s' % (w, h))
rgb_im = im.convert('RGB')
y_key = 986
key_pixels = []
for x in range(w):
    key_pixels.append(rgb_im.getpixel((x, y_key)))
print(key_pixels)
# im.show()

# Map each color to the key type it represents
values = [(248,248,248),(0,0,0),(5, 108, 267),(209,129,6)]
# TODO: Auto detect pressed keys' colors
names = ["w", 'b', 'r', "l"]
# 白，黑，蓝（右手），黄（左手）
variance = lambda tup1, tup2: sum([(tup1[index] - tup2[index]) ** 2 for index in range(2)])
def most_similar(one) -> str:
    variances = [variance(one, some) for some in values]
    return names[variances.index(min(variances))] #越小越接近

OCTAVA_WHITE = "C D E F G A B"
OCTAVA_BLACK = "C# D# F# G# A#"
OCTAVA_FULL = "C C# D D# E F F# G G# A A# B"
OCTAVAn_FULL = "Cn Cn# Dn Dn# En Fn Fn# Gn Gn# An An# Bn"
KEYBOARD = "A0 A0# B0 " + " ".join([OCTAVAn_FULL.replace("n", str(index + 1)) for index in range(7)]) + " C8"
print(KEYBOARD)
KEYBOARD = KEYBOARD.split(" ")
print(len(KEYBOARD))
color_names = [most_similar(x) for x in key_pixels]

counter = 1
keys = []
last = "0"
for x in range(w): # Filter those pixels that are not keys
    curr = color_names[x]
    if last == curr:
        counter += 1
    else:
        keys.append([last, x-1-counter, x-1, counter])
        counter = 1
    last = curr
print(keys)

clean_keys = [k for k in keys if k[-1] >= 5]
print(clean_keys)
print(len(clean_keys)) # should be 88 for a standard piano kbd

pressedl = [KEYBOARD[clean_keys.index(k)] for k in clean_keys if k[0] == "l"]
pressedr = [KEYBOARD[clean_keys.index(k)] for k in clean_keys if k[0] == "r"]
print(f"Pressed keys are: Left hand {', '.join(pressedl)}; Right hand {', '.join(pressedr)}") # should be F2, F4

import pylab
import imageio
num = 23333
#视频的绝对路径
filename = './frames/alice.mp4'
#可以选择解码工具
vid = imageio.get_reader(filename,  'ffmpeg')
for im in enumerate(vid):
    #image的类型是mageio.core.util.Image可用下面这一注释行转换为arrary
    #image = skimage.img_as_float(im).astype(np.float32)
    fig = pylab.figure()
    fig.suptitle('image #{}'.format(num), fontsize=20)
    pylab.imshow(im)
pylab.show()