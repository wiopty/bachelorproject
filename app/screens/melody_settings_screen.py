from kivy.uix.screenmanager import Screen


class MelodySettingsScreen(Screen):
    selected_octaves = [4,5,6] 
    use_sharps = False
    selected_file = None
    selected_melody_instrument = "Piano" 
    selected_bass_instrument = "Piano" 

    def toggle_sharps(self,instance, value):
        self.use_sharps = value

    def set_octaves(self, octaves_list):
        self.selected_octaves = octaves_list

    def set_melody_instrument(self, instrument_name):
        self.selected_melody_instrument = instrument_name

    def set_bass_instrument(self, instrument_name):
        self.selected_bass_instrument = instrument_name

    def generate_notes(self, use_sharps, octaves):
        base_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

        notes_list = []
        for octave in octaves:
            for note in base_notes:
                notes_list.append(f"{note}{octave}")
                if use_sharps and note in ['C', 'D', 'F', 'G', 'A']:
                    notes_list.append(f"{note}#{octave}")
        
        total_blocks = 360
        block_size = total_blocks / len(notes_list)


        note_map = {}
        start_block = 0
        for i, note in enumerate(notes_list):
            end_block = round(start_block + block_size) -1
            note_map[f"{start_block}-{end_block}"] = note
            start_block = end_block + 1

        last_key = list(note_map.keys())[-1]
        last_start, last_end = map(int, last_key.split('-'))
        if last_end < 359:
            note_map[last_key] = note_map[last_key]
            note_map[f"{last_start}-{359}"] = note_map.pop(last_key)
        
        return note_map
                
    def start_processing(self):
        notes_range = self.generate_notes(self.use_sharps, self.selected_octaves)

        # print("Generated notes range:")
        # for k, v in notes_range.items():
        #     print(f"{k}: {v}")

        loading_screen = self.manager.get_screen("loadingscreen")
        loading_screen.notes_range = notes_range
        loading_screen.selected_file = self.selected_file
        loading_screen.selected_melody_instrument = self.selected_melody_instrument
        loading_screen.selected_bass_instrument = self.selected_bass_instrument
        self.manager.current = "loadingscreen"
        loading_screen.start_processing()
    


