"""
Python Tron – Turtle változat
Kétjátékos Tron-játék a Python beépített turtle moduljával.
Indítás: python tron_turtle.py
"""

import turtle
import time

WIDTH, HEIGHT = 900, 650
STEP = 10
TICK = 0.055
LIMIT_X = WIDTH // 2 - 20
LIMIT_Y = HEIGHT // 2 - 55

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Python Tron – Turtle")
screen.bgcolor("#07111f")
screen.tracer(0)

blue = turtle.Turtle()
red = turtle.Turtle()
for rider, colour in ((blue, "#38bdf8"), (red, "#fb476f")):
    rider.shape("square")
    rider.shapesize(0.55, 0.55)
    rider.color(colour)
    rider.penup()
    rider.speed(0)

hud = turtle.Turtle(visible=False)
hud.penup()
hud.color("white")

overlay = turtle.Turtle(visible=False)
overlay.penup()
overlay.color("#e8f3ff")

blue_dir = (1, 0)
red_dir = (-1, 0)
blue_queued = blue_dir
red_queued = red_dir
blue_cells = set()
red_cells = set()
state = "start"
score_blue = 0
score_red = 0
last_move = 0.0
countdown_start = 0.0
countdown_shown = None


def draw_arena():
    border = turtle.Turtle(visible=False)
    border.speed(0)
    border.color("#334155")
    border.penup()
    border.goto(-LIMIT_X, -LIMIT_Y)
    border.pendown()
    for point in ((LIMIT_X, -LIMIT_Y), (LIMIT_X, LIMIT_Y),
                  (-LIMIT_X, LIMIT_Y), (-LIMIT_X, -LIMIT_Y)):
        border.goto(point)
    border.penup()
    border.goto(0, LIMIT_Y + 12)
    border.color("#94a3b8")
    border.write("KÉK: W A S D     |     PIROS: NYÍLBILLENTYŰK",
                 align="center", font=("Arial", 10, "normal"))


def draw_hud(message="", show_score=True):
    hud.clear()
    hud.goto(0, HEIGHT // 2 - 35)
    if show_score:
        hud.write(f"KÉK  {score_blue}     :     {score_red}  PIROS",
                  align="center", font=("Arial", 16, "bold"))
    if message:
        hud.goto(0, -HEIGHT // 2 + 12)
        hud.write(message, align="center", font=("Arial", 11, "normal"))


def show_start():
    global state
    state = "start"
    blue.hideturtle()
    red.hideturtle()
    overlay.clear()
    overlay.goto(0, 65)
    overlay.color("#38bdf8")
    overlay.write("PYTHON TRON", align="center",
                  font=("Arial", 34, "bold"))
    overlay.goto(0, 15)
    overlay.color("white")
    overlay.write("Két játékos – kerüld el a falakat és a fénycsíkokat!",
                  align="center", font=("Arial", 13, "normal"))
    overlay.goto(0, -35)
    overlay.write("ENTER: indítás     ESC: kilépés",
                  align="center", font=("Arial", 15, "bold"))
    draw_hud("Kék: W A S D     |     Piros: nyílbillentyűk", False)
    screen.update()


def reset_round():
    global blue_dir, red_dir, blue_queued, red_queued
    global blue_cells, red_cells, state, last_move
    global countdown_start, countdown_shown
    blue.clear()
    red.clear()
    blue.penup()
    red.penup()
    blue.color("#38bdf8")
    red.color("#fb476f")
    blue.goto(-LIMIT_X + 70, 0)
    red.goto(LIMIT_X - 70, 0)
    blue.setheading(0)
    red.setheading(180)
    blue.pendown()
    red.pendown()
    blue_dir = blue_queued = (1, 0)
    red_dir = red_queued = (-1, 0)
    blue_cells = {(round(blue.xcor()), round(blue.ycor()))}
    red_cells = {(round(red.xcor()), round(red.ycor()))}
    blue.showturtle()
    red.showturtle()
    overlay.clear()
    state = "countdown"
    countdown_start = time.monotonic()
    countdown_shown = None
    last_move = countdown_start
    draw_hud()


def set_direction(player, direction):
    global blue_queued, red_queued
    current = blue_dir if player == "blue" else red_dir
    queued = blue_queued if player == "blue" else red_queued
    if direction != (-current[0], -current[1]) and direction != (-queued[0], -queued[1]):
        if player == "blue":
            blue_queued = direction
        else:
            red_queued = direction


def finish_round(winner):
    global state, score_blue, score_red
    state = "gameover"
    if winner == "KÉK":
        score_blue += 1
    elif winner == "PIROS":
        score_red += 1
    overlay.clear()
    overlay.goto(0, 30)
    overlay.color("#e8f3ff")
    message = "DÖNTETLEN!" if winner == "DÖNTETLEN" else f"{winner} JÁTÉKOS NYERT!"
    overlay.write(message, align="center", font=("Arial", 28, "bold"))
    overlay.goto(0, -20)
    overlay.write("ENTER: új menet     ESC: kilépés",
                  align="center", font=("Arial", 14, "normal"))
    draw_hud()
    screen.update()


def next_position(pos, direction):
    return (pos[0] + direction[0] * STEP,
            pos[1] + direction[1] * STEP)


def collides(pos, own, other):
    x, y = pos
    if abs(x) > LIMIT_X or abs(y) > LIMIT_Y:
        return True
    # Turtle trail is drawn as a thick line; a small radius makes collision fair.
    for cells in (own, other):
        for px, py in cells:
            if abs(x - px) < STEP * 0.8 and abs(y - py) < STEP * 0.8:
                return True
    return False


def move_riders():
    global blue_dir, red_dir
    blue_dir, red_dir = blue_queued, red_queued
    bpos = next_position((round(blue.xcor()), round(blue.ycor())), blue_dir)
    rpos = next_position((round(red.xcor()), round(red.ycor())), red_dir)

    b_crash = collides(bpos, blue_cells, red_cells)
    r_crash = collides(rpos, red_cells, blue_cells)
    if bpos == rpos:
        b_crash = r_crash = True
    if b_crash and r_crash:
        finish_round("DÖNTETLEN")
        return
    if b_crash:
        finish_round("PIROS")
        return
    if r_crash:
        finish_round("KÉK")
        return

    blue.goto(*bpos)
    red.goto(*rpos)
    blue_cells.add(bpos)
    red_cells.add(rpos)


def tick():
    global state, countdown_shown, last_move
    now = time.monotonic()
    if state == "countdown":
        number = 3 - int(now - countdown_start)
        if number != countdown_shown:
            countdown_shown = number
            overlay.clear()
            overlay.goto(0, -5)
            overlay.color("#e8f3ff")
            if number > 0:
                overlay.write(str(number), align="center",
                              font=("Arial", 42, "bold"))
            else:
                overlay.write("RAJT!", align="center",
                              font=("Arial", 34, "bold"))
                state = "playing"
                last_move = now
        if state == "playing":
            screen.ontimer(tick, 400)
            screen.update()
            return
    elif state == "playing" and now - last_move >= TICK:
        last_move = now
        move_riders()
    screen.update()
    screen.ontimer(tick, 16)


def start_game():
    if state in ("start", "gameover"):
        reset_round()


def quit_game():
    screen.bye()


# Keyboard controls
screen.listen()
screen.onkeypress(lambda: set_direction("blue", (0, 1)), "w")
screen.onkeypress(lambda: set_direction("blue", (0, -1)), "s")
screen.onkeypress(lambda: set_direction("blue", (-1, 0)), "a")
screen.onkeypress(lambda: set_direction("blue", (1, 0)), "d")
screen.onkeypress(lambda: set_direction("red", (0, 1)), "Up")
screen.onkeypress(lambda: set_direction("red", (0, -1)), "Down")
screen.onkeypress(lambda: set_direction("red", (-1, 0)), "Left")
screen.onkeypress(lambda: set_direction("red", (1, 0)), "Right")
screen.onkeypress(start_game, "Return")
screen.onkeypress(quit_game, "Escape")

draw_arena()
show_start()
tick()
screen.mainloop()
