from kivy.uix.screenmanager import Screen
from tkinter import Tk, filedialog
import os

class ImageChoosingScreen(Screen):
    selected_file = None
    use_sharps = False

    def on_enter(self):
        self.ids.status.text = "Choose an image"

    def open_filechooser(self):
        self.ids.status.text = " "
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(
            title="Choose an image file",
            filetypes=[("Image", "*.png *.jpg *.jpeg *.bmp")]
        )

        if file_path:
            self.selected_file = file_path
            self.ids.img.source = self.selected_file
            self.ids.status.text = f"File choosed: {os.path.basename(self.selected_file)}"

    # def toggle_sharps(self,instance, value):
    #     self.use_sharps = value

    def start_processing(self):
        if not self.selected_file:
            self.ids.status.text = "You should choose an image first"
            return

        melody_settings = self.manager.get_screen("melodysettings")
        melody_settings.selected_file = self.selected_file
        # loading_screen.use_sharps = self.use_sharps
        self.manager.current = "melody_settings_screen"
