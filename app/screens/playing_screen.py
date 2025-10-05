import os
import pygame
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from .visualization_widget import VisualizerWidget

pygame.mixer.init()

class PlayingScreen(Screen):
    midi_file_path = None
    is_paused = False
    duration = 0
    visualizer = None

    def calculate_duration(self, stream_obj):
        total_quarters = stream_obj.quarterLength
        bpm = 120  # можна робити змінним
        seconds = total_quarters * 60 / bpm
        return seconds

    def on_enter(self):
        self.current_time = 0
        Clock.schedule_interval(self.update_progress, 0.5)

        if self.midi_file_path:
            # отримуємо мелодію з resultscreen
            stream_obj = self.manager.get_screen("resultscreen").melody
            if stream_obj:
                self.duration = int(self.calculate_duration(stream_obj))
                self.start_visualizer(stream_obj)
            self.play_melody()

    def on_leave(self):
        Clock.unschedule(self.update_progress)
        pygame.mixer.music.stop()
        self.remove_visualizer()
        self.midi_file_path = None

    def play_melody(self):
        if not self.midi_file_path:
            print("[Playing] No MIDI file to play")
            return

        pygame.mixer.init()
        pygame.mixer.music.load(self.midi_file_path)
        pygame.mixer.music.play()
        self.is_paused = False
        self.ids.play_btn.text = "Pause"
        self.current_time = 0
        self.ids.progress.value = 0

        minutes = self.duration // 60
        seconds = self.duration % 60
        self.ids.time_label.text = f"0:00 / {minutes}:{seconds:02d}"
        self.ids.progress.max = self.duration

    def toggle_play_pause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            if self.visualizer:
                self.visualizer.resume()
            self.is_paused = False
            self.ids.play_btn.text = "Pause"
        else:
            pygame.mixer.music.pause()
            if self.visualizer:
                self.visualizer.pause()
            self.is_paused = True
            self.ids.play_btn.text = "Play"

    def stop_playing(self):
        pygame.mixer.music.stop()
        self.manager.current = "resultscreen"

    def update_progress(self, dt):
        if not self.is_paused and pygame.mixer.music.get_busy():
            self.current_time += dt
            if self.current_time > self.duration:
                self.current_time = self.duration

        self.ids.progress.value = self.current_time

        minutes = int(self.current_time) // 60
        seconds = int(self.current_time) % 60
        total_minutes = self.duration // 60
        total_seconds = self.duration % 60
        self.ids.time_label.text = f"{minutes}:{seconds:02d} / {total_minutes}:{total_seconds:02d}"

    def start_visualizer(self, stream_obj):
        """Створює візуалізатор на основі MIDI нот"""
        notes = []
        for n in stream_obj.flat.notes:
            if n.isNote:
                notes.append((n.pitch.midi, int(n.quarterLength * 500)))
            elif n.isChord:
                notes.append((n[0].pitch.midi, int(n.quarterLength * 500)))

        if notes:
            self.visualizer = VisualizerWidget(notes)
            self.add_widget(self.visualizer)
            self.visualizer.resume

    
    # def start_visualizer(self):
    #     if not self.midi_file_path:
    #         print("[Visualizer] No MIDI file path, skipping visualizer")
    #         return

    #     wav_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    #     self.wav_file_path = wav_tmp.name

    #     def worker():
    #         midi_to_wav(self.midi_file_path, self.wav_file_path)
    #         print(f"[Visualizer] WAV generated at {self.wav_file_path}")
    #         # запускаємо візуалізатор тільки після створення файлу
    #         Clock.schedule_once(add_visualizer, 0)

    #     def add_visualizer(dt):
    #         if not self.visualizer:
    #             self.visualizer = VisualizerWidget(self.wav_file_path)
    #             self.add_widget(self.visualizer)
    #             self.visualizer.resume()
    #         print("[Visualizer] Visualizer started")

    #     Thread(target=worker, daemon=True).start()
