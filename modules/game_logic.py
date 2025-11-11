import os
import random


def load_level(level_name, base_image_dir="game_materials/images", base_melody_dir="game_materials/melodies"):
    image_dir = os.path.join(base_image_dir, level_name)
    melody_dir = os.path.join(base_melody_dir, level_name)

    if not os.path.exists(image_dir) or not os.path.exists(melody_dir):
        raise FileNotFoundError(f"Not found: {level_name}")

    images = sorted([f for f in os.listdir(image_dir) if f.endswith(".png")])
    melodies = sorted([f for f in os.listdir(melody_dir) if f.endswith((".mid"))])

    if len(images) != len(melodies):
        raise ValueError(f"Number of images is not equal to number of melodies in: {level_name}")

    pairs = list(zip(melodies, images))

    return {
        "name": level_name,
        "image_dir": image_dir,
        "melody_dir": melody_dir,
        "pairs": pairs
    }


def new_round(level_data):
    pairs = level_data["pairs"]
    melody_dir = level_data["melody_dir"]
    image_dir = level_data["image_dir"]

    correct_melody, correct_image = random.choice(pairs)
    all_images = [img for _, img in pairs]
    options = [correct_image]
    while len(options) < 4 and len(options) < len(all_images):
        candidate = random.choice(all_images)
        if candidate not in options:
            options.append(candidate)
    random.shuffle(options)

    return {
        "melody": os.path.join(melody_dir, correct_melody),
        "correct_image": os.path.join(image_dir, correct_image),
        "options": [os.path.join(image_dir, img) for img in options]
    }


def check_answer(selected_image_path, correct_image_path):
    selected_name = os.path.basename(selected_image_path)
    correct_name = os.path.basename(correct_image_path)
    return selected_name == correct_name
