import pygame
import time
import random
import sys

pygame.init()
pygame.font.init()
scale_factor=0.8

scr_info=pygame.display.Info()
scr_width=scr_info.current_w
scr_height=scr_info.current_h

WIDTH, HEIGHT = int(scr_width*scale_factor),int(scr_height*scale_factor)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DON'T EAT THE BOMB!!!")

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 10
FOOD_WIDTH = 10
FOOD_HEIGHT = 20
FOOD_VEL = 5.5

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, count, foods, bombs):
    WIN.blit(BG, (0, 0))

    score = FONT.render(f"SCORE: "+str(count), 1, "white")
    WIN.blit(score, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for food in foods:
        pygame.draw.rect(WIN, "white", food)

    for bomb in bombs:
        pygame.draw.rect(WIN, "black", bomb)

    pygame.display.update()


def main():
    count=0
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()

    hit = False

    food_add_increment = 2000
    food_count = 0

    bomb_add_increment=3000
    bomb_count=0

    foods = []
    bombs=[]

    while run:
        food_count += clock.tick(60)
        bomb_count+=clock.tick(60)

        if food_count > food_add_increment:
            n=random.randint(1,6)
            for _ in range(n):
                food_x = random.randint(0, WIDTH - FOOD_WIDTH)
                food = pygame.Rect(food_x, -FOOD_HEIGHT,
                                   FOOD_WIDTH, FOOD_HEIGHT)
                foods.append(food)

            food_add_increment = max(100, food_add_increment - 50)
            food_count = 0

            if bomb_count > bomb_add_increment:
                n = random.randint(1, 3)
                for _ in range(n):
                    bomb_x = random.randint(0, WIDTH - FOOD_WIDTH)
                    bomb = pygame.Rect(bomb_x, -FOOD_HEIGHT,
                                       FOOD_WIDTH, FOOD_HEIGHT)
                    bombs.append(bomb)

                bomb_add_increment = max(200, bomb_add_increment - 50)
                bomb_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for food in foods[:]:
            food.y += FOOD_VEL
            if food.y > HEIGHT:
                foods.remove(food)
            elif food.y + food.height >= player.y and food.colliderect(player):
                foods.remove(food)
                count += 1

        for bomb in bombs[:]:
            bomb.y += FOOD_VEL
            if bomb.y > HEIGHT:
                bombs.remove(bomb)
            elif bomb.y + food.height >= player.y and bomb.colliderect(player):
                bombs.remove(bomb)
                hit = True
                break

        if hit:
            lost_Text=FONT.render("GAME OVER!!! YOUR SCORE: "+str(count),1,"red")
            WIN.blit(lost_Text,(WIDTH/2 - lost_Text.get_width()/2,HEIGHT/2 - lost_Text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2500)
            break

        draw(player, count, foods, bombs)

    pygame.quit()


if __name__ == "__main__":
    main()