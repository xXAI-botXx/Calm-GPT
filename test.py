from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

class GradientBackground(BoxLayout):
    def __init__(self, **kwargs):
        super(GradientBackground, self).__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.color1 = [1, 0, 0, 1]
        self.color2 = [0, 1, 0, 1]
        self.direction = 1

        Clock.schedule_interval(self.update_gradient, 1/60.)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_gradient(self, dt):
        if self.color1[0] >= 1:
            self.direction = -1
        elif self.color1[0] <= 0:
            self.direction = 1

        self.color1[0] += self.direction * dt
        self.color2[1] -= self.direction * dt

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(*self.color2)
            self.rect = Rectangle(pos=self.pos, size=self.size)

class MyApp(App):
    def build(self):
        return GradientBackground()

if __name__ == '__main__':
    MyApp().run()
