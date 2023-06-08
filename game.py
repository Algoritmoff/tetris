import pygame
import os
from random import *
from time import *
os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
back = (255, 255, 200)
black = (0, 0, 0)
red = (0, 0, 0)
w = 1600
h = 800
mw = pygame.display.set_mode((w, h))
mw.fill(back)
pygame.mixer.music.load('les.ogg')
take = pygame.mixer.Sound('take.ogg')
right = pygame.mixer.Sound('right.ogg')
wrong = pygame.mixer.Sound('wrong.ogg')
pygame.mixer.music.play()
clock = pygame.time.Clock()
tablet_time = round(time())
lives_time = round(time())
score_time = round(time())
timer = 1
score = 0
score_timer = 1
lives = 3
total = ''
md = 122
game_mode = 'menu'
difficult = 'ЛЁГКАЯ'
speed = 20
down = 2
# списки
tablets = []
tablet_texts = []
chests = []
menu_texts = []
# флаги для игрока
player_move_left = False
player_move_right = False
player_run_load_right = False
player_run_load_left = True
create_table_text = True
space_down = False
load = False
def capacity(num):
    if 0 < num < 9:
        razr = 3
    elif 9 < num < 100 or -10 < num < 0:
        razr = 2
    else:
        razr = 1
    return razr
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=(0, 0, 0)):
        """ область: прямоугольник в нужном месте и нужного цвета """
        # запоминаем прямоугольник:
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)
# класс для объектов-картинок
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)

    def draw(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont(
            'verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        # self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
# создание спрайтов
back = Picture('back.jpg', 0, 0, w, h)
chest1 = Picture('chest.png', w-650, h-150, 101, 99)
chest2 = Picture('chest.png', w-450, h-150, 101, 99)
chest3 = Picture('chest.png', w-250, h-150, 101, 99)
player_r_e_l = Picture('player_run_empty_left.png', w/2-200, h-160, 130, 130)
player_r_e_r = Picture('player_run_empty_right.png', w/2-200, h-160, 130, 130)
player_r_l_l = Picture('player_run_load_left.png',
                       player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
player_r_l_r = Picture('player_run_load_right.png',
                       player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
menu_tablet1 = Picture('menu_tablet.png', w/2-325, h/2-100, 650, 99)
menu_tablet2 = Picture('menu_tablet.png', w/2-325, h/2+20, 650, 99)
menu_tablet3 = Picture('menu_tablet_small.png', w/2-205, h/2+140, 650, 99)

# флаг окончания игры
game_over = False

while not game_over and game_mode == 'menu':
    pygame.display.update()
    back.draw()
    menu_tablet1.draw()
    menu_tablet2.draw()
    menu_tablet3.draw()

    menu_text = Label(w/2-160, h/2-350, 50, 23, red)
    menu_text.set_text('-МЕНЮ-', 88, red)
    menu_text.draw()
    # menu_texts.append(menu_text)
    dif_up_text = Label(w/2-297, h/2-90, 50, 23, red)
    dif_up_text.set_text('Сложность Больше', 60, red)
    dif_up_text.draw()
    # menu_texts.append(dif_up_text)
    dif_down_text = Label(w/2-302, h/2+30, 50, 23, red)
    dif_down_text.set_text('Сложность Меньше', 60, red)
    dif_down_text.draw()
    # menu_texts.append(dif_down_text)
    difficult_text = Label(w/2-md, h/2+150, 50, 23, red)
    difficult_text.set_text(str(difficult), 60, red)
    difficult_text.draw()
    # menu_texts.append(difficult_text)
    # for M_T in menu_texts:
    #     M_T.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if menu_tablet1.collidepoint(pos[0], pos[1]):
                if difficult == 'ЛЁГКАЯ':
                    difficult = 'СРЕДНЯЯ'
                    md = 144
                    speed = 15
                    down = 4
                elif difficult == 'СРЕДНЯЯ':
                    difficult = 'ТЯЖЁЛАЯ'
                    md = 150
                    speed = 10
                    down = 6
                else:
                    difficult = 'ТЯЖЁЛАЯ'
            if menu_tablet2.collidepoint(pos[0], pos[1]):
                if difficult == 'ТЯЖЁЛАЯ':
                    difficult = 'СРЕДНЯЯ'
                    md = 144
                    speed = 15
                    down = 4
                elif difficult == 'СРЕДНЯЯ':
                    difficult = 'ЛЁГКАЯ'
                    md = 122
                    speed = 20
                    down = 2
                else:
                    difficult = 'ЛЁГКАЯ'
            if menu_tablet3.collidepoint(pos[0], pos[1]):
                game_mode = 'play'

    clock.tick(20)

while not game_over and game_mode == 'play':
    back.draw()
    chest1.draw()
    chest2.draw()
    chest3.draw()

    if round(time()) - tablet_time > timer:
        create_table_text = True
        timer = speed
        # создание примеров
        z = choice('*-+')
        if z == '-':
            x = randint(0, 100)
            y = randint(0, 100)
            total = x-y
        elif z == '*':
            x = randint(0, 10)
            y = randint(0, 10)
            total = x*y
        # elif z == '/':
            # total = x/y
        elif z == '+':
            x = randint(0, 100)
            y = randint(0, 100)
            total = x+y
        primer = str(x)+' '+z+' '+str(y)
        tablet = Picture('tablet.png', 50, -100, 180, 96)
        tablet_text = Label(tablet.rect.x+25, tablet.rect.y+25, 50, 33, red)
        tablet_text.set_text(primer, 33, red)
        tablets.append(tablet)
        tablet_texts.append(tablet_text)
        tablet_time = round(time())
        if create_table_text:
            create_table_text = False
            rttt = randint(1, 3)
            if rttt == 1:
                print(rttt)
                # chest11_text = Label(chest1.rect.x+65,chest1.rect.y+22,50,48,back)
                # chest11_text.set_text(str(total),52,black)
                razr = capacity(total)
                chest1_text = Label(
                    chest1.rect.x+25*razr, chest1.rect.y+45, 50, 48, red)
                chest1_text.set_text(str(total), 44, red)
                # chests.append(chest11_text)
                chests.append(chest1_text)
                num = randint(0, 100)
                razr = capacity(num)
                chest2_text = Label(
                    chest2.rect.x+25*razr, chest2.rect.y+45, 50, 23, red)
                chest2_text.set_text(str(num), 44, red)
                chests.append(chest2_text)
                num = randint(0, 100)
                razr = capacity(num)
                chest3_text = Label(
                    chest3.rect.x+25*razr, chest3.rect.y+45, 50, 23, red)
                chest3_text.set_text(str(randint(0, 100)), 44, red)
                chests.append(chest3_text)
            elif rttt == 2:
                print(rttt)
                # chest11_text = Label(chest1.rect.x+65,chest1.rect.y+22,50,48,back)
                # chest11_text.set_text(str(rtt),52,black)
                num = randint(0, 100)
                razr = capacity(num)
                chest1_text = Label(
                    chest1.rect.x+25*razr, chest1.rect.y+45, 50, 48, red)
                chest1_text.set_text(str(randint(0, 100)), 44, red)
                # chests.append(chest11_text)
                chests.append(chest1_text)
                razr = capacity(total)
                chest2_text = Label(
                    chest2.rect.x+25*razr, chest2.rect.y+45, 50, 48, red)
                chest2_text.set_text(str(total), 44, red)
                chests.append(chest2_text)
                num = randint(0, 100)
                razr = capacity(num)
                chest3_text = Label(
                    chest3.rect.x+25*razr, chest3.rect.y+45, 50, 48, red)
                chest3_text.set_text(str(randint(0, 100)), 44, red)
                chests.append(chest3_text)
            elif rttt == 3:
                print(rttt)
                # chest11_text = Label(chest1.rect.x+65,chest1.rect.y+22,50,48,back)
                # chest11_text.set_text(str(rtt),52,black)
                num = randint(0, 100)
                razr = capacity(num)
                chest1_text = Label(
                    chest1.rect.x+25*razr, chest1.rect.y+45, 50, 23, red)
                chest1_text.set_text(str(randint(0, 100)), 44, red)
                # chests.append(chest11_text)
                chests.append(chest1_text)
                num = randint(0, 100)
                razr = capacity(num)
                chest2_text = Label(
                    chest2.rect.x+25*razr, chest2.rect.y+45, 50, 23, red)
                chest2_text.set_text(str(randint(0, 100)), 44, red)
                chests.append(chest2_text)
                razr = capacity(total)
                chest3_text = Label(
                    chest3.rect.x+25*razr, chest3.rect.y+45, 50, 23, red)
                chest3_text.set_text(str(total), 44, red)
                chests.append(chest3_text)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_RIGHT:  # если нажата клавиша
                player_run_load_right = True
                player_run_load_left = False
                player_move_right = True  # поднимаем флаг
            if event.key == pygame.K_LEFT:
                player_run_load_right = False
                player_run_load_left = True
                player_move_left = True  # поднимаем флаг
            if event.key == pygame.K_SPACE:
                space_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_move_right = False  # опускаем флаг
            if event.key == pygame.K_LEFT:
                player_move_left = False  # опускаем флаг
            if event.key == pygame.K_SPACE:
                space_down = False

    if player_run_load_right and player_move_right and load:
        player_r_l_r.rect.x += speed
        player_r_l_l.rect.x = player_r_l_r.rect.x
    if player_run_load_right and player_move_left and load:
        player_r_l_r.rect.x -= speed
        player_r_l_l.rect.x = player_r_l_r.rect.x
    if player_run_load_left and player_move_right and load:
        player_r_l_l.rect.x += speed
        player_r_l_r.rect.x = player_r_l_l.rect.x
    if player_run_load_left and player_move_left and load:
        player_r_l_l.rect.x -= speed
        player_r_l_r.rect.x = player_r_l_l.rect.x
    if player_run_load_right and player_move_right and not load:
        player_r_e_r.rect.x += speed
        player_r_e_l.rect.x = player_r_e_r.rect.x
    if player_run_load_right and player_move_left and not load:
        player_r_e_r.rect.x -= speed
        player_r_e_l.rect.x = player_r_e_r.rect.x
    if player_run_load_left and player_move_right and not load:
        player_r_e_l.rect.x += speed
        player_r_e_r.rect.x = player_r_e_l.rect.x
    if player_run_load_left and player_move_left and not load:
        player_r_e_l.rect.x -= speed
        player_r_e_r.rect.x = player_r_e_l.rect.x

    for T in tablets:
        T.rect.y += down
        T.draw()
        if T.rect.colliderect(player_r_l_l.rect) or T.rect.colliderect(player_r_l_r.rect) and right_answer == rttt:
            right.play()
            player_r_e_l.rect.x = player_r_l_l.rect.x
            player_r_e_r.rect.x = player_r_l_r.rect.x
            tablets.remove(T)
            score += 1
            chests = []
            load = False
        if T.rect.y > h-100:
            wrong.play()
            player_r_e_l.rect.x = player_r_l_l.rect.x
            player_r_e_r.rect.x = player_r_l_r.rect.x
            tablets.remove(T)
            score -= 1
            chests = []
            load = False

    for T_T in tablet_texts:
        T_T.rect.y += down
        T_T.draw()
        if T_T.rect.y > h:
            tablet_texts.remove(T_T)
    for CH in chests:
        CH.draw()
        if T.rect.y > h:
            chests = []
        if rttt == 1 and space_down and not load:
            if chests[0].rect.colliderect(player_r_e_l.rect) or chests[0].rect.colliderect(player_r_e_r.rect):
                player_r_l_l = Picture(
                    'player_run_load_left.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                player_r_l_r = Picture(
                    'player_run_load_right.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                take.play()
                load = True
                right_answer = 1
        elif CH == chest1_text and rttt != 1 and space_down and not load:
            if CH.rect.colliderect(player_r_e_l.rect) or CH.rect.colliderect(player_r_e_r.rect):
                if round(time()) - score_time > score_timer:
                    score -= 2
                    score_time = round(time())
        if rttt == 2 and space_down and not load:
            if chests[1].rect.colliderect(player_r_e_l.rect) or chests[1].rect.colliderect(player_r_e_r.rect):
                player_r_l_l = Picture(
                    'player_run_load_left.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                player_r_l_r = Picture(
                    'player_run_load_right.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                take.play()
                load = True
                right_answer = 2
        elif CH == chest2_text and rttt != 2 and space_down and not load:
            if CH.rect.colliderect(player_r_e_l.rect) or CH.rect.colliderect(player_r_e_r.rect):
                if round(time()) - score_time > score_timer:
                    score -= 2
                    score_time = round(time())
        if rttt == 3 and space_down and not load:
            if chests[2].rect.colliderect(player_r_e_l.rect) or chests[2].rect.colliderect(player_r_e_r.rect):
                player_r_l_l = Picture(
                    'player_run_load_left.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                player_r_l_r = Picture(
                    'player_run_load_right.png', player_r_e_l.rect.x, player_r_e_l.rect.y, 130, 130)
                take.play()
                load = True
                right_answer = 3
        elif CH == chest3_text and rttt != 3 and space_down and not load:
            if CH.rect.colliderect(player_r_e_l.rect) or CH.rect.colliderect(player_r_e_r.rect):
                if round(time()) - score_time > score_timer:
                    score -= 2
                    score_time = round(time())

    if player_run_load_right and load:
        player_r_l_r.draw()
    elif player_run_load_left and load:
        player_r_l_l.draw()
    if player_run_load_right and not load:
        player_r_e_r.draw()
    elif player_run_load_left and not load:
        player_r_e_l.draw()
    score_text = Label(w-300, h-750, 50, 23, red)
    score_text.set_text('Счёт: '+str(score), 44, red)
    score_text.draw()
    pygame.display.update()
    clock.tick(20)
