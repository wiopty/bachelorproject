from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Ellipse
from kivy.clock import Clock
import numpy as np

def lerp(a, b, t):
    return a + (b - a) * t

class VisualizerWidget(Widget):
    def __init__(self, notes, **kwargs):
        super().__init__(**kwargs)
        self.notes = notes
        self.sample_rate = 60
        self.pos_index = 0
        self.max_time = sum(d for _, d in notes) / 1000.0
        self.frame_count = int(self.max_time * self.sample_rate) + 1
        self.amplitudes = self._generate_amplitudes()
        self.current_radius = 100  # початковий радіус
        Clock.schedule_interval(self.update_visual, 1/self.sample_rate)

    def _generate_amplitudes(self):
        amplitudes = np.zeros(self.frame_count)
        current_time = 0
        for midi_number, duration_ms in self.notes:
            frames = int(duration_ms / 1000 * self.sample_rate)
            amp = (midi_number - 21) / (108 - 21)
            if frames > 0:
                amplitudes[current_time:current_time+frames] = amp
                current_time += frames
        return amplitudes

    def update_visual(self, dt):
        if self.pos_index >= len(self.amplitudes):
            self.pos_index = 0

        target_amp = self.amplitudes[self.pos_index]
        self.pos_index += 1

        # плавний перехід радіусу
        min_radius = 100
        max_radius = 300
        target_radius = min_radius + target_amp * (max_radius - min_radius)
        self.current_radius = lerp(self.current_radius, target_radius, 0.1)  # 0.1 = швидкість згладжування

        # гладке коло
        center_x, center_y = self.center_x, self.center_y
        num_points = 60
        angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
        points = []
        for a in angles:
            r = self.current_radius * (0.9 + 0.1*np.sin(a*3 + self.pos_index*0.05))  # хвилі
            x = center_x + r * np.cos(a)
            y = center_y + r * np.sin(a)
            points.extend([x, y])
        points.extend([points[0], points[1]])

        self.canvas.clear()
        with self.canvas:
            Color(1, 0.5, 1, 0.8)
            Line(points=points, width=2, close=True)
            Color(0.2, 0.2, 0.2)
            Ellipse(pos=(center_x-50, center_y-50), size=(100,100))

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
