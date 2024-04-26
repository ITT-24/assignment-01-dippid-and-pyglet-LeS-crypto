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

initial_z = 0.6
if sensor.has_capability('accelerometer'):
    initial_z = float(sensor.get_value('accelerometer')['y'])
    print("i_z", initial_z)


# ----- GAME ELEMENTS ----- #
PLAYER_WIDTH = 100
PLAYER_MAX_WIDTH = 250
PLAYER_MIN_WIDTH = 50
PLAYER_HEIGHT = 10
PLAYER_Y = 50
player = shapes.Rectangle(150, PLAYER_Y, 
                          PLAYER_WIDTH, PLAYER_HEIGHT, 
                          (144, 183, 255))

score = pyglet.text.Label(text="Score: 0", x=10, y=380)

class Score_Object():
    count = 0

    def __init__(self, color=(0, 255, 0), is_friend = True):
        self.color = color
        self.objects = []
        self.friend = is_friend

    def draw_objects(self):
        for obj in self.objects:
            obj.draw()
    
    def draw(self):
        self.shape.draw()

    def create_object(self, x):
        radius = random.randint(5, 15)
        x = random.randint(0, window.width - radius)
        y = window.height + radius + 5 # drop from outside
        circle = shapes.Circle(x, y, radius, color=self.color)
        self.objects.append(circle)

    def update_objects(self, x):
        for obj in self.objects:
            self.check_bounds(obj)
            self.update_single(obj)

    def update_single(self, obj): # make 'em fall!
       obj.y -= 10

    def check_bounds(self, obj):  # only works for center of circle 
        player_max_x = player.x + player.width
        player_max_y = player.y + PLAYER_HEIGHT

        # only check collision, if circle at/lower player height
        if obj.y <= player_max_y:

            # make 'em disappear if out of y_bottom_bounds
            min_y = 0 - obj.radius
            if obj.y < min_y:
                self.objects.remove(obj)
                # print("rm target")

            # make 'em disappear if collision with player
            if obj.y >= PLAYER_Y: # and  target.y <= player_max_y:
                if obj.x >= player.x and obj.x <= player_max_x:
                    self.objects.remove(obj)
                    
                    # update Score
                    if self.friend:
                        Score_Object.count += 1
                    else: Score_Object.count -= 1
                    score.text=f"Score: {Score_Object.count}"

class Target(Score_Object):
    def __init__(self, color=(0, 255, 0)):
        super().__init__(color)

class Enemy(Score_Object):
    def __init__(self, color=(255, 0, 0)):
        super().__init__(color, is_friend=False)

target = Target()
enemy = Enemy()

# ----- HELPER ----- #

# direction + = left , - = right
def move_in_bounds(player, new_pos):
    """move the player, but only inside the window bounds"""
    if player.x <= 10 and new_pos > 0: # & if keep moveing left
        player.x = 0
        print("at left border w/", player.x)
    elif (player.x + player.width) >= WIDTH and new_pos < 0:
        player.x = WIDTH - player.width
        print("at right border w/", player.x)
    else:
        player.x -= new_pos

# ----- GAME LOOPS ----- # 

@window.event
def on_draw():
    window.clear()

    score.draw()
    player.draw()
    target.draw_objects()
    enemy.draw_objects()

    # Move rect with sensors
    if(sensor.has_capability('accelerometer')):
        acc_x = float(sensor.get_value('accelerometer')['x'])
        acc_z = float(sensor.get_value('accelerometer')['z'])
        # print(acc_x) # NOTE: +acc_x = left, -acc_x = right

        movement = 10*acc_x

        # only move when acc is high enough
        if acc_x >= 0.05 or acc_x <= 0.05: # ??
            move_in_bounds(player, movement)

        # acc_z = tilt back = bigger + slower (bc. acc_x)
        if acc_z >= initial_z and player.width < PLAYER_MAX_WIDTH:
            # tilt back = bigger
            player.width += 2
            player.x -= 1 # "center" player
        elif acc_z <= initial_z and player.width > PLAYER_MIN_WIDTH:
            # tilt forward = smaller
            player.width -= 2
            player.x += 1

# ASK: gradually increase create_target intervall from 1 to 0.01 the longer the game runs
clock.schedule_interval(target.create_object, 1)
clock.schedule_interval(target.update_objects, 0.1)

clock.schedule_interval(enemy.create_object, 2.5)
clock.schedule_interval(enemy.update_objects, 0.1)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.Q:
        window.close()
    # addition keybinds for optional keyboard usage/debug
    elif symbol == pyglet.window.key.LEFT:
        move_in_bounds(player, movement_speed)         
    elif symbol == pyglet.window.key.RIGHT:
        move_in_bounds(player, -movement_speed)

    elif symbol == pyglet.window.key.UP:
        player.width += 2
        player.x -= 1
    elif symbol == pyglet.window.key.DOWN:
        player.width -= 2
        player.x += 1

# ----- RUN GAME ----- #

if __name__ == '__main__':
    pyglet.app.run()


"""
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

"""