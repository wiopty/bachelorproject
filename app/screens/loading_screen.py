from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from threading import Thread

from modules.colorfind import get_top_colors
from modules.note_mapping import convert_colors_to_notes
from modules.melody_create import create_melody

class LoadingScreen(Screen):
    selected_file = None
    progress_value = 0
    progress_target = 0
    melody_part = None

    def start_processing(self):
        self.ids.progress.value = 0
        self.progress_value = 0
        self.progress_target = 0
        self.melody_part = None


        Clock.schedule_interval(self.animate_progress, 0.02)

        Thread(target=self._run_pipeline, daemon=True).start()

    def animate_progress(self, dt):

        if self.progress_value < self.progress_target:
            self.progress_value += 1.7
            self.ids.progress.value = self.progress_value
        return True  

    def _run_pipeline(self):
        
        all_blocks_colors = get_top_colors(self.selected_file)
        Clock.schedule_once(lambda dt: setattr(self, 'progress_target', 33))

        
        notes = convert_colors_to_notes(all_blocks_colors, "config/hue_to_note.json")
        Clock.schedule_once(lambda dt: setattr(self, 'progress_target', 66))

        
        self.melody_part = create_melody(notes)
        Clock.schedule_once(lambda dt: setattr(self, 'progress_target', 100))

        
        Clock.schedule_once(self.switch_to_result_screen, 1.5)
        

    def switch_to_result_screen(self, dt):
        result_screen = self.manager.get_screen("resultscreen")
        result_screen.melody = self.melody_part
        self.manager.current = "resultscreen"
