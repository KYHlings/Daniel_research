import pygame
from image import get_player_sprite, get_background_image, get_mob_sprite, get_mob_sprite2

pygame.init()


class Player(object):
    def __init__(self, player_x, player_y, width, height):
        self.player_x = player_x
        self.player_y = player_y
        self.width = width
        self.height = height
        self.velocity = 2


class Mob(object):
    def __init__(self,mob_x, mob_y, width, height):
        self.mob_x = mob_x
        self.mob_y = mob_y
        self.width = width
        self.height = height
        self.velocity = 5


def main():
    animal = Player(400,570,40,30)
    vehicle = Mob(0, 350, 80,40)
    vehicle2 = Mob(0, 450, 80,40)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drunk Frogger")
    running = True

    while running:
        screen.blit(get_background_image(), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        vehicle.mob_x += vehicle.velocity
        vehicle2.mob_x += vehicle.velocity
        if vehicle.mob_x and vehicle2.mob_x == 720:
            vehicle.mob_x = 0
            vehicle2.mob_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and animal.player_x > animal.velocity:
            animal.player_x -= animal.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and animal.player_x < 800 - 40 - animal.velocity:
            animal.player_x += animal.velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and animal.player_y < 600 - 30 - animal.velocity:
            animal.player_y += animal.velocity
        if keys[pygame.K_UP] or keys[pygame.K_w] and animal.player_y > animal.velocity:
            animal.player_y -= animal.velocity
        if keys[pygame.K_ESCAPE]:
            running = False

        screen.blit(get_mob_sprite(),(vehicle.mob_x,vehicle.mob_y))
        screen.blit(get_mob_sprite2(),(vehicle2.mob_x,vehicle2.mob_y))
        screen.blit(get_player_sprite(), (animal.player_x, animal.player_y))
        pygame.display.update()


if __name__ == '__main__':
    main()
