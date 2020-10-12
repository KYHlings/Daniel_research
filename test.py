from random import randint
import pygame

from music_handler import get_level_music, get_goat_music, get_splat
from quiz_handler import get_quiz
from image_handler import get_player_sprite, get_background_image, get_mob_sprite, get_get_sprite

pygame.init()
screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()


class Player:
    def __init__(self, player_x, player_y, width, height, rotation):
        self.player_x = player_x
        self.player_y = player_y
        self.width = width
        self.height = height
        self.velocity = 4
        self.hitbox = (self.player_x + 2, self.player_y + 2, 36, 27)
        self.rotation = rotation

    def check_collide_x(self, mob):
        if self.player_x <= mob.mob_x:
            if self.player_x + self.width >= mob.mob_x:
                return True
            return False
        else:
            if mob.mob_x + mob.width >= self.player_x:
                return True
            return False

    def check_collide_y(self, mob):
        if self.player_y <= mob.mob_y:
            if self.player_y + self.height >= mob.mob_y:
                return True
            return False
        else:
            if mob.mob_y + mob.height >= self.player_y:
                return True
            return False

    def check_collide(self, mob):

        return self.check_collide_y(mob) and self.check_collide_x(mob)

    def reset(self):
        self.player_x = 400
        self.player_y = 570

    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a] and self.player_x > self.velocity:
            self.player_x -= self.velocity
            self.rotation = 90
            self.hitbox = (self.player_x + 2, self.player_y + 2, 27, 36)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.player_x < 800 - 40 - self.velocity:
            self.player_x += self.velocity
            self.rotation = 270
            self.hitbox = (self.player_x + 2, self.player_y + 2, 27, 36)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        if keys[pygame.K_UP] or keys[pygame.K_w] and self.player_y > self.velocity:
            self.player_y -= self.velocity
            self.rotation = 0
            self.hitbox = (self.player_x + 2, self.player_y + 2, 36, 27)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.player_y < 600 - 30 - self.velocity:
            self.rotation = 180
            self.player_y += self.velocity
            self.hitbox = (self.player_x + 2, self.player_y + 2, 36, 27)
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


class Mob:
    def __init__(self, mob_x, mob_y, width, height, image):
        self.mob_x = mob_x
        self.mob_y = mob_y
        self.image = image
        self.width = width
        self.height = height
        self.velocity = 7
        self.hitbox = (self.mob_x + 6, self.mob_y + 7, 69, 30)


class Get:
    def __init__(self, get_x, get_y, width, height):
        self.get_x = get_x
        self.get_y = get_y
        self.width = width
        self.height = height
        self.velocity = 4
        self.hitbox = (self.get_x + 6, self.get_y + 7, 69, 30)


def text_object(text, font):
    text_surface = font.render(text, True, (255, 255, 255))
    return text_surface, text_surface.get_rect()


def crash(text):
    run = True
    while run:
        message_window = pygame.Surface([400, 100])
        large_text = pygame.font.Font("freesansbold.ttf", 20)
        text_surf, text_rect = text_object(text, large_text)
        text_rect.center = (400, 300)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    run = False
                if event.key == pygame.K_n:
                    run = False
        screen.blit(message_window, (200, 250))
        screen.blit(text_surf, text_rect)
        screen.blit(get_get_sprite(), (200, 250))
        pygame.display.update()


def redraw_window(cars, animals, wise_goat):
    for car in cars:
        screen.blit(car.image, (car.mob_x, car.mob_y))
        car.hitbox = (car.mob_x + 6, car.mob_y + 7, 69, 30)
        pygame.draw.rect(screen, (255, 0, 0), car.hitbox, 3)
    screen.blit(get_player_sprite(animals.rotation), (animals.player_x, animals.player_y))
    screen.blit(get_get_sprite(), (animals.player_x - 20, wise_goat.get_y))
    pygame.display.update()


def main():
    get_level_music()
    animals = Player(400, 570, 40, 30, 0)
    cars = [Mob(0, 350, 80, 40, get_mob_sprite(False)), Mob(0, 400, 80, 40, get_mob_sprite(True)),
            Mob(0, 450, 80, 40, get_mob_sprite(False))]
    wise_goat = Get(animals.player_x, 200, 40, 30)
    pygame.display.set_caption("Drunk Frogger")
    running = True

    now = [pygame.time.get_ticks(), pygame.time.get_ticks(), pygame.time.get_ticks()]
    mob_spawn_timer = [1000, 2000, 1000]
    lanes = [350, 400, 450]
    q = False
    while running:
        clock.tick(30)
        screen.blit(get_background_image(), (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for car in cars[:]:
            if car.mob_y != 400:
                car.mob_x += car.velocity
                if car.mob_x >= 800:
                    cars.remove(car)
            else:
                car.mob_x -= car.velocity
                if car.mob_x <= -50:
                    cars.remove(car)
        for i in range(3):
            if pygame.time.get_ticks() - now[i] >= mob_spawn_timer[i]:
                if lanes[i] != 400:
                    cars.append(Mob(0, lanes[i], 80, 40, get_mob_sprite(False)))
                else:
                    cars.append(Mob(800, lanes[i], 80, 40, get_mob_sprite(True)))
                now[i] = pygame.time.get_ticks()
                mob_spawn_timer[i] = randint(1000, 2000)
        keys = pygame.key.get_pressed()
        animals.move(keys)
        if keys[pygame.K_ESCAPE]:
            running = False

        for car in cars:
            if animals.check_collide(car):
                get_splat()
                animals.reset()
        if animals.player_y <= 300 and q == False:
            get_goat_music()
            crash("Är T.O.A.D's bäst? y/n ")
            q = True
            get_level_music()
        redraw_window(cars, animals, wise_goat)


if __name__ == '__main__':
    main()
