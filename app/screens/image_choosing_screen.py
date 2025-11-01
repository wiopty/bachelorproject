from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
import os

class ImageChoosingScreen(Screen):
    selected_file = None
    use_sharps = False

    def on_enter(self):
        self.ids.status.text = "Choose an image"
        self.ids.start_button.disabled = True

    def open_filechooser(self):
        self.ids.status.text = " "
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Choose an image file",
            filetypes=[("Image", "*.png *.jpg *.jpeg *.bmp")]
        )

        root.destroy()
        if file_path:
            self.selected_file = file_path
            self.ids.img.source = self.selected_file
            self.ids.img.color = (1, 1, 1, 1)
            self.ids.status.text = f"File choosed: {os.path.basename(self.selected_file)}"
            self.ids.start_button.disabled = False

        else:
            
            self.selected_file = None
            self.ids.img.source = ""
            self.ids.status.text = "No file selected"
            self.ids.start_button.disabled = True  

    def start_processing(self):
        if not self.selected_file:
            self.ids.status.text = "You should choose an image first"
            return

        melody_settings = self.manager.get_screen("melodysettings")
        melody_settings.selected_file = self.selected_file
        self.manager.current = "melody_settings_screen"
