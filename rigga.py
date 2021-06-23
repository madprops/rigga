# pip install pillow
# pip install colormap
# pip install easydev

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from colormap import rgb2hex, rgb2hls, hls2rgb
from nouns_list import nouns
from verbs_list import verbs
import datetime
import random
import sys
import os
import re

font_names = []

def randword():
    a = ["a","e","i","o","u"] 
    b = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", 
    "n", "p", "r", "s", "t", "v", "w", "x", "y", "z"]

    word = ""

    for i in range(0, 6):
      if i % 2 == 0:
        word += random.choice(b)
      else :
        word += random.choice(a)
    
    return word

def now():
  return datetime.datetime.timestamp(datetime.datetime.now())

def string_escape(s, encoding='utf-8'):
  return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
          .decode('unicode-escape') # Perform the actual octal-escaping decode
          .encode('latin1')         # 1:1 mapping back to bytes
          .decode(encoding)) 

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3)) 

def get_font(text, img, font_name):
  font_size = int(img.width / 8)
  draw = ImageDraw.Draw(img)

  while True:
    font = ImageFont.truetype(font_name, font_size)
    size = draw.textsize(text, font)
    if (size[0] < img.width * 0.95) and size[1] < img.height * 0.5:
      return font
    else:
      font_size -= 4
      if font_size < 10:
        quit()

def replace_random_word(match):
  if random.choice([1, 2]) == 1:
    word = random.choice(nouns)
  else:
    word = random.choice(verbs)
  word = word.title()
  return word

def check_text(top_text, middle_text, bottom_text):
  if "<random>" in top_text.lower() or "<random>" in middle_text.lower() or "<random>" in bottom_text.lower():
    top_text = re.sub(r'\<random\>', replace_random_word, top_text, flags=re.IGNORECASE)
    middle_text = re.sub(r'\<random\>', replace_random_word, middle_text, flags=re.IGNORECASE)
    bottom_text = re.sub(r'\<random\>', replace_random_word, bottom_text, flags=re.IGNORECASE)
  return (top_text, middle_text, bottom_text)

def get_random_font_name():
  global font_names
  
  if len(font_names) == 0:
    font_names = os.listdir("fonts")
  i = random.randint(0, len(font_names) - 1)
  name = font_names[i]
  del font_names[i]
  return name

def get_shadowcolor(color):
  r, g, b = hex_to_rgb(color)
  h, l, s = rgb2hls(r / 255.0, g / 255.0, b / 255.0)
  if l >= 0.5:
    shadowcolor = "#212121"
  else:
    shadowcolor = "#e3e3e3"
  return shadowcolor

def make_image(img, top_text, middle_text, bottom_text, color_1, color_2, color_3):  
  top_text, middle_text, bottom_text = check_text(top_text, middle_text, bottom_text)

  # TOP
  if top_text != "<empty>":
    font_name = get_random_font_name()
    font = get_font(top_text, img, 'fonts/{0}'.format(font_name))
    draw = ImageDraw.Draw(img)
    font_size = draw.textsize(top_text, font)
    x = (img.width - font_size[0]) / 2
    y = img.height * 0.025

    # thin border
    shadowcolor = get_shadowcolor(color_1)
    draw.text((x-1, y), top_text, font=font, fill=shadowcolor, align="center")
    draw.text((x+1, y), top_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y-1), top_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y+1), top_text, font=font, fill=shadowcolor, align="center")

    draw.text((x, y), top_text, font=font, fill=color_1, align="center")
  
  # Middle
  if middle_text != "<empty>":
    font_name = get_random_font_name()
    font = get_font(middle_text, img, 'fonts/{0}'.format(font_name))
    draw = ImageDraw.Draw(img)
    font_size = draw.textsize(middle_text, font)
    x = (img.width - font_size[0]) / 2
    y = (img.height - font_size[1]) / 2

    # thin border
    shadowcolor = get_shadowcolor(color_2)
    draw.text((x-1, y), middle_text, font=font, fill=shadowcolor, align="center")
    draw.text((x+1, y), middle_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y-1), middle_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y+1), middle_text, font=font, fill=shadowcolor, align="center")

    draw.text((x, y), middle_text, font=font, fill=color_2, align="center")

  # BOTTOM
  if bottom_text != "<empty>":
    font_name = get_random_font_name()
    font = get_font(bottom_text, img, 'fonts/{0}'.format(font_name))
    draw = ImageDraw.Draw(img)
    font_size = draw.textsize(bottom_text, font)
    x = (img.width - font_size[0]) / 2
    y = img.height - font_size[1] - (img.height * 0.025)

    # thin border
    shadowcolor = get_shadowcolor(color_3)
    draw.text((x-1, y), bottom_text, font=font, fill=shadowcolor, align="center")
    draw.text((x+1, y), bottom_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y-1), bottom_text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y+1), bottom_text, font=font, fill=shadowcolor, align="center")

    draw.text((x, y), bottom_text, font=font, fill=color_3, align="center")

  # SAVE
  result_path = "results/{0}_{1}.jpg".format(randword(), now())
  img.save(result_path)
  return result_path

def main():
  # ARGS
  path = sys.argv[1]
  fname, ext = os.path.splitext(path)
  top_text = string_escape(sys.argv[2])
  middle_text = string_escape(sys.argv[3])
  bottom_text = string_escape(sys.argv[4])
  color_1 = sys.argv[5]
  color_2 = sys.argv[6]
  color_3 = sys.argv[7]
  num_images = int(sys.argv[8])
  if num_images > 100:
    quit()
  img = Image.open(path)
  result_paths = []

  for image in range(0, num_images):
    res = make_image(img.copy(), top_text, middle_text, bottom_text, color_1, color_2, color_3)
    result_paths.append(res)

  print(" ".join(result_paths))

main()