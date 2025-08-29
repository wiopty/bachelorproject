from music21 import stream, note, chord, meter, tie, bar, environment

def create_melody(notes, filename="melody.mid"):
    s = stream.Stream()
    s.append(meter.TimeSignature('4/4'))

    beats_per_measure = 4.0
    current_beat = 0.0

    for notes_group, duration in notes:
        unique_notes = list(dict.fromkeys(notes_group))
        remaining = duration
        first = True
        while remaining > 0:
            space_left = beats_per_measure - current_beat
            dur = min(remaining, space_left)

            if len(unique_notes) == 1:
                n = note.Note(unique_notes[0])
                n.quarterLength = dur
                if duration > dur:
                    if first:
                        n.tie = tie.Tie("start")
                    else:
                        n.tie = tie.Tie("continue")
                elif not first:
                    n.tie = tie.Tie("stop")
                s.append(n)
            else:
                c = chord.Chord(unique_notes)
                c.quarterLength = dur
                if duration > dur:
                    if first:
                        c.tie = tie.Tie("start")
                    else:
                        c.tie = tie.Tie("continue")
                elif not first:
                    c.tie = tie.Tie("stop")
                s.append(c)

            remaining -= dur
            current_beat += dur
            first = False

            if current_beat >= beats_per_measure:
                s.append(bar.Barline('regular'))
                current_beat = 0.0

    if filename.endswith(".mid"):
        s.write("midi", fp=filename)
    else:
        raise ValueError("Not supported")

    return  filename, s


