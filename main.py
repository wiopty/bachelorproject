from app.screens.welcome_screen import WelcomeScreen
from app.screens.main_menu_screen import MainMenuScreen
from app.screens.image_choosing_screen import ImageChoosingScreen
from app.screens.loading_screen import LoadingScreen
from app.screens.result_screen import ResultScreen
from app.screens.playing_screen import PlayingScreen
from app.screens.melody_settings_screen import MelodySettingsScreen
from kivy.app import App
from kivy.lang import Builder


class MyApp(App):
    def build(self):
        return Builder.load_file("my.kv")

        
if __name__ == "__main__":
    MyApp().run()

