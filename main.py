import pygame
import random
import math
from npc import *
from settings import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

humans = [Human(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), RED) for _ in range(NUM_HUMANS)]
zombies = [Zombie(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(NUM_ZOMBIES)]
zombie_group = ZombieGroup(zombies)
player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

#set background to black
screen.fill((255, 255, 255))

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update():
    for human in humans:
        if human.alive:
            human.move(screen)
            human.run(screen, zombies)
            human.become_zombie(screen)
    zombie_group.update()
    player.move(screen)
    for zombie in zombies:
        if math.sqrt((player.x - zombie.x)**2 + (player.y - zombie.y)**2) < 20:
            player.infection += 1
            if player.infection >= 100:
                player.color = GREEN
                player.speed = 3
                player.infection = 100
        zombie.draw()
    for human in humans:
        if human.alive:
            human.draw(screen)
    player.draw(screen)
    zombie_group.set_target(player)
    player.kill_zombies(screen, zombies)
    return True

def main():
    running = True
    while running:
        running = handle_events()
        screen.fill((255, 255, 255))
        if not update():
            break
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
