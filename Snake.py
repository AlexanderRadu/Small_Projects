import pygame
import random

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

width = 600
height = 400

block_size = 10
snake_speed = 10

pygame.init()

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Змейка')
Clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.x = width / 4
        self.y = height / 2
        self.x_change = 0
        self.y_change = 0
        self.snake_list = []
        self.snake_length = 1

    def move(self):
        self.x += self.x_change
        self.y += self.y_change

    def collide(self):
        if self.x <= 0 or self.x >= width or self.y <= 0 or self.y >= height:
            return True
        for snake_part in self.snake_list[:-1]:
            if snake_part == [self.x, self.y]:
                return True
        return False

    def grow(self):
        self.snake_length += 1

    def display_snake(self):
        for snake_part in self.snake_list:
            pygame.draw.rect(window, black, [snake_part[0], snake_part[1], block_size, block_size])


class Apple:
    def __init__(self):
        self.x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
        self.y = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    def draw(self):
        pygame.draw.rect(window, red, [self.x, self.y, block_size, block_size])


def display_score(score):
    score = score_font.render(f'Счёт: {str(score)}', True, yellow)
    window.blit(score, [0, 0])


def display_message():
    lost = font_style.render('Вы проиграли', True, red)
    action = font_style.render('Нажмите R для перезапуска, Q - для выхода', True, red)
    window.blit(lost, [width / 2.75, height / 3])
    window.blit(action, [width / 11.5, height / 2])


def main():
    run = True
    game_over = False
    snake = Snake()
    apple = Apple()
    score = 0
    

    while run:
        while game_over:
            window.fill(green)
            display_message()
            display_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit(0)
                    if event.key == pygame.K_r:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snake.x_change != block_size:
                        snake.x_change = -block_size
                        snake.y_change = 0
                elif event.key == pygame.K_RIGHT:
                    if snake.x_change != -block_size:
                        snake.x_change = block_size
                        snake.y_change = 0
                elif event.key == pygame.K_UP:
                    if snake.y_change != block_size:
                        snake.y_change = -block_size
                        snake.x_change = 0
                elif event.key == pygame.K_DOWN:
                    if snake.y_change != -block_size:
                        snake.y_change = block_size
                        snake.x_change = 0
                elif event.key == pygame.K_q:
                    exit(0)
        snake.move()

        window.fill(green)
        apple.draw()

        if snake.collide():
            game_over = True

        snake.snake_list.append([snake.x, snake.y])

        if len(snake.snake_list) > snake.snake_length:
            del snake.snake_list[0]

        snake.display_snake()
        display_score(score)
        pygame.display.update()

        if snake.x == apple.x and snake.y == apple.y:
            apple = Apple()
            snake.grow()
            score += 1
        Clock.tick(snake_speed)
    pygame.quit()
    quit()


main()
