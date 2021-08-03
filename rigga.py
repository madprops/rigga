# pip3 install pillow

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from typing import List
from typing import Tuple
from typing import Match
from typing import Iterator
from nouns_list import nouns
from verbs_list import verbs
import colorsys
import datetime
import random
import sys
import os
import re

# Globals
font_names: Iterator[str]

def random_string() -> str:
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

def now() -> float:
  return datetime.datetime.timestamp(datetime.datetime.now())

def string_escape(s: str, encoding: str = "utf-8") -> str:
  return (s.encode("latin1")         # To bytes, required by unicode-escape
          .decode("unicode-escape") # Perform the actual octal-escaping decode
          .encode("latin1")         # 1:1 mapping back to bytes
          .decode(encoding))

def hex_to_rgb(hex: str) -> Tuple[int, ...]:
    hex = hex.lstrip("#")
    hlen = len(hex)
    return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

def get_font(text: str, img: Image.Image, font_name: str) -> ImageFont.FreeTypeFont:
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

def replace_random_word(_: Match[str]) -> str:
  n = random.randint(0, 9)
  if n == 0:
    word = str(random.randint(0, 1000))
  elif n == 1:
    word = random_string()
  elif n % 2 == 0:
    word = random.choice(nouns)
  else:
    word = random.choice(verbs)
  return word.title()

def replace_random(text: str) -> str:
  return re.sub("{random}", replace_random_word, text, flags=re.IGNORECASE)

def get_shadowcolor(color: str) -> str:
  r, g, b = hex_to_rgb(color)
  _, l, _ = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
  return "#212121" if l >= 0.5 else "#e3e3e3"

def draw_text(img: Image.Image, text: str, color: str, mode: str, font_name: str) -> None:
    font = get_font(text, img, "fonts/{0}".format(font_name))
    draw = ImageDraw.Draw(img)
    font_size = draw.textsize(text, font)

    x = (img.width - font_size[0]) / 2
    if mode == "top":
      y = img.height * 0.025
    elif mode == "middle":
      y = (img.height - font_size[1]) / 2
    elif mode == "bottom":
      y = img.height - font_size[1] - (img.height * 0.025)
    else: y = 0

    # Thin border
    shadowcolor = get_shadowcolor(color)

    draw.text((x - 1, y), text, font=font, fill=shadowcolor, align="center")
    draw.text((x + 1, y), text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y - 1), text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y + 1), text, font=font, fill=shadowcolor, align="center")
    draw.text((x, y), text, font=font, fill=color, align="center")

def make_image(img: Image.Image, top_text: str, middle_text: str, \
  bottom_text: str, color_1: str, color_2: str, color_3: str, ext: str) -> str:
  top_text = replace_random(top_text)
  middle_text = replace_random(middle_text)
  bottom_text = replace_random(bottom_text)
  font_name = next(font_names)

  # Top
  if top_text != "{empty}":
    draw_text(img, top_text, color_1, "top", font_name)

  # Middle
  if middle_text != "{empty}":
    draw_text(img, middle_text, color_2, "middle", font_name)

  # Bottom
  if bottom_text != "{empty}":
    draw_text(img, bottom_text, color_3, "bottom", font_name)

  # Save
  result_path = "results/{0}_{1}{2}".format(random_string(), now(), ext)
  img.save(result_path)
  return result_path

def main() -> None:
  # Arguments
  path = sys.argv[1]
  _, ext = os.path.splitext(path)
  top_text = string_escape(sys.argv[2])
  middle_text = string_escape(sys.argv[3])
  bottom_text = string_escape(sys.argv[4])
  color_1 = sys.argv[5]
  color_2 = sys.argv[6]
  color_3 = sys.argv[7]
  num_images = int(sys.argv[8])
  if num_images > 100: quit()
  img = Image.open(path)
  result_paths: List[str] = []

  # Get font names
  global font_names
  file_names = os.listdir("fonts")
  random.shuffle(file_names)
  font_names = iter(file_names)  

  # Make images
  for _ in range(0, num_images):
    res = make_image(img.copy(), top_text, middle_text, bottom_text, color_1, color_2, color_3, ext)
    result_paths.append(res)

  # Result paths
  print(" ".join(result_paths))

main()