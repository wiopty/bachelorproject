from modules.colorfind import get_top_colors
from modules.note_mapping import convert_colors_to_notes
from music21 import *
all_blocks_colors = get_top_colors("assets/mona_lisa.jpg")
notes = convert_colors_to_notes(all_blocks_colors,"config/hue_to_note.json" )
print(notes)
