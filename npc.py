from settings import *
import pygame
import random
import math

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class NPC:
    humans = []
    zombies = []

class Person:
    def __init__(self, x, y, color, health=100, speed=1, alive=True, infection=0):
        self.x = x
        self.y = y
        self.color = color
        self.health = health
        self.speed = speed
        self.alive = alive
        self.infection = infection

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

    def move(self, screen):
        self.x += random.randint(-self.speed, self.speed)
        self.y += random.randint(-self.speed, self.speed)
        if self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
        if self.x < 0:
            self.x = 0
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
        if self.y < 0:
            self.y = 0

class Human(Person):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

        self.color = RED

    def run(self, screen, zombies):
        for zombie in zombies:
            if math.sqrt((self.x - zombie.x)**2 + (self.y - zombie.y)**2) < 20:
                self.x -= zombie.x - self.x
                self.y -= zombie.y - self.y
    
    def become_zombie(self, screen):
        if self.infection >= 100:
            self.color = GREEN
            self.speed = 3
            self.infection = 100

    

class Zombie(NPC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = .1
        self.target = None
        self.color = GREEN

    def set_target(self, human):
        self.target = human

    def move_towards_target(self):
        if self.target is None:
            return
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > self.speed:
            self.x += dx/dist * self.speed
            self.y += dy/dist * self.speed
        else:
            self.x = self.target.x
            self.y = self.target.y
            self.target.infect()

    def draw(self):
        pygame.draw.circle(screen, (self.color), (int(self.x), int(self.y)), 10)

class ZombieGroup(NPC):
    def __init__(self, zombies):
        self.zombies = zombies
        self.target = None

    def set_target(self, human):
        self.target = human
        for zombie in self.zombies:
            zombie.set_target(human)

    def update(self):
        if self.target is None or self.target.infected or not self.target.alive:
            self.target = self.get_new_target()
            for zombie in self.zombies:
                zombie.set_target(self.target)
        for zombie in self.zombies:
            zombie.move_towards_target()

    def get_new_target(self):
        possible_targets = list(filter(lambda human: not human.infected and human.alive, self.humans))
        if len(possible_targets) == 0:
            return None
        return random.choice(possible_targets)



class Player:
    def __init__(self, x, y):
        self.speed = 2
        self.infection = 0
        self.color = BLUE
        self.x = x
        self.y = y
        self.infected = False
        self.alive = False

    


    def move(self, screen):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        self.x += dx
        self.y += dy
        if self.x > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH
        if self.x < 0:
            self.x = 0
        if self.y > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT
        if self.y < 0:
            self.y = 0

    def infect(self, human):
        if human.infection < 100:
            human.infection += 1
            if human.infection >= 100:
                human.color = GREEN
                human.speed = 3
                human.infection = 100

    def kill_zombies(self, screen, zombies):
        for zombie in zombies:
            if math.sqrt((self.x - zombie.x)**2 + (self.y - zombie.y)**2) < 20:
                zombies.remove(zombie)
                break
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)
