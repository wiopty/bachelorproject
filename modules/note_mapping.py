# import json

#check
# def load_hue_map(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)
    
def get_note_from_hue(h, hue_map):
    for hue_range, note in hue_map.items():
        start, end = map(int, hue_range.split("-"))
        if start <= h <= end:
            return note

def get_note_length_from_v(block_colors):
    velocity = [v for (_,_,v) in block_colors if _ is not None]
    avg_v = round(sum(velocity)/len(velocity))

    if avg_v <= 10:
        return 6.0
    elif avg_v <= 20:
        return 4.0
    elif avg_v <= 35:
        return 2.0
    elif avg_v <= 50:
        return 1.5
    elif avg_v <= 70:
        return 1.0
    elif avg_v <= 85:
        return 0.5
    else: 
        return 0.25

def convert_colors_to_notes(all_block_colors, note_range):
    notes = []
    for block in all_block_colors:
        block_notes = []
        note_length = get_note_length_from_v(block)
        for hsv in block:
            h,s,v = hsv
            note = get_note_from_hue(h, note_range)
            if note:
                block_notes.append(note)
        notes.append((block_notes, note_length))
        
        
    return notes
