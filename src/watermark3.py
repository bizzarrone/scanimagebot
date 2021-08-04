#Import required Image library
from PIL import Image, ImageDraw, ImageFont

#Create an Image Object from an Image
im = Image.open('Luca-26761246-encoded.png')
width, height = im.size

draw = ImageDraw.Draw(im)
text = "sample watermark"

font = ImageFont.truetype('FreeMono.ttf', 14)
textwidth, textheight = draw.textsize(text, font)

# calculate the x,y coordinates of the text
margin = 0
#x = width - textwidth - margin
x = 34
y = height - textheight - margin

# draw watermark in the bottom right corner
draw.text((x, y), text, font=font)
im.show()

#Save watermarked image
im.save('watermark.png')
