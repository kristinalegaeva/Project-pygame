import random
import pygame
import os
import sys
import pygame_gui
from PIL import Image


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
        if not (self.left < x < self.left + self.width * self.cell_size and \
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


def f_snake():
    # фон
    snake_fon = load_image('snake fon.jpg')
    # рекорды
    rec_snake = RECORDS['snake']
    now_snake = 0

    fps_snake = 2 + SNAKE * 2

    # игорвое поле
    snake = [(15, 15), (16, 15), (17, 15)]
    vx, vy = -1, 0
    apple = (random.randrange(0, 25), random.randrange(0, 25))
    while apple in snake:
        apple = (random.randrange(0, 25), random.randrange(0, 25))
    board = Board(25, 25, snake, apple)
    board.set_view(50, 50, 20)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    # кнопки
    replay_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 264), (160, 54)),
        text='replay',
        manager=manager)

    pause_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 367), (160, 54)),
        text='pause',
        manager=manager)

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 471), (160, 54)),
        text='back',
        manager=manager)

    end = pause = False
    clock = pygame.time.Clock()

    while True:
        screen.blit(snake_fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == replay_btn:
                        if end:
                            if SOUND:
                                game_over_music.fadeout(200)
                            if MUSIC and SOUND:
                                snake_music.play(-1)
                        f_snake()
                        return
                    if event.ui_element == pause_btn:
                        pause = not pause
                    if event.ui_element == back_btn:
                        return
            elif event.type == pygame.KEYDOWN and not end and not pause:
                if event.key == pygame.K_RIGHT and vy != -1:
                    vx, vy = 0, 1
                elif event.key == pygame.K_LEFT and vy != 1:
                    vx, vy = 0, -1
                elif event.key == pygame.K_UP and vx != 1:
                    vx, vy = -1, 0
                elif event.key == pygame.K_DOWN and vx != -1:
                    vx, vy = 1, 0
            manager.process_events(event)
        manager.update(fps_snake)
        manager.draw_ui(screen)

        # проверка - закончилась ли игра
        if (snake[0][0] + vx == -1 or snake[0][1] + vy < 0 or snake[0][0] + vx > 24 or \
            snake[0][1] + vy > 24 or len(snake) != len(set(snake))) and not end and not pause:
            end = True
            if SOUND:
                game_over_music.play()
            if MUSIC and SOUND:
                snake_music.stop()

        # игра не закончена и не на паузе
        if not end and not pause:
            if (snake[0][0] + vx, snake[0][1] + vy) == apple:
                snake = [(snake[0][0] + vx, snake[0][1] + vy)] + snake[:]
                apple = (random.randrange(0, 25), random.randrange(0, 25))
                while apple in snake:
                    apple = (random.randrange(0, 25), random.randrange(0, 25))
                now_snake += 10
                if rec_snake < now_snake:
                    rec_snake = now_snake
                    RECORDS['snake'] = now_snake
                    f = open(os.path.join('data', 'records.txt'), mode='w')
                    text = [f"{RECORDS['snake']}", f"{RECORDS['jump']}",
                            f"{' '.join(list(map(str, RECORDS['maze'])))}"]
                    f.write('\n'.join(text))
                    f.close()
                if SOUND:
                    point_s_music.play()
            else:
                snake = [(snake[0][0] + vx, snake[0][1] + vy)] + snake[:-1]

        # вывод счета
        string_rendered = font.render(f'{now_snake} / {rec_snake}', 1, pygame.Color('#b39fe0'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50 + (50 - intro_rect.height) / 2
        intro_rect.x = 570 + (200 - intro_rect.width) / 2

        board.render(snake, apple)
        screen.blit(string_rendered, intro_rect)
        if end:
            screen.blit(game_over_picture, (50, 50))
        pygame.display.flip()
        clock.tick(fps_snake)


def f_jump():
    # классы блоков и игрока
    class Block(pygame.sprite.Sprite):
        def __init__(self, i):
            super().__init__(blocks_group)
            self.image = block_image
            self.rect = self.image.get_rect().move(50 + i * 100, 400)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__(player_group)
            self.image = player_image
            self.rect = self.image.get_rect().move(50, 330)

    # проверка, что нет двух пустот рядом
    def check(a):
        for i in range(1, len(a)):
            if a[i - 1] == 0 and a[i] == 0:
                return False
        return True

    def new_blocks(blocks, n):
        blocks = blocks[n:] + [random.choice([0, 1]) for _ in range(n)]
        while not (len(blocks) == 8 and check(blocks)):
            blocks = blocks[:-n] + [random.choice([0, 1]) for _ in range(n)]
        return blocks

    # фон
    fon = load_image('jump', 'fon.png')
    background = load_image('jump', 'fon.jpg')

    # рекорды
    rec_jump = RECORDS['jump']
    now_jump = 0

    fps_jump = 20

    # компоненты игры

    blocks_group = pygame.sprite.Group()
    jump_block_group = pygame.sprite.Group()
    block_image = load_image('jump', 'block.png')
    player_image = load_image('jump', 'player.png')
    player_group = pygame.sprite.Group()
    player = Player()
    player_low = AnimatedSprite(load_image('jump', 'player_low.png'), 17, 1, 150, 240)
    player_high = AnimatedSprite(load_image('jump', 'player_high.png'), 17, 1, 150, 140)
    player_falls = AnimatedSprite(load_image('jump', 'player_falls.png'), 4, 1, 150, 330)
    end = False
    end_group = pygame.sprite.Group(player_falls)
    player_now = player_low
    jump_player_group = pygame.sprite.Group()
    #  список блоков
    blocks = [0] + [random.choice([1, 0]) for _ in range(7)]
    while not check(blocks):
        blocks = [0] + [random.choice([1, 0]) for _ in range(7)]
    for i in range(len(blocks)):
        if blocks[i]:
            Block(i)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    # кнопки
    replay_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 367), (160, 54)),
        text='replay',
        manager=manager)

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 471), (160, 54)),
        text='back',
        manager=manager)

    clock = pygame.time.Clock()
    while True:
        screen.fill('#000000')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == replay_btn:
                        if end:
                            if SOUND:
                                game_over_music.fadeout(200)
                            if MUSIC and SOUND:
                                jump_music.play(-1)
                        f_jump()
                        return
                    if event.ui_element == back_btn:
                        return
            elif event.type == pygame.KEYDOWN and not end:
                if event.key == 32 and not player_now.start:
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        if SOUND:
                            jump2_music.play()
                        player_now = player_high
                        n = 2
                    else:
                        if SOUND:
                            jump1_music.play()
                        player_now = player_low
                        n = 1
                    jump_player_group = pygame.sprite.Group(player_now)
                    player_now.cur_frame = 0
                    player_now.start = True
                    a = []
                    for i in range(len(blocks)):
                        if blocks[i]:
                            a.append(AnimatedSprite(load_image('jump', str(n) + '.png'), 1, 17,
                                                    50 + (i - n) * 100, 400))
                    for x in a:
                        x.cur_frame = 0
                    jump_block_group = pygame.sprite.Group(*a)

                    blocks = new_blocks(blocks, n)
                    if blocks[1] == 0 and not end:
                        end = True
                        if MUSIC and SOUND:
                            jump_music.stop()
                        if SOUND:
                            game_over_music.play()
                    elif not end:
                        now_jump += 5 * n

                    blocks_group = pygame.sprite.Group()
                    for i in range(len(blocks)):
                        if blocks[i]:
                            Block(i)
            manager.process_events(event)

        screen.blit(background, (50, 50))

        if player_now.start:  # прыжок
            if player_now.cur_frame == len(player_now.frames) and not end and SOUND:
                jump3_music.play()
            jump_block_group.update()
            jump_block_group.draw(screen)
            jump_player_group.update()
            jump_player_group.draw(screen)
        elif end:  # конец игры
            end_group.draw(screen)
            end_group.update()
            blocks_group.draw(screen)
            screen.blit(game_over_picture, (50, 50))
        else:  # стоим на месте
            blocks_group.draw(screen)
            screen.blit(player.image, (150, 330))

        screen.blit(fon, (0, 0))
        manager.update(fps_jump)
        manager.draw_ui(screen)
        if rec_jump < now_jump:
            rec_jump = now_jump
            RECORDS['jump'] = now_jump
            f = open(os.path.join('data', 'records.txt'), mode='w')
            text = [f"{RECORDS['snake']}", f"{RECORDS['jump']}",
                    f"{' '.join(list(map(str, RECORDS['maze'])))}"]
            f.write('\n'.join(text))
            f.close()

        # вывод рекордов
        string_rendered = font.render(f'{now_jump} / {rec_jump}', 1, pygame.Color('#b39fe0'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50 + (50 - intro_rect.height) / 2
        intro_rect.x = 570 + (200 - intro_rect.width) / 2
        screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(fps_jump)


def f_puzzle(picture):
    class Piece(pygame.sprite.Sprite):
        def __init__(self, image, pos_x, pos_y):
            super().__init__(puzzle_sprites)
            self.image = pieces_images[image]
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.name = image

    # выбор изображения
    def start():
        clock = pygame.time.Clock()
        start_group = pygame.sprite.Group()
        start = []
        for i in range(3):
            a = []
            for j in range(4):
                picture = str(j + i * 4 + 1)
                im = Button(pygame.transform.scale(load_image('puzzle', 'images', picture + '.jpg'),
                                                   (150, 150)), 50 + (33 + 150) * j,
                            50 + (25 + 150) * i)
                start_group.add(im)
                a.append((im, picture))
            start.append(a)

        while True:
            screen.fill('#000000')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coords = pygame.mouse.get_pos()
                    click1_music.play()
                    for lst in start:
                        for x in lst:
                            if x[0].rect.collidepoint(coords):
                                return x[1]
            start_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

    # разрезка на части
    def new_game(n):
        def random_list(n):
            m = [random.randint(1, n + 1) for _ in range(n)]
            while len(set(m)) != n:
                m = [random.randint(1, n) for _ in range(n)]
            return m

        im = Image.open(os.path.join('data', 'puzzle', 'images', picture + '.jpg'))
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
                im.crop((x0, y0, x1, y1)).save(
                    os.path.join('data', 'puzzle', 'pieces', f'{name}.jpg'))
                pieces_images[name] = load_image('puzzle', 'pieces', f'{name}.jpg')

    # фон
    fon = load_image('puzzle', 'fon.jpg')
    # игровое поле
    end = False
    puzzle_sprites = pygame.sprite.Group()
    move_piece = pygame.sprite.Group()
    pieces_images = {}
    n = COUNT
    new_game(n)
    pieces_map = [str(i + 1) + str(j + 1) for i in range(n) for j in range(n)]
    random.shuffle(pieces_map)
    pieces_map = [[pieces_map[i + j * n] for i in range(n)] for j in range(n)]
    pieces = []
    # маленькое изображение
    image = pygame.transform.scale(load_image('puzzle', 'images', picture + '.jpg'), (190, 190))
    # части пазла
    for i in range(n):
        a = []
        for j in range(n):
            p = Piece(pieces_map[i][j], 50 + i * (500 // n), 50 + j * (500 // n))
            a.append(p)
        pieces.append(a)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    # кнопки
    replay_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 312), (160, 54)),
        text='replay',
        manager=manager)

    picture_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 396), (160, 54)),
        text='picture',
        manager=manager)

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 480), (160, 54)),
        text='back',
        manager=manager)

    f = False
    clock = pygame.time.Clock()

    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif (event.type == pygame.MOUSEBUTTONDOWN or f and \
                  event.type == pygame.MOUSEMOTION) and not end:
                coords = pygame.mouse.get_pos()
                for i in range(n):
                    for j in range(n):
                        if 60 + i * (500 // n) < coords[0] < 40 + (i + 1) * (
                                500 // n) and 60 + j * (500 // n) < coords[1] < 40 + (j + 1) * (
                                500 // n) and not f:
                            f = True
                            pos_now = (i, j)
                            move_piece = pygame.sprite.Group(pieces[pos_now[0]][pos_now[1]])
                            if SOUND:
                                click1_music.play()
                            break
                if f:
                    pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][pos_now[1]].rect.y = \
                        coords[0] - 250 // n, coords[1] - 250 // n
            elif event.type == pygame.MOUSEBUTTONUP and f and not end:
                coords = pygame.mouse.get_pos()
                for i in range(n):
                    for j in range(n):
                        if 60 + i * (500 // n) < coords[0] < 40 + (i + 1) * (
                                500 // n) and 60 + j * (500 // n) < coords[1] < 40 + (j + 1) * (
                                500 // n):
                            pieces[pos_now[0]][pos_now[1]], pieces[i][j] = \
                                pieces[i][j], pieces[pos_now[0]][pos_now[1]]
                            pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][
                                pos_now[1]].rect.y = 50 + pos_now[0] * (500 // n), \
                                                     50 + pos_now[1] * (500 // n)
                            pieces[i][j].rect.x, pieces[i][j].rect.y = \
                                50 + i * (500 // n), 50 + j * (500 // n)
                            pieces_map[i][j], pieces_map[pos_now[0]][pos_now[1]] = \
                                pieces_map[pos_now[0]][pos_now[1]], pieces_map[i][j]
                            if pieces_map == [[str(i + 1) + str(j + 1) for i in range(n)] for j in
                                              range(n)] and not end:
                                if MUSIC and SOUND:
                                    puzzle_music.fadeout(1000)
                                if SOUND:
                                    win_music.play()
                                end = True

                            f = False
                            if SOUND:
                                click2_music.play()
                            break
                if f:  # поменялись местами
                    pieces[pos_now[0]][pos_now[1]].rect.x, pieces[pos_now[0]][pos_now[1]].rect.y = \
                        50 + pos_now[0] * (500 // n), 50 + pos_now[1] * (
                                500 // n)
                    if SOUND:
                        click2_music.play()
                    f = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == replay_btn:
                        if end:
                            if SOUND:
                                win_music.fadeout(200)
                            if MUSIC and SOUND:
                                puzzle_music.play(-1)
                        f_puzzle(picture)
                        return
                    if event.ui_element == picture_btn:
                        f_puzzle(start())
                        return
                    if event.ui_element == back_btn:
                        return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        puzzle_sprites.draw(screen)
        screen.blit(image, (575, 50))
        move_piece.draw(screen)
        if end:
            screen.blit(win_picture, (50, 50))
        pygame.display.flip()
        clock.tick(FPS)


def f_maze(n):
    # классы стен игрока и бонусов
    class Wall(pygame.sprite.Sprite):
        def __init__(self, tile_type, x, y):
            super().__init__(walls_group, maze_sprites)
            self.image = images[tile_type]
            self.rect = self.image.get_rect().move(x, y)

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(player_group, maze_sprites)
            self.image = images[-1]
            self.rect = self.image.get_rect().move(x, y)

    class Point(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__(points_group, maze_sprites)
            self.image = images[-2]
            self.rect = self.image.get_rect().move(x, y)

    # фон
    fon = load_image('maze', 'fon.jpg')
    # рекорды
    rec_maze = RECORDS['maze'][int(n) - 1]
    now_maze = 0
    # игровое поле
    maze_sprites = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    points_group = pygame.sprite.Group()
    images = {}

    end = False
    for x in range(-1, 16):
        images[x] = load_image('maze', f'{x}.jpg')
    images[-2] = load_image('maze', '-2.png')
    images[-3] = load_image('maze', '-3.jpg')
    map_maze = [[int(x) for x in line.strip().split()] for line in
                open(os.path.join('data', 'maze', f'map{n}.txt')).readlines()]
    # бонусы
    for _ in range(20):
        i, j = random.randint(1, 39), random.randint(1, 39)
        while map_maze[i][j] != 0:
            i, j = random.randint(1, 39), random.randint(1, 39)
        map_maze[i][j] = -2

    # создание лабиринта
    for i in range(len(map_maze)):
        for j in range(len(map_maze[i])):
            if map_maze[i][j] == -1:
                Wall(0, 54 + j * 12, 54 + i * 12)
                player = Player(54 + j * 12 - 0, 54 + i * 12 - 0)
            elif map_maze[i][j] == -2:
                Wall(0, 54 + j * 12, 54 + i * 12)
                Point(54 + j * 12 - 2, 54 + i * 12 - 2)
            else:
                Wall(map_maze[i][j], 54 + j * 12, 54 + i * 12)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    # кнопки
    map1_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 145), (160, 54)),
        text='map 1',
        manager=manager)

    map2_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 229), (160, 54)),
        text='map 2',
        manager=manager)

    map3_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 313), (160, 54)),
        text='map 3',
        manager=manager)

    replay_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 397), (160, 54)),
        text='replay',
        manager=manager)

    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((590, 481), (160, 54)),
        text='back',
        manager=manager)

    clock = pygame.time.Clock()
    while True:
        screen.blit(fon, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and not end:
                i, j = (player.rect.y - 54) // 12, (player.rect.x - 54) // 12
                if event.key == pygame.K_RIGHT and map_maze[i][j + 1] not in range(1, 16):
                    if map_maze[i][j + 1] == 0:
                        map_maze[i][j] = -3
                    elif map_maze[i][j + 1] == -3:
                        map_maze[i][j] = 0
                    elif map_maze[i][j + 1] == -2:
                        map_maze[i][j] = -3
                        now_maze += 10
                        if SOUND:
                            point_m_music.play()
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
                        point_m_music.play()
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
                        if SOUND:
                            point_m_music.play()
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
                        if SOUND:
                            point_m_music.play()
                    Wall(map_maze[i][j], player.rect.x, player.rect.y)
                    player.rect.y += 12
                    map_maze[i + 1][j] = -1
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == map1_btn and n != '1':
                        if end:
                            if SOUND:
                                win_music.fadeout(200)
                            if MUSIC and SOUND:
                                maze_music.play(-1)
                        f_maze('1')
                        return
                    elif event.ui_element == map2_btn and n != '2':
                        if end:
                            if SOUND:
                                win_music.fadeout(200)
                            if MUSIC and SOUND:
                                maze_music.play(-1)
                        f_maze('2')
                        return
                    elif event.ui_element == map3_btn and n != '3':
                        if end:
                            if SOUND:
                                win_music.fadeout(200)
                            if MUSIC and SOUND:
                                maze_music.play(-1)
                        f_maze('3')
                        return
                    elif event.ui_element == replay_btn:
                        if end:
                            if SOUND:
                                win_music.fadeout(200)
                            if MUSIC and SOUND:
                                maze_music.play(-1)
                        f_maze(n)
                        return
                    elif event.ui_element == back_btn:
                        return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)

        if map_maze[40][39] == -1 and not end:
            end = True
            now_maze += 100
            if MUSIC and SOUND:
                maze_music.fadeout(1000)
            if SOUND:
                win_music.play()

        if rec_maze < now_maze:
            rec_maze = now_maze
            RECORDS['maze'][int(n) - 1] = now_maze
            f = open(os.path.join('data', 'records.txt'), mode='w')
            text = [f"{RECORDS['snake']}", f"{RECORDS['jump']}",
                    f"{' '.join(list(map(str, RECORDS['maze'])))}"]
            f.write('\n'.join(text))
            f.close()

        # вывдо текста
        string_rendered = font.render(f'{now_maze} / {rec_maze}', 1, pygame.Color('#b39fe0'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50 + (50 - intro_rect.height) / 2
        intro_rect.x = 570 + (200 - intro_rect.width) / 2
        maze_sprites.draw(screen)
        player_group.draw(screen)
        screen.blit(string_rendered, intro_rect)
        if end:
            screen.blit(win_picture, (50, 50))
        pygame.display.flip()
        clock.tick(FPS)


def f_records():
    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 446), (160, 54)),
        text='back',
        manager=manager)
    string_snake = ["snake", f"{RECORDS['snake']}"]
    string_jump = ["jump", f"{RECORDS['snake']}"]
    string_maze = ["maze"] + (list(map(str, RECORDS['maze'])))
    top, left = 75, 75
    for x in [string_snake, string_jump, string_maze]:
        for string_rendered in x:
            string_rendered = font.render(string_rendered, 1, pygame.Color('#b39fe0'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = top
            intro_rect.x = left + (180 - intro_rect.width) // 2
            top += intro_rect.height + 30
            screen.blit(string_rendered, intro_rect)
        top = 75
        left += 235

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_btn:
                        return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def f_rules():
    font = pygame.font.Font(os.path.join('data', '19689.otf'), 20)

    fon = load_image('fon rules.jpg')
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 490), (160, 54)),
        text='back',
        manager=manager)
    top = now_top = 50
    left = 65
    for x in [['Snape: Цель игры максимально вырасти, съедая красные поля, и не проиграть,',
               'врезавшись в тело змейки или в поля. Управление осуществляется с помощью',
               'клавиш курсора. За каждое красное поле начисляется +10 очков.'],
              ['Jump: Цель игры не упасть в пропасть. Управление осуществляется с клавиш.',
               'Маленький прыжок - пробел, сочетание Shift и пробела - большой прыжок.',
               'Одинарный прыжок +5 очков, двойной +10 очков'],
              ['Puzzle: Цель игры собрать картинку. Управление мышкой.'],
              ['Maze: Цель игры пройти лабиринт. Управление осуществляется с помощью',
               'клавиш курсора. За пройденный лабиринт + 100 очков, за синие бонусы +10 очков.']]:
        if len(x) == 2:
            now_top += 15
        elif len(x) == 1:
            now_top += 30
        for string_rendered in x:
            string_rendered = font.render(string_rendered, 1, pygame.Color('#ffffff'))
            intro_rect = string_rendered.get_rect()
            intro_rect.y = now_top
            intro_rect.x = left + (670 - intro_rect.width) // 2
            now_top += intro_rect.height + 5
            screen.blit(string_rendered, intro_rect)
        top += 110
        now_top = top

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_btn:
                        return
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def f_settings():
    global MUSIC, SOUND, SNAKE, COUNT
    font = pygame.font.Font(os.path.join('data', '19689.otf'), 30)

    fon = load_image('fon settings.jpg')
    screen.blit(fon, (0, 0))
    clock = pygame.time.Clock()

    string_rendered = font.render('музыка', 1, pygame.Color('#ffffff'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 80
    intro_rect.x = 50 + (200 - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('звуки', 1, pygame.Color('#ffffff'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 305
    intro_rect.x = 50 + (200 - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('количество делей пазла', 1, pygame.Color('#ffffff'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 80
    intro_rect.x = 300 + (450 - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)

    string_rendered = font.render('скорость змейки', 1, pygame.Color('#ffffff'))
    intro_rect = string_rendered.get_rect()
    intro_rect.y = 305
    intro_rect.x = 300 + (450 - intro_rect.width) // 2
    screen.blit(string_rendered, intro_rect)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    back_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 500), (160, 54)),
        text='back',
        manager=manager)

    music_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((80, 150), (140, 60)),
        text='on',
        manager=manager)

    sound_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((80, 375), (140, 60)),
        text='on',
        manager=manager)

    puzzle_4_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((325, 150), (60, 60)),
        text='4',
        manager=manager)

    puzzle_5_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((410, 150), (60, 60)),
        text='5',
        manager=manager)

    puzzle_6_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((495, 150), (60, 60)),
        text='6',
        manager=manager)

    puzzle_7_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((580, 150), (60, 60)),
        text='7',
        manager=manager)

    puzzle_8_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((665, 150), (60, 60)),
        text='8',
        manager=manager)

    snake_1_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((325, 375), (60, 60)),
        text='1',
        manager=manager)

    snake_2_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((410, 375), (60, 60)),
        text='2',
        manager=manager)

    snake_3_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((495, 375), (60, 60)),
        text='3',
        manager=manager)

    snake_4_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((580, 375), (60, 60)),
        text='4',
        manager=manager)

    snake_5_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((665, 375), (60, 60)),
        text='5',
        manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_btn:
                        return
                    elif event.ui_element == music_btn:
                        MUSIC = not MUSIC
                        if MUSIC:
                            music_btn.set_text('on')
                            fon_music.play(-1)
                        else:
                            fon_music.fadeout(500)
                            music_btn.set_text('off')
                    elif event.ui_element == sound_btn:
                        SOUND = not SOUND
                        if SOUND:
                            sound_btn.set_text('on')
                        else:
                            sound_btn.set_text('off')
                    elif event.ui_element == puzzle_4_btn:
                        COUNT = 4
                    elif event.ui_element == puzzle_5_btn:
                        COUNT = 5
                    elif event.ui_element == puzzle_6_btn:
                        COUNT = 6
                    elif event.ui_element == puzzle_7_btn:
                        COUNT = 7
                    elif event.ui_element == puzzle_8_btn:
                        COUNT = 8
                    elif event.ui_element == snake_1_btn:
                        SNAKE = 1
                    elif event.ui_element == snake_2_btn:
                        SNAKE = 2
                    elif event.ui_element == snake_3_btn:
                        SNAKE = 3
                    elif event.ui_element == snake_4_btn:
                        SNAKE = 4
                    elif event.ui_element == snake_5_btn:
                        SNAKE = 5
            manager.process_events(event)
        manager.update(FPS)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    # фон и музыка
    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    fon_music.play(loops=-1)

    manager = pygame_gui.UIManager((800, 600), os.path.join('data', 'menu_theme.json'))
    # кнопки
    snake_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 100), (160, 160)),
        text='snake',
        manager=manager)
    jump_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 100), (160, 160)),
        text='jump',
        manager=manager)
    puzzle_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 340), (160, 160)),
        text='puzzle',
        manager=manager)
    maze_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((320, 340), (160, 160)),
        text='maze',
        manager=manager)
    records_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((540, 100), (160, 54)),
        text='records',
        manager=manager)
    rules_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((540, 193), (160, 54)),
        text='rules',
        manager=manager)
    settings_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((540, 286), (160, 54)),
        text='settings',
        manager=manager)
    exit_btn = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((540, 446), (160, 54)),
        text='exit',
        manager=manager)

    clock = pygame.time.Clock()
    while True:
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == snake_btn:
                        if MUSIC:
                            fon_music.fadeout(1000)
                            snake_music.play(-1)
                        # SNAKE
                        f_snake()
                        if MUSIC:
                            snake_music.fadeout(1000)
                            fon_music.play(-1)
                        if SOUND:
                            game_over_music.fadeout(500)
                    if event.ui_element == jump_btn:
                        if MUSIC:
                            fon_music.fadeout(1000)
                            jump_music.play(-1)
                        # JUMP
                        f_jump()
                        if MUSIC:
                            jump_music.fadeout(1000)
                            fon_music.play(-1)
                        if SOUND:
                            game_over_music.fadeout(500)
                    if event.ui_element == puzzle_btn:
                        if MUSIC:
                            fon_music.fadeout(1000)
                            puzzle_music.play(-1)
                        # PUZZLE
                        f_puzzle('1')
                        if MUSIC:
                            puzzle_music.fadeout(1000)
                            fon_music.play(-1)
                    if event.ui_element == maze_btn:
                        if MUSIC:
                            fon_music.fadeout(1000)
                            maze_music.play(-1)
                        # MAZE
                        f_maze('1')
                        if MUSIC:
                            maze_music.fadeout(1000)
                            fon_music.play(-1)
                    if event.ui_element == records_btn:
                        f_records()
                    if event.ui_element == rules_btn:
                        f_rules()
                    if event.ui_element == settings_btn:
                        f_settings()
                    if event.ui_element == exit_btn:
                        terminate()
            manager.process_events(event)
        manager.update(FPS / 1000)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()

# константы
FPS = 50
MUSIC = SOUND = True
SNAKE = 3
COUNT = 4
f = [x for x in open(os.path.join('data', 'records.txt')).read().split('\n')]
RECORDS = {'snake': int(f[0]), 'jump': int(f[1]), 'maze': [int(x) for x in f[2].split()]}

# создание экрана
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mini games')
all_sprites = pygame.sprite.Group()
# загрузка некоторых данных
game_over_picture = load_image('game over.png')
win_picture = load_image('win.png')
font = pygame.font.Font(os.path.join('data', '19689.otf'), 36)

fon_music = pygame.mixer.Sound(os.path.join('data', 'music', 'fon.wav'))
snake_music = pygame.mixer.Sound(os.path.join('data', 'music', 's.wav'))
jump_music = pygame.mixer.Sound(os.path.join('data', 'music', 'j.wav'))
maze_music = pygame.mixer.Sound(os.path.join('data', 'music', 'm.wav'))
puzzle_music = pygame.mixer.Sound(os.path.join('data', 'music', 'p.wav'))

game_over_music = pygame.mixer.Sound(os.path.join('data', 'music', 'game over.wav'))
win_music = pygame.mixer.Sound(os.path.join('data', 'music', 'win.wav'))
point_m_music = pygame.mixer.Sound(os.path.join('data', 'music', 'point_m.wav'))
point_s_music = pygame.mixer.Sound(os.path.join('data', 'music', 'point_s.wav'))
click1_music = pygame.mixer.Sound(os.path.join('data', 'music', 'click1.wav'))
click2_music = pygame.mixer.Sound(os.path.join('data', 'music', 'click2.wav'))
jump1_music = pygame.mixer.Sound(os.path.join('data', 'music', 'fly low.wav'))
jump2_music = pygame.mixer.Sound(os.path.join('data', 'music', 'fly high.wav'))
jump3_music = pygame.mixer.Sound(os.path.join('data', 'music', 'fall.wav'))

# главная функция
start_screen()
