import tempfile
import os
import pygame
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from music21 import midi

pygame.mixer.init()

class PlayingScreen(Screen):
    temp_file_path = None
    is_paused = False
    duration = 0

    def calculate_duration(self, stream_obj):
        total_quarters = stream_obj.quarterLength
        bpm = 120 
        seconds = total_quarters * 60 / bpm
        return seconds
    
    def on_enter(self):
        if self.temp_file_path:
            self.play_melody()
        self.current_time = 0
        Clock.schedule_interval(self.update_progress, 0.5)

    def on_leave(self):
        Clock.unschedule(self.update_progress)
        pygame.mixer.music.stop()
        if self.temp_file_path and os.path.exists(self.temp_file_path):
            os.remove(self.temp_file_path)
            self.temp_file_path = None

    def play_melody(self):
        if not self.temp_file_path:
            return

        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_file_path)
        pygame.mixer.music.play()
        self.is_paused = False
        self.ids.play_btn.text = "Pause"
        self.current_time = 0
        self.ids.progress.value = 0
        if self.manager.get_screen("resultscreen").melody:
            stream_obj = self.manager.get_screen("resultscreen").melody
            self.duration = int(self.calculate_duration(stream_obj))
        else:
            self.duration = 0

        minutes = self.duration // 60
        seconds = self.duration % 60
        self.ids.time_label.text = f"0:00 / {minutes}:{seconds:02d}"
        self.ids.progress.max = self.duration

    def toggle_play_pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.ids.play_btn.text = "Pause"
        else:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.ids.play_btn.text = "Play"

    def stop_playing(self):
        pygame.mixer.music.stop()
        self.manager.current = "resultscreen"

    
    def update_progress(self, dt):
        if not self.is_paused and pygame.mixer.music.get_busy():
            self.current_time += dt  # додаємо проміжок часу
            if self.current_time > self.duration:
                self.current_time = self.duration

        self.ids.progress.value = self.current_time

        minutes = int(self.current_time) // 60
        seconds = int(self.current_time) % 60
        total_minutes = self.duration // 60
        total_seconds = self.duration % 60
        self.ids.time_label.text = f"{minutes}:{seconds:02d} / {total_minutes}:{total_seconds:02d}"
