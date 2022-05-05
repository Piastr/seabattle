import random
import socket
import threading
import pygame
import config
from second_player import game_second_player


def listen(s: socket.socket, host: str, port: int, members_on_server, game_on):
    while True:
        msg, addr = s.recvfrom(4096)
        msg_port = addr[-1]
        msg = msg.decode('ascii')
        allowed_ports = threading.currentThread().allowed_ports
        if msg_port not in allowed_ports:
            continue

        if not msg:
            continue

        if '__' in msg:
            command, content = msg.split('__')
            if command == 'members':
                members_on_server.clear()
                for n, member in enumerate(content.split(';'), start=1):
                    print('\r\r' + f'{n}) {member}', end='\n')
                    if member not in members_on_server:
                        # [имя, предложили ли он вам сыграть]
                        user = [member, False]
                        members_on_server.append(user)

        if msg.startswith('__inwait'):
            contect = msg.split(' ')[-1]
            who = 'client' + contect
            for i in members_on_server:
                if who == i[0]:
                    i[1] = True

        if msg == '__iamready':
            game_second_player.enemy_ready_test = True

        if msg.startswith('__hi'):
            port_name = msg.split(' ')[-1]
            print(f'hi from client{port_name}')

        if msg.startswith('__ok'):
            game_on[0] = True
            enemy_port = msg.split(' ')[-1]
            game_on[1] = enemy_port
            print(enemy_port)

        if msg == '__change':
            game_second_player.my_turn_test = False

        if msg == '__yougotme':
            game_second_player.list_rects_enemy_test[game_second_player.pos_ships_mine_attack_test[0]][
                                                game_second_player.pos_ships_mine_attack_test[1]].alive = 1

        if msg == '__youkillme':
            game_second_player.list_rects_enemy_test[game_second_player.pos_ships_mine_attack_test[0]][
                game_second_player.pos_ships_mine_attack_test[1]].change()
            game_second_player.list_rects_enemy_test[game_second_player.pos_ships_mine_attack_test[0]][
                game_second_player.pos_ships_mine_attack_test[1]].alive = 1

        if msg == '__miss':
            game_second_player.list_rects_enemy_test[game_second_player.pos_ships_mine_attack_test[0]][
                                                game_second_player.pos_ships_mine_attack_test[1]].alive = 2

        if msg.startswith('__attack'):
            pos = msg.split(' ')[-1]
            i = pos[0]
            j = pos[1]
            game_second_player.pos_ships_enemy_attack_test[0] = int(i)
            game_second_player.pos_ships_enemy_attack_test[1] = int(j)

        if msg.startswith('__ready'):
            contect = msg[8:]
            game_second_player.get_pos_enemy_ship_test = True

        if msg == '__youwin':
            game_second_player.game_running_test = False

        if msg.startswith('__no'):
            contect = msg.split(' ')[-1]
            who = 'client' + contect
            for i in members_on_server:
                if who == i[0]:
                    i[1] = False

def start_listen(target, socket, host, port, members_on_server, game_on):
    th = threading.Thread(target=target, args=(socket, host, port, members_on_server, game_on), daemon=True)
    th.start()
    return th


class Button:
    def __init__(self, text, color):
        self.color = color
        self.text = text

    def render(self, x, y, font):
        self.surf = font.render(self.text, True, self.color)
        self.pos = (x, y)
        self.rect = self.surf.get_rect(topleft=self.pos)
        return self.surf, self.pos


def multiplayer_menu(running, host, port):
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("test2")
    clock = pygame.time.Clock()
    pygame.display.update()
    font = pygame.font.SysFont('Arial', 25)
    static_text = ["Ваше имя", "Список игроков"]
    interactive_text = ["Назад", "Обновить"]
    buttons = [Button(interactive_text[i], config.WHITE) for i in range(len(interactive_text))]
    own_port = random.randint(3000, 4000)
    game_on = [False, 2000, False]
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, own_port))
    members_on_server = []
    listen_thread = start_listen(listen, s, host, port, members_on_server, game_on)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    sendto = (host, port)
    s.sendto('__join'.encode('ascii'), sendto)
    go_button = []
    ok_button = []
    no_button = []
    current_members = []
    pygame.display.update()

    while running:

        clock.tick(config.FPS)
        screen.fill(config.BLACK)
        pos_mouse = pygame.mouse.get_pos()

        # отрисовка кнопок и надписей
        screen.blit(buttons[0].render(20, 10, font)[0], buttons[0].render(20, 10, font)[1])
        screen.blit(font.render(static_text[0], True, config.BLUE), (20, 250))
        screen.blit(font.render(f'client{own_port}', True, config.GREEN), (20, 290))
        screen.blit(buttons[1].render(300, 10, font)[0], buttons[1].render(300, 10, font)[1])
        screen.blit(font.render(static_text[1], True, config.BLUE), (450, 10))

        if len(members_on_server) == 0:
            screen.blit(font.render('На сервере никого', True, config.BLUE), (400, 50))
        else:
            memb_butt = [Button(members_on_server[i][0], config.WHITE) for i in range(len(members_on_server))]
            if members_on_server != current_members:
                go_button = [Button('Go?', config.WHITE) for i in range(len(members_on_server))]
                ok_button = [Button('OK', config.BLACK) for i in range(len(members_on_server))]
                no_button = [Button('NO', config.BLACK) for i in range(len(members_on_server))]

            for i in range(len(memb_butt)):
                screen.blit(memb_butt[i].render(525, 50 + i * 50, font)[0],
                            memb_butt[i].render(525, 50 + i * 50, font)[1])
                screen.blit(go_button[i].render(300, 50 + i * 50, font)[0],
                            memb_butt[i].render(300, 50 + i * 50, font)[1])
                screen.blit(ok_button[i].render(375, 50 + i * 50, font)[0],
                            ok_button[i].render(375, 50 + i * 50, font)[1])
                screen.blit(no_button[i].render(450, 50 + i * 50, font)[0],
                            no_button[i].render(450, 50 + i * 50, font)[1])
                current_members = members_on_server

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                s.sendto('__exit'.encode('ascii'), sendto)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(buttons)):
                    if buttons[i].__dict__['rect'].collidepoint(pos_mouse):
                        if buttons[i].__dict__['text'] == interactive_text[i]:
                            x = interactive_text[i]
                            if x == 'Назад':
                                running = False
                                s.sendto('__exit'.encode('ascii'), sendto)
                            if x == 'Обновить':
                                s.sendto('__members'.encode('ascii'), sendto)
                                pass

                for i in range(len(members_on_server)):
                    if go_button[i].__dict__['rect'].collidepoint(pos_mouse):
                        s.sendto(f'__inwait {members_on_server[i][0]}'.encode('ascii'), sendto)
                        print(f'__inwait {members_on_server[i][0]}')
                    if no_button[i].__dict__['rect'].collidepoint(pos_mouse):
                        s.sendto(f'__no {members_on_server[i][0]}'.encode('ascii'), sendto)
                        members_on_server[i][1] = False
                        for i in range(len(ok_button)):
                            ok_button[i].__dict__['color'] = config.BLACK
                            no_button[i].__dict__['color'] = config.BLACK
                    if ok_button[i].__dict__['rect'].collidepoint(pos_mouse):
                        s.sendto(f'__ok {members_on_server[i][0]}'.encode('ascii'), sendto)
                        game_on[0] = True
                        game_on[1] = members_on_server[i][0][-4:]
                        game_on[2] = True

        for i in buttons:
            if i.__dict__['rect'].collidepoint(pos_mouse):
                i.__dict__['color'] = config.GREEN
                pygame.display.update()
            else:
                i.__dict__['color'] = config.WHITE
                pygame.display.update()

            for i in go_button:
                if i.__dict__['rect'].collidepoint(pos_mouse):
                    i.__dict__['color'] = config.GREEN
                    pygame.display.update()
                else:
                    i.__dict__['color'] = config.WHITE
                    pygame.display.update()

            for i in range(len(ok_button)):
                if members_on_server[i][1]:
                    if ok_button[i].__dict__['rect'].collidepoint(pos_mouse):
                        ok_button[i].__dict__['color'] = config.GREEN
                        pygame.display.update()
                    else:
                        ok_button[i].__dict__['color'] = config.WHITE
                        pygame.display.update()

                    if no_button[i].__dict__['rect'].collidepoint(pos_mouse):
                        no_button[i].__dict__['color'] = config.RED
                        pygame.display.update()
                    else:
                        no_button[i].__dict__['color'] = config.WHITE
                        pygame.display.update()
        if game_on[0]:
            allowed_ports.append(int(game_on[1]))
            print(game_on[1])
            game_on[0] = game_second_player.game(True, int(game_on[1]), s, game_on[2])


if __name__ == '__main__':
    multiplayer_menu(True, '127.0.0.1', 2000)

