from ursina import *
import random as r

app = Ursina()

latar_belakang = Entity(model='quad', texture='assets/back1.mp4', scale=(40, 20), z=1)

bird = Animation('assets/img', collider='box', scale=(2, 2, 2), x=-10, y=0, z=0)
bird.disable()

camera.orthographic = True
camera.fov = 20

bird.velocity_y = 0
gravity = -40

game_active = False
score = 0

jump_sound = Audio('assets/wing.wav', autoplay=False)
background_music = Audio('assets/backsound.mp3', autoplay=True, loop=True)
collision_sound = Audio('assets/hit.wav', autoplay=False)
win_sound = Audio('assets/clap.mp3', autoplay=False)
lose_sound = Audio('assets/die.wav', autoplay=False)
pass_pipe_sound = Audio('assets/point.wav', autoplay=False)

pipe_speed = 7
elapsed_time = 0

win_sprite = Sprite('assets/images.png', scale=2, visible=False)
lose_sprite = Sprite('assets/kalah.png', scale=0.5, visible=False)

def start_button_action():
    start_button.visible = False
    start_game()

start_button = Button(texture='assets/message.png', scale=(0.5, 0.7), position=(0, 0), on_click=start_button_action)

score_text = Text(text=f'Score: {score}', position=(0.5, 0.4), origin=(0, 0), scale=2)

def update():
    global game_active, elapsed_time, score
    
    if game_active:
        bird.y += bird.velocity_y * time.dt
        bird.velocity_y += gravity * time.dt
        
        elapsed_time += time.dt
        if elapsed_time >= 10:
            increase_pipe_speed()
            elapsed_time = 0
        
        for p in pipes:
            p.x -= pipe_speed * time.dt
            if p.x < bird.x and not p.passed:
                p.passed = True
                score += 5
                score_text.text = f'Score: {score}'
                pass_pipe_sound.play()
        
        touch = bird.intersects()
        if touch.hit or bird.y < -10:
            collision_sound.play()
            lose_game()

def input(key):
    global game_active
    
    if key == 'space':
        if not game_active:
            start_button.visible = False
            start_game()
        else:
            bird_jump()

def start_game():
    global game_active, score
    game_active = True
    bird.enable()
    score = 0
    score_text.text = f'Score: {score}'
    invoke(win_game, delay=60)

def bird_jump():
    bird.velocity_y = 12
    jump_sound.play()

def win_game():
    global game_active
    game_active = False
    win_sound.play()
    win_sprite.visible = True
    for p in pipes:
        p.disable()
    bird.disable()

def lose_game():
    global game_active
    game_active = False
    lose_sound.play()
    lose_sprite.visible = True
    for p in pipes:
        p.disable()
    bird.disable()

pipes = []

pipe = Entity(model='quad',
              color=color.green,
              texture='white_cube',
              position=(20, 10),
              scale=(3, 15, 1),
              collider='box')

pipe.passed = False

def newPipe():
    y = r.randint(4, 12)
    new1 = duplicate(pipe, y=y)
    new2 = duplicate(pipe, y=y - 22)
    new1.passed = False
    new2.passed = False
    pipes.extend((new1, new2))
    invoke(newPipe, delay=2)

def increase_pipe_speed():
    global pipe_speed
    pipe_speed += 6

newPipe()

app.run()
