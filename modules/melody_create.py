from music21 import stream, note, chord, meter, tie, bar, instrument, clef
# from pydub import AudioSegment
import os

def get_instrument(instrument_name):
    instrument_map = {
        'Piano': instrument.Piano(),
        'Organ': instrument.Organ(),
        'Violin': instrument.Violin(),
        'Flute': instrument.Flute(),
        'Accordion': instrument.Accordion(),
        'Guitar': instrument.Guitar(),
        "Bagpipes": instrument.Bagpipes()
    }
    return instrument_map.get(instrument_name, instrument.Piano())

def create_melody(notes, bass_notes, filename="melody.mid", melody_instrument="Piano", bass_instrument="Piano"):
    
    score = stream.Score()
    
    melody_part = stream.Part()
    bass_part = stream.Part()
    
    
    melody_part.append(get_instrument(melody_instrument))
    melody_part.append(clef.TrebleClef())
    bass_part.append(get_instrument(bass_instrument))
    bass_part.append(clef.BassClef())
    
    melody_part.append(meter.TimeSignature('4/4'))
    bass_part.append(meter.TimeSignature('4/4'))

    beats_per_measure = 4.0
    melody_current_beat = 0.0
    bass_current_beat = 0.0

    max_length = max(len(notes), len(bass_notes))
    
    for i in range(max_length):
        if i < len(notes):
            notes_group, duration = notes[i]
            unique_notes = list(dict.fromkeys(notes_group))
            remaining = duration
            first = True
            
            while remaining > 0:
                space_left = beats_per_measure - melody_current_beat
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
                    melody_part.append(n)
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
                    melody_part.append(c)

                remaining -= dur
                melody_current_beat += dur
                first = False

                if melody_current_beat >= beats_per_measure:
                    melody_part.append(bar.Barline('regular'))
                    melody_current_beat = 0.0

        if i < len(bass_notes):
            bass_group, bass_duration = bass_notes[i]
            unique_bass_notes = list(dict.fromkeys(bass_group))
            remaining = bass_duration
            first = True
            
            while remaining > 0:
                space_left = beats_per_measure - bass_current_beat
                dur = min(remaining, space_left)

                if len(unique_bass_notes) == 1:
                    n = note.Note(unique_bass_notes[0])
                    n.quarterLength = dur
                    if bass_duration > dur:
                        if first:
                            n.tie = tie.Tie("start")
                        else:
                            n.tie = tie.Tie("continue")
                    elif not first:
                        n.tie = tie.Tie("stop")
                    bass_part.append(n)
                else:
                    c = chord.Chord(unique_bass_notes)
                    c.quarterLength = dur
                    if bass_duration > dur:
                        if first:
                            c.tie = tie.Tie("start")
                        else:
                            c.tie = tie.Tie("continue")
                    elif not first:
                        c.tie = tie.Tie("stop")
                    bass_part.append(c)

                remaining -= dur
                bass_current_beat += dur
                first = False

                if bass_current_beat >= beats_per_measure:
                    bass_part.append(bar.Barline('regular'))
                    bass_current_beat = 0.0

    score.insert(0, melody_part)
    score.insert(0, bass_part)
    
    return score

def save_melody(s, filename = None):
    if not filename:
        raise ValueError("Filename must be provided")
    
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".mid":
        s.write("midi", fp = filename)
        return filename
    
    if ext ==".xml":
        s.write("xml", fp = filename)
        return filename
    # elif ext == ".mp3":
    #     temp_mid = filename.replace(".mp3", ".mid")
    #     s.write("midi", fp = filename)
    #     audio = AudioSegment.from_file(temp_mid, format="mid")
    #     audio.export(filename, format="mp3")

    #     os.remove(temp_mid)
    #     return filename
    
    else: 
        raise ValueError("Unsupported file format. Use .mid or .mp3")