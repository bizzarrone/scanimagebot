# import all the libraries
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
import numpy as np
  
# image opening
image = Image.open("Luca-26761246-encoded.png")
# this open the photo viewer
image.show()  
#plt.imshow(image)
  
# text Watermark
watermark_image = image.copy()
  
draw = ImageDraw.Draw(watermark_image)
# ("font type",font size)
font = ImageFont.truetype("FreeMono.ttf", 5)
  
# add Watermark
draw.text((0, 0), "Filename", (0, 0, 0), font=font)
#plt.subplot(1, 2, 1)
#plt.title("black text")
#plt.imshow(watermark_image)
