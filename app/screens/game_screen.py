from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from modules import game_logic
class ImageButton(ButtonBehavior, Image):
    pass

class GameScreen(Screen):
    correct_answers = NumericProperty(0)
    total_attempts = NumericProperty(0)
    next_enabled = BooleanProperty(False)
    level_name = StringProperty("level1")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level_data = None
        self.round_data = None
        self.sound = None
        self.sound_checker = None

    def on_pre_enter(self, *args):
        self.reset_game()
        self.start_level("level1")

    def reset_game(self):
        self.correct_answers = 0
        self.total_attempts = 0
        self.level_name = "level1"

        

    def on_enter(self, *args):
        if self.sound_checker:
            self.sound_checker.cancel()
        
        self.sound_checker = Clock.schedule_interval(self.play_sound, 0.1)

    def play_sound(self, dt):
        if (hasattr(self.ids, 'images_layout') and 
            self.ids.images_layout.children and 
            self.sound and 
            not self.sound_ready):
            self.sound.play()
            self.sound_ready = True 
            return False  
        return True

    def load_level(self, level_name):
        
        self.level_name = level_name
        self.level_data = game_logic.load_level(level_name)
        self.sound_ready = False 
        self.new_round()

    def start_level(self, level_name):
        self.correct_answers = 0
        self.total_attempts = 0
        self.level_name = level_name
        self.level_data = game_logic.load_level(level_name)
        self.sound_ready = False 
        self.new_round()

    def new_round(self, *args):
        if self.sound:
            self.sound.stop()

        self.next_enabled = False
        self.sound_ready = False
        self.total_attempts += 1
        self.ids.score_label.text = f"Level: {self.level_name.replace('level', '')} | Score: {self.correct_answers}/{self.total_attempts}"

        self.round_data = game_logic.new_round(self.level_data)
        melody_path = self.round_data["melody"]
        self.sound = SoundLoader.load(melody_path)

        self.ids.images_layout.clear_widgets()
        for img_path in self.round_data["options"]:
            btn = ImageButton(
                source=img_path,
                allow_stretch=True,
                keep_ratio=False
            )
            btn.bind(on_press=lambda instance, p=img_path: self.check_answer(p))
            self.ids.images_layout.add_widget(btn)

        if self.sound_checker:
            self.sound_checker.cancel()
        self.sound_checker = Clock.schedule_interval(self.play_sound, 0.1)

    def check_answer(self, selected_image):
        
        is_correct = game_logic.check_answer(selected_image, self.round_data["correct_image"])
        if is_correct:
            self.correct_answers += 1
        self.ids.score_label.text = f"Level: {self.level_name.replace('level', '')} | Score: {self.correct_answers}/{self.total_attempts}"

        for widget in self.ids.images_layout.children:
            if isinstance(widget, ImageButton):
                widget.disabled = True


        self.next_enabled = True
        self.ids.next_button.disabled = False

    def next_level(self):
        next_level_name = {
            "level1": "level2",
            "level2": "level3",
            "level3": "level1",  
        }.get(self.level_name, "level1")

        self.load_level(next_level_name)

    def back_to_menu(self):
        if self.sound:
            self.sound.stop()

        if self.sound_checker:
            self.sound_checker.cancel()
            self.sound_checker = None
        self.manager.current = "mainmenuscreen"
