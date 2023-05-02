import pygame
from settings import *
from agents import *
import random
import math
import time

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(SCREEN_TITLE)

# Create a clock object
clock = pygame.time.Clock()

# Add the separate_agents function here
def separate_agents(agent_list1, agent_list2, min_distance):
    for agent1 in agent_list1:
        for agent2 in agent_list2:
            if agent1 != agent2:
                distance = math.sqrt((agent1.x - agent2.x) ** 2 + (agent1.y - agent2.y) ** 2)
                if distance < min_distance:
                    # Calculate the direction vector from agent1 to agent2
                    # Add 1e-9 to avoid division by zero
                    direction_x = (agent2.x - agent1.x) / (distance + 1e-9)
                    direction_y = (agent2.y - agent1.y) / (distance + 1e-9)

                    # Calculate the overlap between the agents
                    overlap = min_distance - distance

                    # Move the agents away from each other by half of the overlap
                    agent1.x -= direction_x * (overlap / 2)
                    agent1.y -= direction_y * (overlap / 2)
                    agent2.x += direction_x * (overlap / 2)
                    agent2.y += direction_y * (overlap / 2)


#Sprite lists
humanlist = []
zombielist = []
projectilelist = []



# Create a human sprite list
for human in range(NUMBER_OF_HUMANS):
    human = Human(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), ORANGE, HUMAN_SPEED)
    humanlist.append(human)

# Create a zombie sprite list
for zombie in range(NUMBER_OF_ZOMBIES):
    zombie = Zombie(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), GREEN, ZOMBIE_SPEED)
    zombielist.append(zombie)

#Create armed humans and add them to the sprite list
for armed_human in range(NUMBER_OF_ARMED_HUMANS):
    armed_human = ArmedHuman(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), ORANGE, HUMAN_SPEED)
    humanlist.append(armed_human)

def game_loop():
    #Variables are global so they will be displayed on the console outside the game loop
    global friendlyfiredeaths
    friendlyfiredeaths = 0
    global zombiedeaths
    zombiedeaths = 0
    global zombifiedhumans
    zombifiedhumans = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



        humans_to_remove = []
        zombies_to_add = []
        zombies_to_remove = []
        projectiles_to_remove = []

        #Human behavior loop
        for human in humanlist:
            if isinstance(human, ArmedHuman):
                human.shoot(zombielist, projectilelist)

            if human.alive:
                human.move(zombielist)
                #Handle human zombie collisions
                for zombie in zombielist:
                    if zombie.alive and human.collide(zombie):
                        zombies_to_add.append(human.become_zombie())
                        humans_to_remove.append(human)
                        zombifiedhumans += 1


            else:
                humans_to_remove.append(human)

        #Zombie behavior loop
        for zombie in zombielist:
            if zombie.alive:
                zombie.move(humanlist)
                #Handle zombie human collisions
                #Zombies infect humans using the become_zombie method
                for human in humanlist:
                    if human.alive and zombie.collide(human):
                        zombies_to_add.append(human.become_zombie())
                        humans_to_remove.append(human)
                        zombifiedhumans += 1
                
            else:
                zombies_to_add.append(zombie)

        #Projectile behavior loop
        projectiles_to_remove = []
        for projectile in projectilelist:
            if projectile.alive:
                projectile.move()
                #Handle projectile zombie collisions
                for zombie in zombielist:
                    if zombie.alive and projectile.collide(zombie):
                        zombies_to_remove.append(zombie)
                        projectiles_to_remove.append(projectile)
                        zombie.die()
                        zombiedeaths += 1
                #Handle projectile human collisions
                #Armed humans are immune to friendly fire
                for human in humanlist:
                    if not isinstance(human, ArmedHuman):
                        if human.alive and projectile.collide(human):
                            humans_to_remove.append(human)
                            projectiles_to_remove.append(projectile)
                            human.die()
                            friendlyfiredeaths += 1
                    

            else:
                projectiles_to_remove.append(projectile)

        #Remove dead agents from the sprite lists
        #If statement is in place to prevent the program from crashing
        for human in humans_to_remove:
            if human in humanlist:
                humanlist.remove(human)

        #Add new agents to the sprite lists
        for zombie in zombies_to_add:
            if zombie not in zombielist:
                zombielist.append(zombie)

        #Remove dead agents from the sprite lists
        for zombie in zombies_to_remove:
            if zombie in zombielist:
                zombielist.remove(zombie)

        #Remove dead agents from the sprite lists
        for projectile in projectiles_to_remove:
            if projectile in projectilelist:
                projectilelist.remove(projectile)
        
        #Separate agents that are too close to each other
        separate_agents(humanlist, humanlist, 25)
        separate_agents(zombielist, zombielist, 20)

        #Draw the agents on the screen
        screen.fill(BLACK)
        for human in humanlist:
            if human.alive:
                human.draw(screen)

        for zombie in zombielist:
            if zombie.alive:
                zombie.draw(screen)

        for projectile in projectilelist:
            if projectile.alive:
                projectile.draw(screen)
                                

        #Display zombie and friendly fire deaths on the screen
        font = pygame.font.Font(None, 36)
        text1 = font.render("Zombified humans: " + str(zombifiedhumans), 1, WHITE)
        text2 = font.render("Friendly fire deaths: " + str(friendlyfiredeaths), 1, WHITE)
        text3 = font.render("Zombie deaths: " + str(zombiedeaths), 1, WHITE)
        screen.blit(text1, (10, 10))
        screen.blit(text2, (10, 30))
        screen.blit(text3, (10, 50))

        #Display the winner on the screen
        if len(humanlist) == 0:
            text4 = font.render("Zombies win", 1, WHITE)
            screen.blit(text4, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 50))
        elif len(zombielist) == 0:
            text5 = font.render("Humans win", 1, WHITE)
            screen.blit(text5, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 50))





        #Update the screen
        pygame.display.flip()
        clock.tick(60)

# Run the game loop
if __name__ == "__main__":
    game_loop()
    if len(humanlist) == 0:
        print("Zombies win")
    else:
        print("Humans win")
    print("Zombified humans: " + str(zombifiedhumans))
    print("Friendly fire deaths: " + str(friendlyfiredeaths))
    print("Zombie deaths: " + str(zombiedeaths))

# quit pygame
pygame.quit()
