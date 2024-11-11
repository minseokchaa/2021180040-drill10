# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
import game_world
import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8



class Idle:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.face_dir = 1
            bird.dir = 1

        bird.frame_x = 0
        bird.frame_y = 0

    @staticmethod
    def exit(bird, e):
        if turn_around(e):
            if bird.face_dir == -1:
                bird.face_dir = 1
                bird.dir =1
            else:
                bird.face_dir = -1
                bird.dir = -1
            bird.frame_x = 0
            bird.frame_y = 0

    @staticmethod
    def do(bird):
        bird.frame_x = (bird.frame_x + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6

        if bird.frame_x == 5:
            bird.frame_y += 1
            bird.frame_x = 0

        if bird.frame_y == 2 and bird.frame_x == 4:
            bird.frame_x = 0
            bird.frame_y = 0


        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if bird.x > 1600:
            bird.state_machine.add_event(('Turn_around', 0))



    @staticmethod
    def draw(bird):
        if bird.face_dir == 1:
            bird.image.clip_draw(int(bird.frame_x) * 183, 337-(bird.frame_y*168), 183, 168, bird.x, bird.y)
        else:
            bird.image.clip_composite_draw(int(bird.frame_x) * 183, 337-(bird.frame_y*168), 183, 168, 0, 'h', bird.x, bird.y, 183, 168)






class Bird:

    def __init__(self):
        self.x, self.y = 400, 90
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Idle)
        self.state_machine.set_transitions(
            {
                Idle: {turn_around: Idle}
            }
        )


    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
