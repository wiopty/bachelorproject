from kivy.uix.screenmanager import Screen

class GameResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.correct_answers = 0
        self.total_attempts = 0

    def set_results(self, correct, total):
        self.correct_answers = correct
        self.total_attempts = total
        self.update_display()

    def update_display(self):
        percentage = (self.correct_answers / self.total_attempts * 100) if self.total_attempts > 0 else 0
        
        self.ids.congratulations_label.text = "Congratulations!"
        self.ids.score_label.text = f"Your Score: {self.correct_answers}/{self.total_attempts}"
        self.ids.percentage_label.text = f"Accuracy: {percentage:.1f}%"
        
        if percentage >= 67:
            self.ids.rating_label.text = "Excellent! "
        elif percentage >= 34:
            self.ids.rating_label.text = "Good job! "
        else:
            self.ids.rating_label.text = "Keep trying! "

    def play_again(self):
        game_screen = self.manager.get_screen("gamescreen")
        game_screen.reset_game()
        self.manager.current = "gamescreen"
    
    def back_to_menu(self):
        self.manager.current = "mainmenuscreen"