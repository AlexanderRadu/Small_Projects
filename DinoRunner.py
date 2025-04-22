#DinoRunner game
import pygame
import os
import random

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dino Runner')

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

DEAD = pygame.image.load(os.path.join("Assets/Dino", "DinoDead.png"))
DINO_START = pygame.image.load(os.path.join("Assets/Dino", "DinoStart.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

JUMP_SOUND = pygame.mixer.Sound("Assets/Music/Jump Sound.mp3")
DEATH_SOUND = pygame.mixer.Sound("Assets/Music/Death sound.mp3")
HUNDRED_SOUND = pygame.mixer.Sound("Assets/Music/Hundred riched sound.mp3")

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

GAME_OVER = pygame.image.load(os.path.join("Assets/Other", "GameOver.png"))

RESET_BUTTON = pygame.image.load(os.path.join("Assets/Other", "Reset.png"))

MOVEMENT_VELOCITY = 8.5

score_font = pygame.font.SysFont("comicsansms", 35)


class Dinosaur:
    ANIMATION_TIME = 5 * 2
    dino_start_image = DINO_START
    dino_dead_image = DEAD

    def __init__(self):
        self.image_count = 0
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.ducking = False
        self.running = True
        self.jumping = False
        self.vertical_speed = 18
        self.image = self.run_img[0]
        self.x = 80
        self.y = 485

    def jump(self):
        self.image = self.jump_img
        self.y -= self.vertical_speed
        self.vertical_speed -= 0.8
        if self.vertical_speed == 0:
            self.vertical_speed += 0.8
            self.y += self.vertical_speed
        if self.y >= 485:
            self.y = 485
            self.jumping = False
            self.running = True
            self.ducking = False
            self.image_count = 0
            self.vertical_speed = 18

    def run(self):
        self.jumping = False
        self.running = True
        self.ducking = False
        self.image = self.run_img[0]

    def duck(self):
        self.jumping = False
        self.running = False
        self.ducking = True
        self.image = self.duck_img[0]

    def update_statement(self, user_input, user_mouse_input):
        if self.ducking:
            self.duck()
        if self.running:
            self.run()
        if self.jumping:
            self.jump()

        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.jumping and not user_input[pygame.K_DOWN]:
            self.ducking = False
            self.running = False
            self.jumping = True
            JUMP_SOUND.play()
        elif user_mouse_input[0] and not self.jumping and not user_input[pygame.K_DOWN]:
            self.ducking = False
            self.running = False
            self.jumping = True
            JUMP_SOUND.play()
        elif user_input[pygame.K_DOWN] and not self.jumping:
            self.ducking = True
            self.running = False
            self.jumping = False
        elif not (self.jumping or user_input[pygame.K_DOWN]):
            self.ducking = False
            self.running = True
            self.jumping = False
        elif user_input[pygame.K_DOWN] and self.jumping:
            self.vertical_speed -= 7

    def draw(self):
        self.image_count += 1
        if self.running:
            if self.image_count < self.ANIMATION_TIME:
                self.image = self.run_img[0]
            elif self.image_count < self.ANIMATION_TIME * 2:
                self.image = self.run_img[1]
            elif self.image_count < self.ANIMATION_TIME * 3 + 1:
                self.image = self.run_img[0]
                self.image_count = 0
            SCREEN.blit(self.image, (self.x, self.y))
        elif self.ducking:
            if self.image_count < self.ANIMATION_TIME:
                self.image = self.duck_img[0]
            elif self.image_count < self.ANIMATION_TIME * 2:
                self.image = self.duck_img[1]
            elif self.image_count < self.ANIMATION_TIME * 3 + 1:
                self.image = self.duck_img[0]
                self.image_count = 0
            SCREEN.blit(self.image, (self.x, self.y + 35))
        elif self.jumping:
            SCREEN.blit(self.image, (self.x, self.y))

    def get_ready(self):
        SCREEN.blit(self.dino_start_image, (self.x, self.y - 8))

    def dead(self, ax=0):
        SCREEN.blit(self.dino_dead_image, (self.x + ax, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image.convert_alpha())


class Obstacle:
    start_pos = SCREEN_WIDTH
    stop_pos = SCREEN_WIDTH + 250
    distance = 100

    def __init__(self, obstacle_images):
        self.obstacle_images = obstacle_images
        self.velocity = MOVEMENT_VELOCITY
        self.image = self.obstacle_images[0]
        self.x = self._generate_new_x()

    def _generate_new_x(self):
        new_x = random.randint(Obstacle.start_pos, Obstacle.stop_pos)
        Obstacle.start_pos = new_x + Obstacle.distance
        Obstacle.stop_pos = Obstacle.start_pos + Obstacle.distance * 3
        return new_x

    def move(self):
        self.x -= self.velocity
        if self.x <= -self.image.get_width():
            self.x = self._generate_new_x()
            self.image = random.choice(self.obstacle_images)

    def get_mask(self):
        return pygame.mask.from_surface(self.image.convert_alpha())


class SmallCactus(Obstacle):
    def __init__(self):
        super().__init__(SMALL_CACTUS)
        self.y = 572 - self.image.get_height()

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


class LargeCactus(Obstacle):
    def __init__(self):
        super().__init__(LARGE_CACTUS)
        self.y = 572 - self.image.get_height()

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


class Bird(Obstacle):
    ANIMATION_TIME = 8 * 2

    def __init__(self):
        super().__init__(BIRD)
        self.image_count = 0
        self.y = SCREEN_HEIGHT // 4 + random.randint(0, 270)

    def _generate_new_x(self):
        new_x = random.randint(Obstacle.start_pos, Obstacle.stop_pos)
        Obstacle.start_pos += Obstacle.distance
        Obstacle.stop_pos += Obstacle.distance
        return new_x

    def move(self):
        self.x -= self.velocity
        if self.x <= -self.image.get_width():
            self.x = self._generate_new_x()
            self.y = SCREEN_HEIGHT // 4 + random.randint(0, 270)

    def draw(self):
        self.image_count += 1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.obstacle_images[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.obstacle_images[1]
        elif self.image_count < self.ANIMATION_TIME * 3 + 1:
            self.image = self.obstacle_images[0]
            self.image_count = 0
        SCREEN.blit(self.image, (self.x, self.y))


class Base:
    def __init__(self):
        self.first_image = BG
        self.second_image = BG
        self.velocity = MOVEMENT_VELOCITY
        self.first_image_x = 0
        self.second_image_x = self.first_image.get_width()

    def move(self):
        self.first_image_x -= self.velocity
        self.second_image_x -= self.velocity
        if self.first_image_x <= -self.first_image.get_width():
            self.first_image_x = self.second_image_x + self.second_image.get_width()
        if self.second_image_x <= -self.second_image.get_width():
            self.second_image_x = self.first_image_x + self.first_image.get_width()

    def draw(self):
        SCREEN.blit(self.first_image, (self.first_image_x, SCREEN_HEIGHT - self.first_image.get_height() - 20))
        SCREEN.blit(self.second_image, (self.second_image_x, SCREEN_HEIGHT - self.second_image.get_height() - 20))


class Cloud:
    start_pos = SCREEN_WIDTH
    stop_pos = SCREEN_WIDTH + 550
    distance = 50

    def __init__(self):
        self.image = CLOUD
        self.velocity = MOVEMENT_VELOCITY
        self.x = self.generate_new_x()
        self.y = random.randint(75, 200)

    def move(self):
        self.x -= self.velocity // 2
        if self.x <= -self.image.get_width():
            self.x = self.generate_new_x()
            self.y = random.randint(75, 200)

    def generate_new_x(self):
        new_x = random.randint(Cloud.start_pos, Cloud.stop_pos)
        Cloud.stop_pos += Cloud.distance
        Cloud.start_pos += Cloud.distance
        return new_x

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))


class CollideObject:
    def __init__(self, image, x, y):
        self.rect = x, y
        self.mask = pygame.mask.from_surface(image.convert_alpha())


def display_score(score, x, y, text=''):
    score = score_font.render(f'{text}{score}', True, (0, 0, 0))
    SCREEN.blit(score, [x, y])


def update_movement_velocity(bird, base, small_cactus, large_cactus):
    epsilon = 0.002
    bird.velocity += epsilon
    small_cactus.velocity += epsilon
    large_cactus.velocity += epsilon
    base.velocity += epsilon
    #Obstacle.distance += 1


def collide(dino, *obstacles):
    dino_sprite = CollideObject(dino.image, dino.x, dino.y)
    for obstacle in obstacles:
        obstacle_sprite = CollideObject(obstacle.image, obstacle.x, obstacle.y)
        if pygame.sprite.collide_mask(dino_sprite, obstacle_sprite):
            return True
    return False


def main(run, highest_score):
    score = 0
    is_dead = False

    base = Base()
    dino = Dinosaur()
    clouds = [Cloud(), Cloud(), Cloud(), Cloud()]
    small_cactus = SmallCactus()
    large_cactus = LargeCactus()
    bird = Bird()

    while not run:
        SCREEN.fill((255, 255, 255))
        dino.get_ready()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_SPACE):
                    run = True
                    dino.jump()
                    JUMP_SOUND.play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    run = True
                    dino.jump()
                    JUMP_SOUND.play()
        pygame.display.update()

    while run:
        SCREEN.fill((255, 255, 255))
        user_input = pygame.key.get_pressed()
        user_mouse_input = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        dino.update_statement(user_input, user_mouse_input)
        for cloud in clouds:
            cloud.move()
            cloud.draw()

        if score > 350:
            bird.move()
            bird.draw()

        large_cactus.move()
        small_cactus.move()
        large_cactus.draw()
        small_cactus.draw()

        base.move()
        base.draw()
        dino.draw()

        if collide(dino, small_cactus, large_cactus, bird):
            run = False
            is_dead = True
            highest_score = max(score, highest_score)
            DEATH_SOUND.play()

        score += 0.125
        if score % 100 == 0:
            HUNDRED_SOUND.play()

        display_score(int(score), 0, 0)
        display_score(int(highest_score), 0, 30, text='HI  ')
        update_movement_velocity(bird=bird, base=base, small_cactus=small_cactus, large_cactus=large_cactus)
        pygame.display.update()
        pygame.time.Clock().tick(120)

    while is_dead:
        SCREEN.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_SPACE):
                    main(True, highest_score)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    main(True, highest_score)

        SCREEN.blit(GAME_OVER, (360, 260))
        SCREEN.blit(RESET_BUTTON, (510, 300))
        base.draw()
        large_cactus.draw()
        small_cactus.draw()
        bird.draw()
        for cloud in clouds:
            cloud.draw()
        if dino.ducking:
            dino.dead(ax=25)
        else:
            dino.dead()
        display_score(int(score), 0, 0)
        display_score(int(highest_score), 0, 30, text='HI  ')
        pygame.display.update()


main(run=False, highest_score=0)
