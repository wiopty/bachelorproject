note_order = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
seventh_intervals = {
    "major": [0, 4, 7, 10],
    "minor": [0, 3, 7, 10]
}

def calculate_average_saturation(all_block_colors):
    all_saturations = []
    for block in all_block_colors:
        for hsv in block:
            h, s, v = hsv
            if s is not None:
                all_saturations.append(s)
    
    if all_saturations:
        avg_saturation = sum(all_saturations) / len(all_saturations)
        return avg_saturation
    else:
        return 50  

def determine_mode_from_saturation(avg_saturation):

    if avg_saturation > 51:
        mode = "major"
    else:
        mode = "minor"
    return mode

def create_bass(melody_notes, all_block_colors=None, mode=None):
    bass_notes = []


    if all_block_colors is not None:
        avg_saturation = calculate_average_saturation(all_block_colors)
        used_mode = determine_mode_from_saturation(avg_saturation)
    elif mode is not None:
        used_mode = mode
    else:
        used_mode = "major"  


    for block_notes, duration in melody_notes:
        if not block_notes:
            continue

        lowest = min(block_notes, key=lambda n: int(''.join(c for c in n if c.isdigit())))
        name = ''.join([c for c in lowest if c.isalpha() or c == '#'])
        octave = int(''.join([c for c in lowest if c.isdigit()]))

        bass_octave = 1 if octave == 2 else 2
        idx = note_order.index(name)
        chord = [note_order[(idx + i) % 12] for i in seventh_intervals[used_mode]]
        chord = [n+str(bass_octave) for n in chord if n not in [ ''.join(c for c in mn if c.isalpha() or c=='#') for mn in block_notes]]
        bass_notes.append((chord, duration))

    return bass_notes