import random
from tools import *

class Element:

    def __init__(self, pos, environment):
        self.pos = pos
        self.environment = environment

    def find_next_step(self, direction):
        if direction == N:
            return (self.pos[0] - 1, self.pos[1])
        elif direction == E:
            return (self.pos[0], self.pos[1] + 1)
        elif direction == S:
            return (self.pos[0] + 1, self.pos[1])
        elif direction == W:
            return (self.pos[0], self.pos[1] - 1)

    def step(self, next):
        self.environment[self.pos] = None
        self.pos = next
        self.environment[next] = self
        return True

class Dirty(Element):
    pass

class Playpen(Element):

    def __init__(self, pos, environment):
        Element.__init__(self, pos, environment)
        self.child = False

class Child(Element):

    def move(self):
        direction = random.randint(0, 4)
        if direction != STAY:
            next = self.find_next_step(direction)
            if self.environment.is_in(next) and next != self.environment.robot.pos:
                element = self.environment[next]
                if type(element) is Obstacle and element.move(direction):
                    self.step(next)
                elif element is None:
                    self.step(next)

class Obstacle(Element):

    def move(self, direction):
        next = self.find_next_step(direction)
        if self.environment.is_in(next):
            element = self.environment[next]

            if type(element) is Obstacle:
                return element.move(direction) and self.step(next)
            elif element is None:
                return self.step(next)
            return False

        return False
