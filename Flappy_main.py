import random
import pygame
import sys
from pygame.locals import *

FPS = 32
s_w = 350
s_h = 500
s = pygame.display.set_mode((s_w, s_h))
g = s_h * 0.8
g_s = {}
g_sd = {}
PLAYER = "sprites/plane.png"
b_g = "sprites/b_g.png"
PIPE = "sprites/building.png"


def welcome_screen():
    px = int(s_w / 5)
    py = int((s_h - g_s['player'].get_height()) / 2)
    mx = int((s_w - g_s['message'].get_width()) / 2)
    my = int(s_h * 0.13)
    bx = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                s.blit(g_s['background'], (0, 0))
                s.blit(g_s['player'], (px, py))
                s.blit(g_s['message'], (mx, my))
                s.blit(g_s['base'], (bx, g))
                pygame.display.update()
                fps_clock.tick(FPS)


def main_game():
    score = 0
    px = int(s_w / 5)
    py = int(s_w / 2)
    bx = 0

    new_pipe1 = get_random_pipe()
    new_pipe2 = get_random_pipe()

    u_p = [
        {'x': s_w + 200, 'y': new_pipe1[0]['y']},
        {'x': s_w + 200 + (s_w / 2), 'y': new_pipe2[0]['y']}
    ]
    l_p = [
        {'x': s_w + 200, 'y': new_pipe1[1]['y']},
        {'x': s_w + 200 + (s_w / 2), 'y': new_pipe2[1]['y']}
    ]
    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAcc = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if py > 0:
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    g_sd['wing'].play()
        crashTest = isCollide(px, py, u_p, l_p)
        if crashTest:
            return

        playerMidPos = px + g_s['player'].get_width()/2
        for pip in u_p:
            pipeMidPos = pip['x'] + g_s['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your Score is: {score}")
                g_sd['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        p_h = g_s['player'].get_height()
        py = py + min(playerVelY, g - py - p_h)

        for u_ps, l_ps in zip(u_p, l_p):
            u_ps['x'] += pipeVelX
            l_ps['x'] += pipeVelX

        if 0 < u_p[0]['x'] < 5:
            new_pipe = get_random_pipe()
            u_p.append(new_pipe[0])
            l_p.append(new_pipe[1])

        if u_p[0]['x'] < -g_s['pipe'][0].get_width():
            u_p.pop(0)
            l_p.pop(0)

        s.blit(g_s['background'], (0, 0))
        for u_ps, l_ps in zip(u_p, l_p):
            s.blit(g_s['pipe'][0], (u_ps['x'], u_ps['y']))
            s.blit(g_s['pipe'][1], (l_ps['x'], l_ps['y']))
        s.blit(g_s['base'], (bx, g))
        s.blit(g_s['player'], (px, py))
        m_d = [int(x) for x in list(str(score))]
        width = 0
        for d in m_d:
            width += g_s['numbers'][d].get_width()
        x_os = (s_w - width) / 2
        for o in m_d:
            s.blit(g_s['numbers'][o], (x_os, s_h * 0.12))
            x_os += g_s['numbers'][o].get_width()
        pygame.display.update()
        fps_clock.tick(FPS)


def isCollide(px, py, u_p, l_p):
    if py > g - g_s['player'].get_height() or py < 0 or py > g_s['pipe'][0].get_height() + 90:
        pygame.mixer.stop()
        g_sd['hit'].play()
        return True

    for pip in u_p:
        p_h = g_s['pipe'][0].get_height()
        if (py < p_h + pip['y']) and abs(px - pip['x']) < g_s['pipe'][0].get_width():
            pygame.mixer.stop()
            g_sd['hit'].play()
            return True

    for pip in l_p:
        if (py + g_s['player'].get_height() > pip['y']) and abs(px - pip['x']) < g_s['pipe'][0].get_width():
            pygame.mixer.stop()
            g_sd['hit'].play()
            return True

    return False


def get_random_pipe():
    p_h = g_s['pipe'][0].get_height()
    o_s = s_h / 3
    y2 = o_s + random.randrange(0, int(s_h - g_s['base'].get_height() - 1.2 * o_s))
    pipe_x = s_w + 10
    y1 = p_h - y2 + o_s
    pipe = [
        {'x': pipe_x, 'y': -y1},
        {'x': pipe_x, 'y': y2}
    ]
    return pipe


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Airplane")
    g_s['numbers'] = (
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )
    g_s['message'] = pygame.image.load('sprites/message.png').convert_alpha()
    g_s['base'] = pygame.image.load('sprites/base.png').convert_alpha()
    g_s['background'] = pygame.image.load(b_g).convert()
    g_s['player'] = pygame.image.load(PLAYER).convert_alpha()
    g_s['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha(),
    )

    g_sd['hit'] = pygame.mixer.Sound('sounds/hit.mp3')
    g_sd['point'] = pygame.mixer.Sound('sounds/point.mp3')
    g_sd['wing'] = pygame.mixer.Sound('sounds/wing.mp3')

    while True:
        welcome_screen()
        main_game()
