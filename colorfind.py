from PIL import Image
from collections import Counter
import colorsys
import math

MAX_BLOCKS = 600
TOP_COLORS = 3

# Open an image
im = Image.open('mona_lisa.jpg').convert('RGBA')
width, height = im.size
pixels = im.load()

aspect_ratio = width / height
num_blocks_x = int(math.sqrt(MAX_BLOCKS * aspect_ratio))
num_blocks_y = int(MAX_BLOCKS / num_blocks_x)

# Розміри одного блоку в пікселях
block_width_px = width // num_blocks_x
block_height_px = height // num_blocks_y

print(f"Зображення: {width}x{height}")
print(f"Сітка: {num_blocks_x} x {num_blocks_y} = {num_blocks_x*num_blocks_y} блоків")
print(f"Розмір блоку: {block_width_px}x{block_height_px }")


def rgb_to_hsv(pixel):
    if len(pixel) == 4 and pixel[3] == 0:  # прозорий піксель
        return None
    r, g, b = [x / 255.0 for x in pixel[:3]]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return int(h * 360), int(s * 100), int(v * 100)

for by in range(num_blocks_y):
    for bx in range(num_blocks_x):
        x_start = bx * block_width_px
        y_start = by * block_height_px
        x_end = x_start + block_width_px
        y_end = y_start + block_height_px

        block_pixels = im.crop((x_start, y_start, x_end, y_end)).getdata()
        hsv_pixels = [rgb_to_hsv(p) for p in block_pixels]

        top_colors = Counter(hsv_pixels).most_common(TOP_COLORS)
        print(f"Block ({bx},{by}) top 3 HSV colors: {top_colors}")