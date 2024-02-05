import pyglet
import random

class Renderer(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.batch = pyglet.graphics.Batch()
        self.x = list(range(1, 101))
        random.shuffle(self.x)
        self.bars = self.create_bars()

    def create_bars(self):
        bars = []
        for e, i in enumerate(self.x):
            bars.append(pyglet.shapes.Rectangle(100 + e * 10, 100, 8, i * 5, batch=self.batch))
        return bars

    def draw(self):
        self.clear()
        self.batch.draw()

def merge_sort_animation(window, bars):
    if len(bars) <= 1:
        return bars

    mid = len(bars) // 2
    left_half = bars[:mid]
    right_half = bars[mid:]

    left_half = merge_sort_animation(window, left_half)
    right_half = merge_sort_animation(window, right_half)

    return merge_animation(window, left_half, right_half)

def merge_animation(window, left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i].height < right[j].height:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    for e, bar in enumerate(result):
        bar.x = 100 + e * 10

    pyglet.clock.tick()
    window.draw()
    pyglet.app.platform_event_loop.step(pyglet.clock.get_sleep_time(0.5))

    return result

if __name__ == "__main__":
    window = Renderer(1200, 600, "Merge Sort Animation")
    unsorted_bars = window.bars.copy()

    @window.event
    def on_draw():
        window.draw()

    pyglet.clock.schedule_interval(lambda dt: merge_sort_animation(window, unsorted_bars), 5)

    pyglet.app.run()
