from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
from modules.melody_create import save_melody

class ResultScreen(Screen):
    melody = None

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

