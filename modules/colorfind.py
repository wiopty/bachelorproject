from PIL import Image
from collections import Counter
import colorsys
import math

MAX_BLOCKS = 600
TOP_COLORS = 3

def get_top_colors(image_path):
    im = Image.open(image_path).convert('RGBA')
    width, height = im.size


    aspect_ratio = width / height
    num_blocks_x = int(math.sqrt(MAX_BLOCKS * aspect_ratio))
    num_blocks_y = int(MAX_BLOCKS / num_blocks_x)

    block_width_px = width // num_blocks_x
    block_height_px = height // num_blocks_y


    def rgb_to_hsv(pixel):
        if len(pixel) == 4 and pixel[3] == 0:
            return None
        r, g, b = [x / 255.0 for x in pixel[:3]]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return int(h * 360), int(s * 100), int(v * 100)

    all_blocks_colors = []
    for by in range(num_blocks_y):
        for bx in range(num_blocks_x):
            x_start = bx * block_width_px
            y_start = by * block_height_px
            x_end = x_start + block_width_px
            y_end = y_start + block_height_px

            block_pixels = im.crop((x_start, y_start, x_end, y_end)).getdata()
            hsv_pixels = [rgb_to_hsv(p) for p in block_pixels]

            top_colors = [color for color, _ in Counter(hsv_pixels).most_common(TOP_COLORS)]
            all_blocks_colors.append(top_colors)
    return all_blocks_colors
