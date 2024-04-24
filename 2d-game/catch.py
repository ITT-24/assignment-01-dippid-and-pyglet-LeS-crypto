import pyglet
from pyglet import shapes, clock
import random

WIDTH = 400
HEIGHT = 400
window = pyglet.window.Window(WIDTH, HEIGHT)
# batch = pyglet.graphics.Batch()

# ----- GAME ELEMENTS ----- #
player = shapes.Rectangle(150, 50, 100, 10, (255, 0, 0))

class Target():
    targets = []

    def draw_targets():
        for target in Target.targets:
            target.draw()
    
    def draw(self):
        self.shape.draw()

    # def __init__(self, x, y, radius):
    #     self.x = x
    #     self.y = y
    #     self.radius = radius
    #     self.color = (0, 255, 130)
    #     self.shape = shapes.Circle(x=self.x, y=self.y,
    #                                radius=self.radius, 
    #                                color=self.color)
    #     #...
    # doesn't work with update 

    def create_target(delta_time):
        radius = random.randint(5, 15)
        x = random.randint(0, window.width - radius)
        y = window.height + radius + 5 # drop from outside
        # y = random.randint(0, window.height - radius)
        # Target.targets.append(Target(x, y, radius))
        circle = shapes.Circle(x, y, radius, color=(0, 255, 0))
        Target.targets.append(circle)

    def update_targets(delta_time):
        for target in Target.targets:
            Target.check_bounds(target)
            Target.update_single(target)

    def update_single(target):
       target.y -= 10
        # make 'em fall!

    def check_bounds(target):
        # make 'em disappear if out of y_bottom_bounds
        min_y = 0 - target.radius
        if target.y < min_y:
            Target.targets.remove(target)
        # make 'em disappear if collision with player


# ----- GAME LOOPS ----- # 
@window.event
def on_draw():
    window.clear()

    player.draw()
    Target.draw_targets()



clock.schedule_interval(Target.create_target, 1)
# TODO: increase create_intervall from 1 to 0.01 the longer the game runs
clock.schedule_interval(Target.update_targets, 0.1)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        window.close()

# ----- RUN GAME ----- #

if __name__ == '__main__':
    pyglet.app.run()