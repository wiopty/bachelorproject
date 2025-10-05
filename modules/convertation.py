from collections import defaultdict
from mido import MidiFile
from pydub import AudioSegment
from pydub.generators import Sine

def note_to_freq(note):
    return (2.0 ** ((note - 69) / 12.0)) * 440.0

def midi_to_wav(midi_file_path: str, wav_file_path: str, tempo_bpm: int = 120):
    mid = MidiFile(midi_file_path)
    output = AudioSegment.silent(duration=mid.length * 1000.0)

    def ticks_to_ms(ticks):
       tick_ms = (60000.0 / tempo_bpm) / mid.ticks_per_beat
       return ticks * tick_ms
    
    for track in mid.tracks:
        current_pos = 0.0
        current_notes = [dict() for _ in range(16)]

        for msg in track:
            current_pos += ticks_to_ms(msg.time)

            if msg.type == 'note_on' and msg.velocity > 0:
                current_notes[msg.channel][msg.note] = (current_pos, msg)

            elif msg.type in ('note_off', 'note_on') and msg.note in current_notes[msg.channel]:
               start_pos, start_msg = current_notes[msg.channel].pop(msg.note)
               duration = current_pos - start_pos

               freq = note_to_freq(msg.note)
               signal = Sine(freq).to_audio_segment(duration = duration-50, volume=-20)
               signal = signal.fade_in(30).fade_out(30)

               output = output.overlay(signal, position=int(start_pos))
    output.export(wav_file_path, format="wav")
    return wav_file_path