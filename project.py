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
    apple = (random.randrange(0, 25), random.randrange(0, 25))
    while apple in snake:
        apple = (random.randrange(0, 25), random.randrange(0, 25))
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game1_sprites)
    board = Board(25, 25, snake, apple)
    board.set_view(50, 50, 20)
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
        if snake[0][0]  + vx == -1 or snake[0][1] + vy < 0 or snake[0][0] + vx > 24 or snake[0][1] + vy > 24 or len(snake) != len(set(snake)):
            end = True
        if not end:
            if (snake[0][0] + vx, snake[0][1] + vy) == apple:
                snake = [(snake[0][0] + vx, snake[0][1] + vy)] + snake[:]
                apple = (random.randrange(0, 25), random.randrange(0, 25))
                while apple in snake:
                    apple = (random.randrange(0, 25), random.randrange(0, 25))
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
        intro_rect.x = 600

        game1_sprites.draw(screen)
        board.render(snake, apple)
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()

        clock.tick(fps_game1)


def f_game2():
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

def f_game3():
    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, x, y):
            super().__init__(tiles_group, game3_sprites)
            self.type = tile_type
            self.image = tile_images[tile_type]
            self.coords = (x, y)
            self.rect = self.image.get_rect().move(x, y)
            self.stop = False

        def collide(self, tiles, direction):
            for tile in tiles:
                xt, yt = tile.coords
                x, y = self.coords
                if direction == 'r':
                    return y == yt and xt - x == 80 and not tile.stop
                if direction == 'l':
                    return y == yt and x - xt == 80  and not tile.stop
                if direction == 'u':
                    return x == xt and y - yt == 80 and not tile.stop
                if direction == 'd':
                    return x == xt and yt - y == 80 and not tile.stop


        def update(self, e):
            if e == pygame.K_RIGHT:
                x, y = self.coords
                self.stop = True if y == 460 else False
                print(self.collide(tiles, 'r'), self.coords, self.type)
                while self.collide(tiles, 'r') or not self.stop:

                    #print(pygame.sprite.spritecollideany(self, tiles_group))
                    x, y = self.coords
                    x += 10
                    self.rect = self.image.get_rect().move(x, y)
                    self.coords = (x, y)
                    self.stop = True if y == 460 else False
                    tiles.clear()
                    tiles.append(self)
            if e == pygame.K_LEFT:
                pass
            if e == pygame.K_UP:
                pass
            if e == pygame.K_DOWN:
                pass


    class Fon(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(fon_group, game3_sprites)
            self.type = 0
            self.image = tile_images[0]
            self.rect = self.image.get_rect().move(x, y)
            self.coords = (x, y)


    def left():
        for i in range(6):
            a = []
            a_zero = []
            for j in range(6):
                if map_2048[i][j] != 0:
                    a.append(map_2048[i][j])
                else:
                    a_zero.append(0)
            map_2048[i] = a + a_zero

    def right():
        for i in range(6):
            a = []
            a_zero = []
            for j in range(6):
                if map_2048[i][j] != 0:
                    a.append(map_2048[i][j])
                else:
                    a_zero.append(0)
            map_2048[i] = a_zero + a

    def up():
        for j in range(6):
            a = []
            a_zero = []
            for i in range(6):
                if map_2048[i][j] != 0:
                    a.append(map_2048[i][j])
                else:
                    a_zero.append(0)
            for i in range(6):
                a += a_zero
                map_2048[i][j] = a[i]

    def down():
        for j in range(6):
            a = []
            a_zero = []
            for i in range(6):
                if map_2048[i][j] != 0:
                    a.append(map_2048[i][j])
                else:
                    a_zero.append(0)
            for i in range(6):
                a_zero += a
                map_2048[i][j] = a_zero[i]

    fon_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    game3_sprites = pygame.sprite.Group()
    tiles = []
    clock = pygame.time.Clock()
    back = Button(load_image('back.jpg'), 600, 450)
    back.add(game3_sprites)
    tile_images = {}
    for x in [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
        tile_images[x] = load_image('2048', f'{x}.jpg')
    map_2048 = [[int(x) for x in line.strip().split()] for line in open(os.path.join('data', '2048', 'map.txt')).readlines()]
    print(map_2048)
    while True:
        screen.fill('#000000')
        tiles.clear()
        for i in range(0, 6):
            for j in range(0, 6):
                pos = map_2048[j][i]
                if pos == 0:
                    fon = Fon(60 + i * 80, 60 + j * 80)
                else:
                    fon = Fon(60 + i * 80, 60 + j * 80)
                    tile = Tile(pos, 60 + i * 80, 60 + j * 80)
                    tiles.append(tile)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
            elif event.type == pygame.KEYDOWN:
                tiles_group.update(event.key)
                #pygame.draw.rect(screen, (10, 10, 10), (60 + i * 80 + 1, 60 + j * 80 + 1, 78, 78))
                #rect = load_image(f'2048/{map_2048[i][j]}.jpg').get_rect().move(60 + i * 80, 60 + j * 80)
                #screen.blit(load_image('2048', f'{map_2048[i][j]}.jpg'), (60 + i * 80, 60 + j * 80))

        #pygame.draw.rect(screen, '#303030', (50, 50, 500, 500))
        game3_sprites.draw(screen)
        fon_group.draw(screen)
        tiles_group.draw(screen)


        pygame.display.flip()
        clock.tick(FPS)

def f_game4():
    class Wall(pygame.sprite.Sprite):
        def __init__(self, tile_type, x, y):
            super().__init__(walls_group, game4_sprites)
            self.image = images[tile_type]
            self.rect = self.image.get_rect().move(x, y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(player_group, game4_sprites)
            self.image = images[-1]
            self.rect = self.image.get_rect().move(x, y)

    clock = pygame.time.Clock()
    game4_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game4_sprites)
    images = {}
    for x in range(-1, 16):
        images[x] = load_image('maze', f'{x}.jpg')
    map_maze = [[int(x) for x in line.strip().split()] for line in
                open(os.path.join('data', 'maze', 'map1.txt')).readlines()]
    for i in range(len(map_maze)):
        for j in range(len(map_maze[i])):
            if map_maze[i][j] == -1:
                Wall(0, 54 + j * 12, 54 + i * 12)
                player = Player(54 + j * 12 - 0, 54 + i * 12 - 0)
            else:
                Wall(map_maze[i][j], 54 + j * 12, 54 + i * 12)
    while True:
        screen.fill('#000000')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.rect.x += 12
                if event.key == pygame.K_LEFT:
                    player.rect.x -= 12
                if event.key == pygame.K_UP:
                    player.rect.y -= 12
                if event.key == pygame.K_DOWN:
                    player.rect.y += 12
        game4_sprites.draw(screen)
        player_group.draw(screen)
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
