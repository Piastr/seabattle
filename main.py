import pygame
import config
import multiplayer_menu


def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('Arial', 25)
    font_zagl = pygame.font.SysFont('Arial', 50)
    text_menu = ["Сетевая игра", "Выход"]
    menu_butts = [multiplayer_menu.Button(text_menu[i], config.WHITE) for i in range(len(text_menu))]
    background = pygame.image.load('images/sea.png')
    background_rect = background.get_rect(topleft=(0,0))

    in_menu = True
    while in_menu:
        clock.tick(config.FPS)
        screen.fill(config.BLACK)
        screen.blit(background, background_rect)
        pos_mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(len(menu_butts)):
                    if menu_butts[i].__dict__['rect'].collidepoint(pos_mouse):
                        if menu_butts[i].__dict__['text'] == text_menu[i]:
                            x = text_menu[i]
                            print(x)
                            if x == 'Сетевая игра':
                                multiplayer_menu.multiplayer_menu(True, '127.0.0.1', 2000)
                            if x == 'Выход':
                                in_menu = False
        screen.blit(font_zagl.render('Морской бой', True, config.BLUE), (250, 50))
        for i in range(len(menu_butts)):
            screen.blit(menu_butts[i].render(150, 200 + i * 80, font)[0], menu_butts[i].render(150, 200 + i * 80, font)[1])

        for i in menu_butts:
            if i.__dict__['rect'].collidepoint(pos_mouse):
                i.__dict__['color'] = config.GREEN
                pygame.display.update()
            else:
                i.__dict__['color'] = config.WHITE
                pygame.display.update()


if __name__ == '__main__':
    main()

