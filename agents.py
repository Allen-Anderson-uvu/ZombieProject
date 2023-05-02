import pygame
from settings import *
import random
import math
import time
from abc import ABC, abstractmethod

#Define abstract class Agent
class Agent(ABC, pygame.sprite.Sprite):
    def __init__ (self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        
    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def collide(self, other):
        pass

    @abstractmethod
    def die(self):
        pass



#Define class Human
class Human(Agent):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, color, speed)

        self.color = ORANGE
        self.speed = HUMAN_SPEED
        self.set_new_destination()
        self.alive = True
        self.radius = 5
    
    #Part of the logic for human to die
    def die(self):
        self.alive = False

    #This method is not used currently.  It is here for future use.
    def set_new_destination(self):
        self.destination_x = random.randint(0, SCREEN_WIDTH)
        self.destination_y = random.randint(0, SCREEN_HEIGHT)

    #Draw the human
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

    #This is the logic that controls the movement of the human
    def move(self, zombielist):
        closest_zombie = None
        closest_distance = math.inf

        # Find the closest zombie
        for zombie in zombielist:
            if zombie.alive:
                distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_zombie = zombie

        # If there is a zombie, move away from it
        if closest_zombie is not None:
            direction_x = (self.x - closest_zombie.x) / closest_distance
            direction_y = (self.y - closest_zombie.y) / closest_distance

            self.x += direction_x * self.speed
            self.y += direction_y * self.speed

            # Keep the human within the screen bounds
            self.x = max(10, min(self.x, SCREEN_WIDTH - 10))
            self.y = max(10, min(self.y, SCREEN_HEIGHT - 10))

    #This returns true if a human collides with another agent
    def collide(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

        if isinstance(other, Human):
            min_distance = 10  # Set the minimum distance between humans
            if distance < min_distance:
                return True

        elif isinstance(other, Projectile):
            if distance <= (self.radius + other.radius):
                return True

        elif isinstance(other, Zombie):
            if distance <= (self.radius + other.radius):
                return True

        return False

    #This is not currently used in the program.  It is here for future use.
    #I want to make the human behavior more complex and avoid getting stuck in corners.
    def human_behavior(self):
        self.move()
    
    #This creates a zombie, kills the human, and returns the zombie
    def become_zombie(self):
        zombie = Zombie(self.x, self.y, GREEN, ZOMBIE_SPEED)
        self.die()
        return zombie




class ArmedHuman(Human):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, color, speed)

        self.color = RED
        self.speed = ARMED_HUMAN_SPEED
        self.set_new_destination()
        self.alive = True
        self.shoot_cooldown = 0

    #This method allows armed humans to fire projectiles
    def shoot(self, zombielist, projectilelist):
        if self.shoot_cooldown <= 0:
            closest_zombie = None
            closest_distance = math.inf

            # Find the closest zombie
            for zombie in zombielist:
                if zombie.alive:
                    distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_zombie = zombie

            # If there is a zombie, shoot at it
            #Will not fire from more than half the screen width away
            if closest_zombie is not None and closest_distance <= SCREEN_WIDTH * 0.5:
                direction_x = (closest_zombie.x - self.x) / closest_distance
                direction_y = (closest_zombie.y - self.y) / closest_distance

                projectile = Projectile(self.x, self.y, WHITE, PROJECTILE_SPEED, direction_x, direction_y)
                projectilelist.append(projectile)

                self.shoot_cooldown = 60  # Reset the shoot cooldown (60 frames or 1 second)

        else:
            self.shoot_cooldown -= 1

    #This method moves the armed human towards zombies
    #Armed humans maintain a buffer distance between themselves and zombies to prevent infection
    def move(self, zombielist):
        closest_zombie = None
        closest_distance = math.inf

        for zombie in zombielist:
            if zombie.alive:
                distance = math.sqrt((self.x - zombie.x) ** 2 + (self.y - zombie.y) ** 2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_zombie = zombie

        if closest_zombie is not None:
            buffer_distance = 100  # Distance to maintain from zombies

            if closest_distance > buffer_distance:
                # Move towards the zombie
                direction_x = (closest_zombie.x - self.x) / closest_distance
                direction_y = (closest_zombie.y - self.y) / closest_distance
            else:
                # Move away from the zombie
                direction_x = (self.x - closest_zombie.x) / closest_distance
                direction_y = (self.y - closest_zombie.y) / closest_distance

            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
            self.x = max(10, min(self.x, SCREEN_WIDTH - 10))
            self.y = max(10, min(self.y, SCREEN_HEIGHT - 10))




#Define class Zombie
class Zombie(Agent):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, color, speed)

        self.color = GREEN
        self.speed = ZOMBIE_SPEED
        self.alive = True
        self.radius = 5

    #This method kills the zombie
    def die(self):
        self.alive = False

    #This method draws the zombie
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5)

    #This method moves the zombie towards humans
    def move(self, humanlist):
            closest_human = None
            closest_distance = math.inf

            for human in humanlist:
                if human.alive:
                    distance = math.sqrt((self.x - human.x) ** 2 + (self.y - human.y) ** 2)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_human = human

            if closest_human is not None:
                direction_x = (closest_human.x - self.x) / closest_distance
                direction_y = (closest_human.y - self.y) / closest_distance

                self.x += direction_x * self.speed
                self.y += direction_y * self.speed

                # Keep the zombie within the screen bounds
                self.x = max(10, min(self.x, SCREEN_WIDTH - 10))
                self.y = max(10, min(self.y, SCREEN_HEIGHT - 10))


    #This method checks if the zombie has collided with a human
    def collide(self, other):
        distance = math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        if isinstance(other, Human):
            if distance <= (self.radius + other.radius):
                return True
        return False
    
    #This method is not used, but I have not removed it because I intend to make zombie behavior more complex
    def zombie_behavior(self, humanlist):
        self.move(humanlist)

#Define class Projectile
class Projectile:
    def __init__(self, x, y, color, speed, direction_x, direction_y):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.alive = True

    #This method draws the projectile
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)

    #This method moves the projectile
    def move(self):
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y < 0 or self.y > SCREEN_HEIGHT:
            self.alive = False
    
    #This method checks if the projectile has collided with a zombie or human
    def collide(self, shotobject):
        distance = math.sqrt((self.x - shotobject.x) ** 2 + (self.y - shotobject.y) ** 2)
        if isinstance(shotobject, Zombie):
            if distance <= 5:
                return True
        elif isinstance(shotobject, Human):
            if distance <= 5:
                return True
            
        return False