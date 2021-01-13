import random

import pygame
import os
import sys

from PIL import Image

f = [int(x) for x in open(os.path.join('data', 'records.txt')).read().split('\n')]
RECORDS = {(0, 'snake'): f[0], (1, 'puzzle'): f[1], (2, 'jump'): f[2], (3, 'maze'):f[3]}

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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.start = False

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, cycle=False):
        if not cycle:
            if self.cur_frame < len(self.frames):
                self.image = self.frames[self.cur_frame]
                self.cur_frame += 1
            else:
                self.start = False
        else:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]


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
        if end:
            screen.blit(game_over, (50, 50))

        pygame.display.flip()

        clock.tick(fps_game1)


def f_game2():

    class Block(pygame.sprite.Sprite):
        def __init__(self, i):
            super().__init__(blocks_group)
            self.image = block_image
            self.rect = self.image.get_rect().move(50 + i*100, 400)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(player_group)
            self.image = player_image
            self.rect = self.image.get_rect().move(50, 330)





    def check(a):
        for i in range(1, len(a)):
            if a[i-1] == 0 and a[i] == 0:
                return False
        return True

    def new_blocks(blocks, n):
        print('   ', blocks)
        blocks = blocks[n:] + [random.choice([0, 1]) for _ in range(n)]
        while not (len(blocks) == 8 and check(blocks)):
            blocks = blocks[:-n] + [random.choice([0, 1]) for _ in range(n)]
        return blocks


    fps_game2 = 18
    clock = pygame.time.Clock()
    game2_sprites = pygame.sprite.Group()
    blocks_group = pygame.sprite.Group()
    jump_group = pygame.sprite.Group()
    jump_block_group = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 650, 450)
    block_image = load_image('jump', 'block.png')
    player_image = load_image('jump', 'player.png')
    player_group = pygame.sprite.Group()
    player = Player()
    player_low = AnimatedSprite(load_image('jump', 'player_low.png'), 17, 1, 150, 240)
    player_high = AnimatedSprite(load_image('jump', 'player_high.png'), 17, 1, 150, 140)
    player_falls = AnimatedSprite(load_image('jump', 'player_falls.png'), 4, 1, 150, 330)
    end = fall = False
    rec_jump = RECORDS[(2, 'jump')]
    now_jump = 0
    font = pygame.font.Font(None, 30)
    end_group = pygame.sprite.Group(player_falls)
    player_now = player_low
    jump_player_group = pygame.sprite.Group()
    fon = load_image('jump', 'fon.png')
    blocks = [0] + [random.choice([1, 0]) for _ in range(7)]
    while not check(blocks):
        blocks = [0] + [random.choice([1, 0]) for _ in range(7)]
    for i in range(len(blocks)):
        if blocks[i]:
            Block(i)

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
                if event.key == 32 and event.mod in [1, 0] and player_now.start == False:
                    if event.mod == 0:
                        player_now = player_low
                        n = 1
                    else:
                        player_now = player_high
                        n = 2
                    jump_player_group = pygame.sprite.Group(player_now)
                    player_now.cur_frame = 0
                    player_now.start = True
                    a = []
                    for i in range(len(blocks)):
                        if blocks[i]:
                            a.append(AnimatedSprite(load_image('jump', str(n)+'.png'), 1, 17, 50 + (i - n)*100, 400))
                    for x in a:
                        x.cur_frame = 0
                    jump_block_group = pygame.sprite.Group(*a)

                    blocks = new_blocks(blocks, n)
                    print(blocks)
                    if blocks[1] ==0:
                        end = True
                    else:
                        now_jump += 5*n

                    blocks_group = pygame.sprite.Group()
                    for i in range(len(blocks)):
                        if blocks[i]:
                            Block(i)





        screen.fill('#000000')


        game2_sprites.draw(screen)
        game2_sprites.update()
        if player_now.start:
            jump_block_group.update()
            jump_block_group.draw(screen)
            jump_player_group.update()
            jump_player_group.draw(screen)
        elif end:
            end_group.draw(screen)
            end_group.update()
            blocks_group.draw(screen)
            screen.blit(game_over, (50, 50))
        else:
            blocks_group.draw(screen)
            screen.blit(player.image, (150, 330))

        screen.blit(fon, (0, 0))
        if rec_jump < now_jump:
            rec_jump = now_jump
            RECORDS[(2, 'jump')] = now_jump
            f = open(os.path.join('data', 'records.txt'), mode='w')
            f.write('\n'.join([str(RECORDS[game]) for game in sorted(RECORDS)]))
            f.close()

        string_rendered = font.render(f'{now_jump} / {rec_jump}', 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 600
        screen.blit(string_rendered, intro_rect)
        screen.blit(back.image, (650, 450))
        pygame.display.flip()
        clock.tick(fps_game2)


def f_game3():
    def new_game(n):
        def random_list(n):
            m = [random.randint(1, n+1) for _ in range(n)]
            while len(set(m)) != n:
                m = [random.randint(1, n) for _ in range(n)]
            return m
        im = Image.open(os.path.join('data', 'puzzle', 'images', picture+'.jpg'))
        pixels = im.load()
        x, y = im.size
        delta = x // n
        folder = os.path.join('data', 'puzzle', 'pieces')
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        for i in range(n):
            for j in range(n):
                x0, x1, y0, y1 = j * delta, (j + 1) * delta, i * delta, (i + 1) * delta
                name = f'{i + 1}{j + 1}'
                im.crop((x0, y0, x1, y1)).save(os.path.join('data', 'puzzle', 'pieces', f'{name}.jpg'))
                pieces_images[name] = load_image('puzzle', 'pieces', f'{name}.jpg')

    class Piece(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super().__init__(game1_sprites)
            self.image = pieces_images[image]
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.name = image

    picture = '6'
    end = False
    clock = pygame.time.Clock()
    game1_sprites = pygame.sprite.Group()
    move_piece = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 650, 450)
    back.add(game1_sprites)
    pieces_images = {}
    n = 4
    new_game(n)
    pieces_map = [str(i + 1) + str(j + 1) for i in range(n) for j in range(n)]
    random.shuffle(pieces_map)
    pieces_map = [[pieces_map[i + j * n] for i in range(n)] for j in range(n)]
    pieces = []
    image = pygame.transform.scale(load_image('puzzle', 'images', picture+'.jpg'), (150, 150))
    for i in range(n):
        a = []
        for j in range(n):
            p = Piece(pieces_map[i][j], 50 + i * (500//n), 50+ j * (500//n))
            a.append(p)
        pieces.append(a)

    f = False

    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.MOUSEBUTTONDOWN or f and event.type == pygame.MOUSEMOTION) and not end:
                coords = pygame.mouse.get_pos()
                for i in range(n):
                    for j in range(n):
                        if 60+i*(500//n) < coords[0] < 40 + (i + 1)*(500//n) and 60+j*(500//n) < coords[1] < 40 + (j + 1)*(500//n) and not f:
                            f = True
                            pos_now = (i, j)
                            move_piece = pygame.sprite.Group(pieces[pos_now[0]][pos_now[1]])
                            break
                if f:
                    pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][pos_now[1]].rect.y = coords[0] - 250//n, coords[1] - 250//n
            elif event.type == pygame.MOUSEBUTTONUP and f and not end:
                coords = pygame.mouse.get_pos()
                for i in range(n):
                    for j in range(n):
                        if 60+i*(500//n) < coords[0] < 40 + (i + 1)*(500//n) and 60+j*(500//n) < coords[1] < 40 + (j + 1)*(500//n):
                            pieces[pos_now[0]][pos_now[1]], pieces[i][j] = pieces[i][j], pieces[pos_now[0]][pos_now[1]]
                            # Piece(pieces[pos_now[0]][pos_now[1]].name, 50 + i * (500//n), 50 + j * (500//n))
                            # pieces[i][j] = Piece(pieces[i][j].name, 50 + pos_now[0] * (500//n), 50 + pos_now[1] * (500//n))
                            pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][pos_now[1]].rect.y = 50 + pos_now[0] * (500//n), 50 + pos_now[1] * (500//n)
                            pieces[i][j].rect.x, pieces[i][j].rect.y = 50+ i * (500//n), 50 + j * (500//n)
                            pieces_map[i][j], pieces_map[pos_now[0]][pos_now[1]] = pieces_map[pos_now[0]][pos_now[1]], pieces_map[i][j]
                            if pieces_map == [[str(i + 1) + str(j + 1) for i in range(n)] for j in range(n)]:
                                end = True

                            f = False
                            break
                if f:
                    pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][pos_now[1]].rect.y = 50 + pos_now[0] * (500//n), 50 + pos_now[1] * (500//n)
                    f = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = pygame.mouse.get_pos()
                if back.rect.collidepoint(coords):
                    return
        # if f:
        #     piece_now.update(*coords)

        game1_sprites.draw(screen)
        screen.blit(image, (600, 50))
        move_piece.draw(screen)
        if end:
            screen.blit(win, (50, 50))
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

    class Point(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(points_group, game4_sprites)
            self.image = images[-2]
            self.rect = self.image.get_rect().move(x, y)

    clock = pygame.time.Clock()
    game4_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    points_group = pygame.sprite.Group()
    back = Button(load_image('back.jpg'), 600, 400)
    back.add(game4_sprites)
    images = {}
    rec_maze = RECORDS[(3, 'maze')]
    now_maze = 0
    font = pygame.font.Font(None, 30)

    end = False
    for x in range(-1, 16):
        images[x] = load_image('maze', f'{x}.jpg')
    images[-2] = load_image('maze', '-2.png')
    images[-3] = load_image('maze', '-3.jpg')
    map_maze = [[int(x) for x in line.strip().split()] for line in
                open(os.path.join('data', 'maze', 'map3.txt')).readlines()]
    n = random.randint(5, 20)
    print(n)
    for i in range(len(map_maze)):
        for j in range(len(map_maze[i])):
            if map_maze[i][j] == -1:
                Wall(0, 54 + j * 12, 54 + i * 12)
                player = Player(54 + j * 12 - 0, 54 + i * 12 - 0)
            elif map_maze[i][j] == 0 and random.randint(0, 100) == 0:
                map_maze[i][j] = -2
                Wall(0, 54 + j * 12, 54 + i * 12)
                Point(54 + j * 12 - 2, 54 + i * 12 - 2)
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
            elif event.type == pygame.KEYDOWN and not end:
                i, j = (player.rect.y - 54) // 12, (player.rect.x - 54) // 12
                if event.key == pygame.K_RIGHT and map_maze[i][j + 1] not in range(1, 16):
                    if map_maze[i][j + 1] == 0 :
                        map_maze[i][j] = -3
                    elif map_maze[i][j + 1] == -3:
                        map_maze[i][j] = 0
                    elif map_maze[i][j + 1] == -2:
                        map_maze[i][j] = -3
                        now_maze += 10
                    Wall(map_maze[i][j], player.rect.x, player.rect.y)
                    player.rect.x += 12
                    map_maze[i][j + 1] = -1

                if event.key == pygame.K_LEFT and map_maze[i][j - 1] not in range(1, 16):
                    if map_maze[i][j - 1] == 0:
                        map_maze[i][j] = -3
                    elif map_maze[i][j - 1] == -3:
                        map_maze[i][j] = 0
                    elif map_maze[i][j - 1] == -2:
                        now_maze += 10
                        map_maze[i][j] = -3
                    Wall(map_maze[i][j], player.rect.x, player.rect.y)
                    player.rect.x -= 12
                    map_maze[i][j - 1] = -1

                if event.key == pygame.K_UP and map_maze[i - 1][j] not in range(1, 16):
                    if map_maze[i - 1][j] == 0:
                        map_maze[i][j] = -3
                    elif map_maze[i - 1][j] == -3:
                        map_maze[i][j] = 0
                    elif map_maze[i - 1][j] == -2:
                        map_maze[i][j] = -3
                        now_maze += 10
                    Wall(map_maze[i][j], player.rect.x, player.rect.y)
                    player.rect.y -= 12
                    map_maze[i - 1][j] = -1

                if event.key == pygame.K_DOWN and map_maze[i + 1][j] not in range(1, 16):
                    if map_maze[i + 1][j] == 0:
                        map_maze[i][j] = -3
                    elif map_maze[i + 1][j] == -3:
                        map_maze[i][j] = 0
                    elif map_maze[i + 1][j] == -2:
                        map_maze[i][j] = -3
                        now_maze += 10
                    Wall(map_maze[i][j], player.rect.x, player.rect.y)
                    player.rect.y += 12
                    map_maze[i + 1][j] = -1
        if map_maze[40][39] == -1 and not end:
            end = True
            now_maze += 100

        if rec_maze < now_maze:
            rec_maze = now_maze
            RECORDS[(3, 'maze')] = now_maze
            f = open(os.path.join('data', 'records.txt'), mode='w')
            f.write('\n'.join([str(RECORDS[game]) for game in sorted(RECORDS)]))
            f.close()

        string_rendered = font.render(f'{now_maze} / {rec_maze}', 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 600

        game4_sprites.draw(screen)
        player_group.draw(screen)
        #points_group.draw(screen)
        screen.blit(string_rendered, intro_rect)
        if end:
            screen.blit(win, (50, 50))
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

game_over = load_image('game over.png')
win = load_image('win.png')


start_screen()
