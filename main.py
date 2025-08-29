from modules.colorfind import get_top_colors
from modules.note_mapping import convert_colors_to_notes
from modules.melody_create import create_melody

all_blocks_colors = get_top_colors("assets/colorful_shapes.jpg")
notes = convert_colors_to_notes(all_blocks_colors,"config/hue_to_note.json" )
saved_file, melody_part = create_melody(notes, "melody1.mid")
