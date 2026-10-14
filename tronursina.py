from ursina import *
import math

app = Ursina()
window.title = 'Python Tron'
window.color = color.rgb(8, 12, 24)
window.borderless = False
window.exit_button.visible = False
window.fps_counter.enabled = True

CELL = 0.5
BOARD_W = 40
BOARD_H = 28
MOVE_INTERVAL = 0.12
TRAIL_Y = 0.08

# Game states: start, countdown, playing, gameover
state = 'start'
countdown_value = 3
countdown_elapsed = 0.0
move_elapsed = 0.0
winner_text = ''
score_blue = 0
score_red = 0

blue_path = []
red_path = []
blue_grid = set()
red_grid = set()
blue_dir = (1, 0)
red_dir = (-1, 0)
blue_next_dir = (1, 0)
red_next_dir = (-1, 0)
blue_mesh = None
red_mesh = None
blue_trail = None
red_trail = None

# Arena
floor = Entity(model='plane', scale=(BOARD_W * CELL, 1, BOARD_H * CELL),
               position=(0, -0.03, 0), color=color.rgb(17, 24, 39),
               texture='white_cube', texture_scale=(BOARD_W, BOARD_H))
floor.rotation_x = 0
arena = Entity(model='wireframe_cube', scale=(BOARD_W * CELL, 0.02, BOARD_H * CELL),
               position=(0, 0, 0), color=color.rgba(100, 130, 170, 110))
# Grid lines are grouped into a single entity where possible.
for x in range(BOARD_W + 1):
    Entity(model='cube', scale=(0.012, 0.006, BOARD_H * CELL),
           position=((x - BOARD_W / 2) * CELL, 0.005, 0),
           color=color.rgba(75, 95, 130, 70))
for z in range(BOARD_H + 1):
    Entity(model='cube', scale=(BOARD_W * CELL, 0.006, 0.012),
           position=(0, 0.005, (z - BOARD_H / 2) * CELL),
           color=color.rgba(75, 95, 130, 70))

camera.position = (0, 22, -24)
camera.rotation_x = 35
camera.fov = 65

title = Text('PYTHON TRON', origin=(0, 0), scale=2.4, y=0.28,
             color=color.rgb(100, 190, 255))
subtitle = Text('KÉT JÁTÉKOS  •  NE ÜTKÖZZ A FÉNYCSÍKOKKAL!', origin=(0, 0),
                scale=0.9, y=0.16, color=color.light_gray)
instructions = Text('Kék: W A S D     |     Piros: nyilak\nENTER – indítás / új játék     ESC – kilépés',
                    origin=(0, 0), scale=1.0, y=-0.08, color=color.white)
status_text = Text('', origin=(0, 0), scale=1.4, y=0.34, color=color.white)
score_text = Text('', origin=(0, 0), scale=1.0, y=0.45, color=color.white)
hint = Text('ENTER', origin=(0, 0), scale=1.1, y=-0.35, color=color.rgb(100, 190, 255))

def cell_to_world(cell):
    return ((cell[0] - BOARD_W / 2 + 0.5) * CELL, TRAIL_Y,
            (cell[1] - BOARD_H / 2 + 0.5) * CELL)

def path_mesh(path, tint):
    # One mesh per rider, rebuilt only after a move rather than every frame.
    vertices = []
    triangles = []
    colors = []
    half = CELL * 0.36
    for cx, cz in path:
        x, _, z = cell_to_world((cx, cz))
        base = len(vertices)
        vertices.extend([
            Vec3(x-half, TRAIL_Y, z-half), Vec3(x+half, TRAIL_Y, z-half),
            Vec3(x+half, TRAIL_Y, z+half), Vec3(x-half, TRAIL_Y, z+half),
            Vec3(x-half, TRAIL_Y+0.035, z-half), Vec3(x+half, TRAIL_Y+0.035, z-half),
            Vec3(x+half, TRAIL_Y+0.035, z+half), Vec3(x-half, TRAIL_Y+0.035, z+half),
        ])
        triangles.extend([
            (base+0,base+1,base+2),(base+0,base+2,base+3),
            (base+4,base+6,base+5),(base+4,base+7,base+6),
            (base+0,base+4,base+5),(base+0,base+5,base+1),
            (base+1,base+5,base+6),(base+1,base+6,base+2),
            (base+2,base+6,base+7),(base+2,base+7,base+3),
            (base+3,base+7,base+4),(base+3,base+4,base+0),
        ])
        colors.extend([tint] * 8)
    mesh = Mesh(vertices=vertices, triangles=triangles, colors=colors, mode='triangle')
    mesh.generate()
    return mesh

def refresh_trails():
    global blue_mesh, red_mesh
    if blue_trail:
        blue_trail.model = path_mesh(blue_path, color.rgb(40, 170, 255))
    if red_trail:
        red_trail.model = path_mesh(red_path, color.rgb(255, 65, 95))

def update_score():
    score_text.text = f'KÉK  {score_blue}     :     {score_red}  PIROS'
    score_text.enabled = True

def reset_round():
    global state, countdown_value, countdown_elapsed, move_elapsed
    global blue_path, red_path, blue_grid, red_grid, blue_dir, red_dir
    global blue_next_dir, red_next_dir, blue_trail, red_trail, winner_text
    blue_path = [(7, BOARD_H // 2)]
    red_path = [(BOARD_W - 8, BOARD_H // 2)]
    blue_grid = set(blue_path)
    red_grid = set(red_path)
    blue_dir = (1, 0)
    red_dir = (-1, 0)
    blue_next_dir = blue_dir
    red_next_dir = red_dir
    move_elapsed = 0.0
    countdown_elapsed = 0.0
    countdown_value = 3
    winner_text = ''
    if blue_trail:
        destroy(blue_trail)
    if red_trail:
        destroy(red_trail)
    blue_trail = Entity(model=path_mesh(blue_path, color.rgb(40, 170, 255)),
                        color=color.rgb(40, 170, 255), unlit=True)
    red_trail = Entity(model=path_mesh(red_path, color.rgb(255, 65, 95)),
                       color=color.rgb(255, 65, 95), unlit=True)
    state = 'countdown'
    title.enabled = subtitle.enabled = instructions.enabled = hint.enabled = False
    status_text.enabled = True
    status_text.text = '3'
    update_score()

def set_direction(player, direction):
    global blue_next_dir, red_next_dir
    current = blue_dir if player == 'blue' else red_dir
    queued = blue_next_dir if player == 'blue' else red_next_dir
    # Disallow 180-degree turns, including multiple keypresses between moves.
    if direction != (-current[0], -current[1]) and direction != (-queued[0], -queued[1]):
        if player == 'blue':
            blue_next_dir = direction
        else:
            red_next_dir = direction

def finish_round(winner):
    global state, winner_text, score_blue, score_red
    state = 'gameover'
    winner_text = winner
    if winner == 'KÉK':
        score_blue += 1
    elif winner == 'PIROS':
        score_red += 1
    status_text.text = ('DÖNTETLEN!' if winner == 'DÖNTETLEN' else f'{winner} JÁTÉKOS NYERT!')
    status_text.color = color.white
    update_score()
    hint.text = 'ENTER – új menet'
    hint.enabled = True

def step_game():
    global blue_dir, red_dir
    blue_dir, red_dir = blue_next_dir, red_next_dir
    b0, r0 = blue_path[-1], red_path[-1]
    b1 = (b0[0] + blue_dir[0], b0[1] + blue_dir[1])
    r1 = (r0[0] + red_dir[0], r0[1] + red_dir[1])

    def crashed(pos, own_grid, other_grid):
        x, z = pos
        return (x < 0 or x >= BOARD_W or z < 0 or z >= BOARD_H
                or pos in own_grid or pos in other_grid)

    blue_crash = crashed(b1, blue_grid, red_grid)
    red_crash = crashed(r1, red_grid, blue_grid)
    if b1 == r1:
        blue_crash = red_crash = True
    if blue_crash and red_crash:
        finish_round('DÖNTETLEN')
        return
    if blue_crash:
        finish_round('PIROS')
        return
    if red_crash:
        finish_round('KÉK')
        return

    blue_path.append(b1)
    red_path.append(r1)
    blue_grid.add(b1)
    red_grid.add(r1)
    refresh_trails()

def input(key):
    if key == 'escape':
        application.quit()
    if key == 'enter':
        if state in ('start', 'gameover'):
            reset_round()
    # Blue rider: WASD
    controls = {'w': (0, 1), 's': (0, -1), 'a': (-1, 0), 'd': (1, 0)}
    if key in controls and state in ('countdown', 'playing'):
        set_direction('blue', controls[key])
    # Red rider: arrow keys
    arrows = {'up arrow': (0, 1), 'down arrow': (0, -1),
              'left arrow': (-1, 0), 'right arrow': (1, 0)}
    if key in arrows and state in ('countdown', 'playing'):
        set_direction('red', arrows[key])

def update():
    global state, countdown_elapsed, countdown_value, move_elapsed
    if state == 'countdown':
        countdown_elapsed += time.dt
        if countdown_elapsed >= 1.0:
            countdown_elapsed -= 1.0
            countdown_value -= 1
            if countdown_value > 0:
                status_text.text = str(countdown_value)
            else:
                state = 'playing'
                status_text.text = 'RAJT!'
                invoke(setattr, status_text, 'enabled', False, delay=0.65)
    elif state == 'playing':
        move_elapsed += time.dt
        if move_elapsed >= MOVE_INTERVAL:
            move_elapsed %= MOVE_INTERVAL
            step_game()

# Start screen
status_text.enabled = False
score_text.enabled = False
hint.enabled = True

app.run()
