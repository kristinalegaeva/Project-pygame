import random

import pygame
import os
import sys

f = [int(x) for x in open(os.path.join('data', 'records.txt')).read().split('\n')]
RECORDS = {(0, 'snake'): f[0], (1, '2048'): f[1], (2, 'jump'): f[2], (3, 'maze'):f[3]}

def terminate():
    pygame.quit()
    sys.exit()


def load_image(*name, color_key=None):
    fullname = os.path.join('data', *name)
    image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Board:

    # создание поля
    def __init__(self, width, height, snake, apple):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        for xy in snake:
            self.board[xy[0]][xy[1]] = 1
        self.board[apple[0]][apple[1]] = -1
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 10

    def render(self, snake, apple):
        self.board = [[0] * width for _ in range(height)]
        self.board[apple[0]][apple[1]] = -1
        for xy in snake:
            self.board[xy[0]][xy[1]] = 1
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == -1:
                    color = '#cc0000'
                elif self.board[i][j] == 1:
                    color = '#ffaa44'
                else:
                    color = '#000000'
                pygame.draw.rect(screen,
                                 color,
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size))
                pygame.draw.rect(screen,
                                 (30, 30, 30),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    # настройка внешнего вида - масштабирование
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        # клик не в доске
        if not (self.left < x < self.left + self.width * self.cell_size and\
                self.top < y < self.top + self.height * self.cell_size):
            return None
        # вычисление координаты клетки поля
        return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size

    def get_click(self, mouse_pos):
        return self.get_cell(mouse_pos)


class Button(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = image
        self.rect = self.image.get_rect().move(pos_x, pos_y)



def f_game1():
    font = pygame.font.Font(None, 30)
    rec_snake = RECORDS[(0, 'snake')]
    now_snake = 0
    fps_game1 = 6
    snake = [(15, 15), (16, 15), (17, 15)]
    vx, vy = -1, 0
    apple = (random.randrange(0, 20), random.randrange(0, 20))
    while apple in snake:
        apple = (random.randrange(0, 20), random.randrange(0, 20))
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game1_sprites)
    board = Board(20, 20, snake, apple)
    board.set_view(100, 100, 20)
    end = False

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
            elif event.type == pygame.KEYDOWN and not end:
                if event.key == pygame.K_RIGHT and vy != -1:
                    vx, vy = 0, 1
                elif event.key == pygame.K_LEFT and vy != 1:
                    vx, vy = 0, -1
                elif event.key == pygame.K_UP and vx != 1:
                    vx, vy = -1, 0
                elif event.key == pygame.K_DOWN and vx != -1:
                    vx, vy = 1, 0
        if snake[0][0]  + vx == -1 or snake[0][1] + vy < 0 or snake[0][0] + vx > 19 or snake[0][1] + vy > 19 or len(snake) != len(set(snake)):
            end = True
        if not end:
            if (snake[0][0] + vx, snake[0][1] + vy) == apple:
                snake = [(snake[0][0] + vx, snake[0][1] + vy)] + snake[:]
                apple = (random.randrange(0, 20), random.randrange(0, 20))
                while apple in snake:
                    apple = (random.randrange(0, 20), random.randrange(0, 20))
                now_snake += 10
                if rec_snake < now_snake:
                    rec_snake = now_snake
                    RECORDS[(0, 'snake')] = now_snake
                    f = open(os.path.join('data', 'records.txt'), mode='w')
                    f.write('\n'.join([str(RECORDS[game]) for game in sorted(RECORDS)]))
                    f.close()
            else:
                snake = [(snake[0][0] + vx, snake[0][1] + vy)] + snake[:-1]

        string_rendered = font.render(f'{now_snake} / {rec_snake}', 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 400

        game1_sprites.draw(screen)
        board.render(snake, apple)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

        clock.tick(fps_game1)


def f_game2():
    clock = pygame.time.Clock()
    game2_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game2_sprites)

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        game2_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def f_game3():
    clock = pygame.time.Clock()
    game3_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 450)
    back.add(game3_sprites)
    map_2048 = [[int(x) for x in line.strip().split()] for line in open(os.path.join('data', '2048', 'map.txt')).readlines()]
    print(map_2048)
    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        pygame.draw.rect(screen, (100, 100, 100), (60, 60, 480, 480))
        game3_sprites.draw(screen)

        for i in range(0, 6):
            for j in range(0, 6):
                #pygame.draw.rect(screen, (10, 10, 10), (60 + i * 80 + 1, 60 + j * 80 + 1, 78, 78))
                #rect = load_image(f'2048/{map_2048[i][j]}.jpg').get_rect().move(60 + i * 80, 60 + j * 80)
                screen.blit(load_image('2048', f'{map_2048[i][j]}.jpg'), (60 + i * 80, 60 + j * 80))

        pygame.display.flip()
        clock.tick(FPS)

def f_game4():
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 100, 100)
    back.add(game1_sprites)

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        game1_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def f_records():
    screen.fill('#000000')
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game1_sprites)
    rec = [str(x) for x in RECORDS]
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for game in sorted(RECORDS):
        string_rendered = font.render(f'{game[-1]}: {RECORDS[game]}', 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 50
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        game1_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def f_rules():
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 100, 100)
    back.add(game1_sprites)

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        game1_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def f_settings():
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 100, 100)
    back.add(game1_sprites)

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        game1_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

def start_screen():
    fon = load_image('start screen', 'fon.jpg')
    screen.blit(fon, (0, 0))

    game1 = Button(load_image('start screen', 'snake.jpg'), 100, 100)
    game2 = Button(load_image('start screen', 'jump.jpg'), 325, 100)
    game3 = Button(load_image('start screen', '2048.jpg'), 100, 350)
    game4 = Button(load_image('start screen', 'maze.jpg'), 325, 350)
    records = Button(load_image('start screen', 'records.jpg'), 550, 100)
    rules = Button(load_image('start screen', 'rules.jpg'), 550, 200)
    settings = Button(load_image('start screen', 'settings.jpg'), 550, 450)
    button_sprites = pygame.sprite.Group(game1, game2, game3, game4, records, rules, settings)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if game1.rect.collidepoint(coords):
                    f_game1()
                elif game2.rect.collidepoint(coords):
                    f_game2()
                elif game3.rect.collidepoint(coords):
                    f_game3()
                elif game4.rect.collidepoint(coords):
                    f_game4()
                elif records.rect.collidepoint(coords):
                    f_records()
                elif rules.rect.collidepoint(coords):
                    f_rules()
                elif settings.rect.collidepoint(coords):
                    f_settings()
        screen.blit(fon, (0, 0))
        button_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()
FPS = 50
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('')
all_sprites = pygame.sprite.Group()

start_screen()
