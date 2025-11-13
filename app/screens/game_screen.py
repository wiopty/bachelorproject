from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.properties import NumericProperty, BooleanProperty, StringProperty
from modules import game_logic
from kivy.graphics import Color, Line
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_border, size=self.update_border)
        
    def on_kv_post(self, base_widget):
        self.draw_default_border()
        
    def draw_default_border(self):
        """Малює стандартну сіру рамку"""
        with self.canvas.after:
            Color(0.5, 0.5, 0.5, 1)  # Сірий колір
            Line(rectangle=(self.x, self.y, self.width, self.height), width=3)
    
    def update_border(self, *args):
        """Оновлює позицію рамки при зміні розміру/позиції"""
        self.canvas.after.clear()
        self.draw_default_border()

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
        self.next_enabled = False

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
            btn.color = (1, 1, 1, 1)
            btn.bind(on_press=lambda instance, p=img_path: self.check_answer(p))
            self.ids.images_layout.add_widget(btn)

        self.ids.next_button.disabled = True
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

                if widget.source == selected_image:
                    self.add_border_to_widget(widget, is_correct)
                elif widget.source == self.round_data["correct_image"] and not is_correct:
                    self.add_border_to_widget(widget, True)
        self.next_enabled = True
        self.ids.next_button.disabled = False

    def add_border_to_widget(self, widget, is_correct):


        with widget.canvas.after:
            if is_correct:
                Color(0, 1, 0, 1)  # Зелений колір для правильної відповіді
            else:
                Color(1, 0, 0, 1)  # Червоний колір для неправильної відповіді
            
            # Створюємо рамку навколо картинки
            Line(rectangle=(widget.x, widget.y, widget.width, widget.height), width=8)

    def next_level(self):
        next_level_name = {
            "level1": "level2",
            "level2": "level3",
            "level3": None,  
        }.get(self.level_name, "level1")

        if next_level_name is None:
            self.show_final_results()
        else:
            self.load_level(next_level_name)

    def show_final_results(self):
        if self.sound:
            self.sound.stop()

        if self.sound_checker:
            self.sound_checker.cancel()
            self.sound_checker = None
            
        results_screen = self.manager.get_screen("gameresultsscreen")
        results_screen.set_results(self.correct_answers, self.total_attempts)
        self.manager.current = "gameresultsscreen"

    def back_to_menu(self):
        if self.sound:
            self.sound.stop()

        if self.sound_checker:
            self.sound_checker.cancel()
            self.sound_checker = None
        self.manager.current = "mainmenuscreen"
