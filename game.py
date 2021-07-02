import pygame
import random

pygame.init()

display_height = 800
display_width = 800
game_over = 0
FPS = 60

background = pygame.image.load("libraries/images/background2.jpg")
restart_img = pygame.image.load("libraries/images/restart_btn.png")
restart_img = pygame.transform.scale(restart_img, (50, 50))

screen = pygame.display.set_mode((display_height, display_width))
pygame.display.set_caption("JB's platformer")

clock = pygame.time.Clock()


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        fly_cooldown = 5

        if game_over == 0:

            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False:
                self.vel_y = - 15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT] and self.rect.x > self.vel_x:
                dx -= 5
                self.direction = -1
            if key[pygame.K_RIGHT] and self.rect.x < display_width - 65:
                dx += 5
                self.direction = 1

            # handle animation
            self.counter += 1
            if self.counter > fly_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            if pygame.sprite.spritecollide(self, walls_group, False):
                game_over = -1

            # check for collision
            if pygame.sprite.spritecollide(self, ground_group, False):
                game_over = -1

            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 50:
                self.rect.y -= 5

        # Draw bird onto sccreen
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 6):
            img_right = pygame.image.load(f'libraries/images/felpudoVoa{num}.png')
            img_right = pygame.transform.scale(img_right, (75, 75))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('libraries/images/skull.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (50, 50))
        self.image = self.images_right[self.index]
        self.img = self.image
        self.img_flipped = pygame.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_x = 0
        self.vel_y = 0
        self.jumped = False
        self.direction = 0


class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("libraries/images/wall.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect.move(self.rect.width, 0))

        self.rect.move_ip(-2, 0)
        if self.rect.right == 0:
            self.rect.x = 800
            # self.kill()


class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("libraries/images/Piso.png")
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image, self.rect.move(self.rect.width, 0))

        self.rect.move_ip(-2, 0)
        if self.rect.right == -10:
            self.rect.x = 0


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


bird = Bird(100, 300)
ground = Ground(0, 710)

walls = Walls(random.randint(50, 600), random.randint(60, 650))
walls2 = Walls(random.randint(50, 600), random.randint(60, 650))
walls3 = Walls(random.randint(50, 600), random.randint(60, 650))
walls4 = Walls(random.randint(50, 600), random.randint(60, 650))

walls_group = pygame.sprite.Group()
walls_group.add(walls, walls2, walls3, walls4)
ground_group = pygame.sprite.Group()
ground_group.add(ground)

restart_button = Button(display_width // 2 - 50, display_height // 2 - 100, restart_img)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(background, (0, 0))

    if game_over == 0:
        ground.update()
        walls_group.update()
        ground_group.update()

    walls_group.draw(screen)

    game_over = bird.update(game_over)

    if game_over == -1:
        if restart_button.draw():
            bird.reset(200, 400)
            game_over = 0

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
