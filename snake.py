import pygame
import time
import random

pygame.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 20
snake_speed = 10

# Font settings
font = pygame.font.SysFont("Arial", 25, bold=True)
score_font = pygame.font.SysFont("Arial", 30, bold=True)

high_score = 0

def show_score(score, high_score):
    score_text = score_font.render(f"Score: {score}", True, white)
    high_score_text = score_font.render(f"High Score: {high_score}", True, white)
    dis.blit(score_text, (10, 10))
    dis.blit(high_score_text, (dis_width - 200, 10))

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, red, [obs[0], obs[1], snake_block, snake_block])

def generate_obstacles():
    obstacles = []
    for _ in range(3):
        obs_x = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
        obs_y = round(random.randrange(50, dis_height - snake_block) / 20.0) * 20.0
        obstacles.append([obs_x, obs_y])
    return obstacles

def game_over_screen():
    dis.fill(black)
    game_over_text = score_font.render("Game Over!", True, white)
    dis.blit(game_over_text, (dis_width // 3, dis_height // 3))
    
    pygame.draw.rect(dis, white, [150, 250, 120, 40])
    pygame.draw.rect(dis, white, [330, 250, 120, 40])
    
    play_again_text = font.render("Play Again", True, black)
    quit_text = font.render("Quit", True, black)
    
    dis.blit(play_again_text, (160, 260))
    dis.blit(quit_text, (370, 260))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 150 <= x <= 270 and 250 <= y <= 290:
                    waiting = False
                elif 330 <= x <= 450 and 250 <= y <= 290:
                    pygame.quit()
                    quit()

def gameLoop():
    global high_score
    
    while True:  
        game_over = False
        score = 0

        x1, y1 = dis_width / 2, dis_height / 2
        x1_change, y1_change = 0, 0

        snake_List = []
        Length_of_snake = 1

        foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
        foody = round(random.randrange(50, dis_height - snake_block) / 20.0) * 20.0

        obstacles = generate_obstacles()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and x1_change == 0:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT and x1_change == 0:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP and y1_change == 0:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN and y1_change == 0:
                        y1_change = snake_block
                        x1_change = 0

            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_over = True
                break

            x1 += x1_change
            y1 += y1_change
            dis.fill(black)

            pygame.draw.rect(dis, blue, [foodx, foody, snake_block, snake_block])

            snake_Head = [x1, y1]
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]

            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_over = True
                    break

            draw_obstacles(obstacles)

            for obs in obstacles:
                if x1 == obs[0] and y1 == obs[1]:
                    game_over = True
                    break

            our_snake(snake_block, snake_List)
            show_score(score, high_score)

            pygame.display.update()

            if x1 == foodx and y1 == foody:
                foodx = round(random.randrange(0, dis_width - snake_block) / 20.0) * 20.0
                foody = round(random.randrange(50, dis_height - snake_block) / 20.0) * 20.0
                Length_of_snake += 1
                score += 1

                if score > high_score:
                    high_score = score

            clock.tick(snake_speed)

        game_over_screen()

gameLoop()
