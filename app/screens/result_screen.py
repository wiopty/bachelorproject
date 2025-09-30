from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from modules.melody_create import save_melody
import tempfile
class ResultScreen(Screen):
    melody = None

    def start_processing(self):
        if self.melody:
            # створюємо тимчасовий файл для MIDI
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp_file:
                self.melody.write("midi", fp=tmp_file.name)
                temp_path = tmp_file.name

            # передаємо шлях у PlayingScreen
            playing_screen = self.manager.get_screen("playingscreen")
            playing_screen.temp_file_path = temp_path
        else:
            playing_screen = self.manager.get_screen("playingscreen")
            playing_screen.temp_file_path = None

        self.manager.current = "playingscreen"

    def save_melody(self):
        if not self.melody:
            return
        
        root = Tk()
        root.withdraw()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mid",
            filetypes=[("MIDI files", "*.mid"), ("MP3 files", "*.mp3")],
            title="Save melody as"
        )

        if file_path:
            saved_path = save_melody(self.melody, filename=file_path)
            print(f"Melody saved to: {saved_path}")

