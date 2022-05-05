import pygame
import config


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

pos_ships_enemy_attack = [-1, -1]
pos_ships_mine_attack = [-1, -1]
get_pos_enemy_ship = True
my_turn = False
game_running = True
enemy_ready = False

class Block:
    def __init__(self, rect, color, size):
        self.rect = rect
        self.color = color
        self.size = size
        self.ship_in_block = False
        self.alive = 0

    def change(self):
        if self.color == config.BLACK:
            self.color = config.BLUE
            self.size = 3
            self.ship_in_block = True
            self.alive = 3

        elif self.color == config.BLUE:
            self.color = config.BLACK
            self.size = 1
            self.ship_in_block = False
            self.alive = 0

    def attack(self):
        self.alive = 1


list_rects_mine = [[], [], [], [], [], [], [], [], [], []]
list_rects_enemy = [[], [], [], [], [], [], [], [], [], []]


for i in range(10):
    for j in range(10):
        list_rects_mine[i].append(Block(pygame.Rect((50 + i * 30, 50 + j * 30, 30, 30)), config.BLACK, 1))
        list_rects_enemy[i].append(Block(pygame.Rect((450 + i * 30, 50 + j * 30, 30, 30)), config.BLACK, 1))


def draw_grid():
    font_size = 25
    font = pygame.font.SysFont('arrial', font_size)
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, list_rects_mine[i][j].color, list_rects_mine[i][j], list_rects_mine[i][j].size)
            pygame.draw.rect(screen, list_rects_enemy[i][j].color, list_rects_enemy[i][j], list_rects_enemy[i][j].size)

            if list_rects_enemy[i][j].alive == 1:
                pygame.draw.line(screen, config.BLUE, [450 + i * 30, 50 + j * 30],
                                 [450 + (i + 1) * 30, 50 + (j + 1) * 30], 3)
                pygame.draw.line(screen, config.BLUE, [450 + (i + 1) * 30, 50 + j * 30],
                                 [450 + i * 30, 50 + (j + 1) * 30], 3)
            elif list_rects_enemy[i][j].alive == 2:
                pygame.draw.circle(screen, config.BLUE, [465 + i * 30, 65 + j * 30], 3)

            if list_rects_mine[i][j].alive == 1:
                pygame.draw.line(screen, config.BLUE, [50 + i * 30, 50 + j * 30],
                                 [50 + (i + 1) * 30, 50 + (j + 1) * 30], 3)
                pygame.draw.line(screen, config.BLUE, [50 + (i + 1) * 30, 50 + j * 30],
                                 [50 + i * 30, 50 + (j + 1) * 30], 3)
            elif list_rects_mine[i][j].alive == 2:
                pygame.draw.circle(screen, config.BLUE, [65 + i * 30, 65 + j * 30], 3)


    for ii in range(10):
        number = font.render(numbers[ii], True, config.BLACK)
        letter = font.render(letters[ii], True, config.BLACK)
        screen.blit(number, (55 + ii * 30, 30))
        screen.blit(number, (455 + ii * 30, 30))
        screen.blit(letter, (30, 55 + ii * 30))
        screen.blit(letter, (430, 55 + ii * 30))


class Button:
    def __init__(self, text, color):
        self.color = color
        self.text = text

    def render(self, x, y, font):
        self.surf = font.render(self.text, True, self.color)
        self.pos = (x, y)
        self.rect = self.surf.get_rect(topleft=self.pos)
        return self.surf, self.pos


def game(running, enemy_port, s, turn):
    global game_running
    game_running = True
    s = s
    sendto = ('127.0.0.1', enemy_port)
    font = pygame.font.SysFont('Arial', 30)
    ready_button = [Button("Я готов", config.BLUE), False]
    leave_button = [Button("Я сдаюсь", config.BLUE), False]
    rasstanovka_korabley = True
    global list_rects_mine, list_rects_enemy, my_turn, enemy_ready
    list_rects_mine = [[], [], [], [], [], [], [], [], [], []]
    list_rects_enemy = [[], [], [], [], [], [], [], [], [], []]
    for i in range(10):
        for j in range(10):
            list_rects_mine[i].append(Block(pygame.Rect((50 + i * 30, 50 + j * 30, 30, 30)), config.BLACK, 1))
            list_rects_enemy[i].append(Block(pygame.Rect((450 + i * 30, 50 + j * 30, 30, 30)), config.BLACK, 1))
    my_turn = turn
    last_hit = [pos_ships_enemy_attack[0], pos_ships_enemy_attack[1]]

    while running:
        screen.fill(config.WHITE)
        clock.tick(config.FPS)
        pos_mouse = pygame.mouse.get_pos()
        if rasstanovka_korabley and enemy_ready:
            screen.blit(font.render('Враг готов', True, config.BLACK), (200, 400))
        screen.blit(leave_button[0].render(100, 500, font)[0], leave_button[0].render(100, 500, font)[1])
        if my_turn:
            screen.blit(font.render('Мой ход', True, config.BLACK), (100, 450))
        else:
            screen.blit(font.render('Ход врага', True, config.BLACK), (100, 450))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.sendto('__youwin'.encode('ascii'), sendto)
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rasstanovka_korabley:
                    if ready_button[0].__dict__['rect'].collidepoint(pos_mouse):
                        rasstanovka_korabley = False
                        enemy_ready = False
                        s.sendto('__iamready'.encode('ascii'), sendto)
                        ready_button.clear()
                if leave_button[0].__dict__['rect'].collidepoint(pos_mouse):
                    s.sendto('__youwin'.encode('ascii'), sendto)
                    running = False
                if rasstanovka_korabley:
                    for i in range(10):
                        for j in range(10):
                            if list_rects_mine[i][j].rect.collidepoint(pos_mouse):
                                list_rects_mine[i][j].change()

                if not rasstanovka_korabley:
                    if my_turn:
                        for i in range(10):
                            for j in range(10):
                                if list_rects_enemy[i][j].rect.collidepoint(pos_mouse):
                                    s.sendto(f'__attack {i}{j}'.encode('ascii'), sendto)
                                    pos_ships_mine_attack[0] = i
                                    pos_ships_mine_attack[1] = j

        if pos_ships_enemy_attack != last_hit:
            if list_rects_mine[pos_ships_enemy_attack[0]][pos_ships_enemy_attack[1]].ship_in_block:
                list_rects_mine[pos_ships_enemy_attack[0]][pos_ships_enemy_attack[1]].alive = 1
                last_hit[0] = pos_ships_enemy_attack[0]
                last_hit[1] = pos_ships_enemy_attack[1]
                ships_around = 0
                if pos_ships_enemy_attack[0] != 0:
                    if list_rects_mine[pos_ships_enemy_attack[0] - 1][
                        pos_ships_enemy_attack[1]].alive == 3:
                        ships_around += 1
                if pos_ships_enemy_attack[0] != 9:
                    if list_rects_mine[pos_ships_enemy_attack[0] + 1][
                        pos_ships_enemy_attack[1]].alive == 3:
                        ships_around += 1
                if pos_ships_enemy_attack[1] != 0:
                    if list_rects_mine[pos_ships_enemy_attack[0]][
                        pos_ships_enemy_attack[1] - 1].alive == 3:
                        ships_around += 1
                if pos_ships_enemy_attack[1] != 9:
                    if list_rects_mine[pos_ships_enemy_attack[0]][
                        pos_ships_enemy_attack[1] + 1].alive == 3:
                        ships_around += 1

                if ships_around == 0:
                    s.sendto(f'__youkillme'.encode('ascii'), sendto)
                else:
                    s.sendto(f'__yougotme'.encode('ascii'), sendto)
            else:
                s.sendto(f'__miss'.encode('ascii'), sendto)
                list_rects_mine[pos_ships_enemy_attack[0]][pos_ships_enemy_attack[1]].alive = 2
                s.sendto(f'__change'.encode('ascii'), sendto)
                last_hit[0] = pos_ships_enemy_attack[0]
                last_hit[1] = pos_ships_enemy_attack[1]
                my_turn = True

        if len(ready_button) != 0:
            screen.blit(ready_button[0].render(100, 400, font)[0], ready_button[0].render(100, 400, font)[1])
            if ready_button[0].__dict__['rect'].collidepoint(pos_mouse):
                ready_button[0].__dict__['color'] = config.GREEN
            else:
                ready_button[0].__dict__['color'] = config.BLUE

        if leave_button[0].__dict__['rect'].collidepoint(pos_mouse):
            leave_button[0].__dict__['color'] = config.GREEN
        else:
            leave_button[0].__dict__['color'] = config.BLUE


        if not game_running:
            print('Я выиграл')
            running = False
        draw_grid()
        pygame.display.update()
