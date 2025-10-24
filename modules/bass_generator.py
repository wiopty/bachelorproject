note_order = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
seventh_intervals = {
    "major": [0, 4, 7, 10],
    "minor": [0, 3, 7, 10]
}
def create_bass(melody_notes, mode="major"):
    bass_notes = []

    for block_notes, duration in melody_notes:
        if not block_notes:
            continue

        lowest = min(block_notes, key=lambda n: int(''.join(c for c in n if c.isdigit())))
        name = ''.join([c for c in lowest if c.isalpha() or c == '#'])
        octave = int(''.join([c for c in lowest if c.isdigit()]))

        bass_octave = 1 if octave == 2 else 2
        idx = note_order.index(name)
        chord = [note_order[(idx + i) % 12] for i in seventh_intervals[mode]]
        chord = [n+str(bass_octave) for n in chord if n not in [ ''.join(c for c in mn if c.isalpha() or c=='#') for mn in block_notes]]
        bass_notes.append((chord, duration))

        
    return bass_notes


    


