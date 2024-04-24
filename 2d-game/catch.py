from DIPPID import SensorUDP
import pyglet
from pyglet import shapes, clock
import random

PORT = 5700
sensor = SensorUDP(PORT)

WIDTH = 400
HEIGHT = 400
window = pyglet.window.Window(WIDTH, HEIGHT)
# batch = pyglet.graphics.Batch()

movement_speed = 10

# ----- GAME ELEMENTS ----- #
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 10
PLAYER_Y = 50
player = shapes.Rectangle(150, PLAYER_Y, 
                          PLAYER_WIDTH, PLAYER_HEIGHT, 
                          (255, 0, 0))

score = pyglet.text.Label(text="Score: 0", x=10, y=380)

class Target():
    targets = []
    count = 0

    def draw_targets():
        for target in Target.targets:
            target.draw()
    
    def draw(self):
        self.shape.draw()

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
       # make 'em fall!
       target.y -= 10
        # TODO: speed up when time progresses

    def check_bounds(target):
        # collision works, but a little laggy
        # only works for center of circle => TODO
        
        player_max_x = player.x + PLAYER_WIDTH
        player_max_y = player.y + PLAYER_HEIGHT

        # only check collision, if circle at bottom of screen
        if target.y <= player_max_y:
            # make 'em disappear if out of y_bottom_bounds
            min_y = 0 - target.radius
            if target.y < min_y:
                Target.targets.remove(target)
                # print("rm target")

             # make 'em disappear if collision with player
            if target.y >= PLAYER_Y: # and  target.y <= player_max_y:
                if target.x >= player.x and target.x <= player_max_x:
                    Target.targets.remove(target)
                    
                    # update Score
                    Target.count += 1
                    score.text=f"Score: {Target.count}"
        
        # NOTE: check rotation of implemented

    def check_bounds_old(target):
        # make 'em disappear if out of y_bottom_bounds
        min_y = 0 - target.radius
        if target.y < min_y:
            Target.targets.remove(target)
        
        # get bounds of player
        player_max_y = player.y + PLAYER_HEIGHT
        player_max_x = player.x + PLAYER_WIDTH
        
        # make 'em disappear if collision with player
        if target.y >= PLAYER_Y and target.y <= player_max_y:
            if target.x >= player.x and target.x <= player_max_x:
                Target.targets.remove(target)
                print("collision")
        # collision works, but a little laggy
        # only works for center of circle => TODO

# direction + = left , - = right
def move_in_bounds(player, new_pos):
    """move the player, but only inside the window bounds"""
    if player.x <= 10 and new_pos < 0: # & keep moveing left
        player.x = 0
        print("at left border w/", player.x)
    elif (player.x + PLAYER_WIDTH) >= WIDTH and new_pos > 0:
        player.x = WIDTH - PLAYER_WIDTH
        print("at right border w/", player.x)
    else:
        player.x += new_pos

# ----- GAME LOOPS ----- # 
@window.event
def on_draw():
    window.clear()

    score.draw()
    player.draw()
    Target.draw_targets()

    # Move rect with sensors
    if(sensor.has_capability('accelerometer')):
        acc_x = float(sensor.get_value('accelerometer')['x'])
        print(acc_x) # NOTE: +acc_x = left, -acc_x = right

        movement = 10*acc_x

        # only move when acc is hight enough
        if acc_x >= 0.05 or acc_x <= 0.05:
            move_in_bounds(player, movement)



clock.schedule_interval(Target.create_target, 1)
# TODO: gradually increase create_target intervall from 1 to 0.01 the longer the game runs
clock.schedule_interval(Target.update_targets, 0.1)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        window.close()
    # addition keybinds for optional keyboard usage/debug
    elif symbol == pyglet.window.key.LEFT:
        move_in_bounds(player, -movement_speed)         
    elif symbol == pyglet.window.key.RIGHT:
        move_in_bounds(player, movement_speed)

    # TODO:
    elif symbol == pyglet.window.key.UP:
        player.rotation += 20
    elif symbol == pyglet.window.key.DOWN:
        player.rotation -= 20

# ----- RUN GAME ----- #

if __name__ == '__main__':
    pyglet.app.run()