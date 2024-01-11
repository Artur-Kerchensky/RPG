import pygame
from config.config import cell_size, NUM_OF_CELLS_CHUNK


class Creature:
    def __init__(self, name, start_pos, hp, speed=1, attack=0, defense=0):
        self.name = name
        self.x, self.y = start_pos[0], start_pos[1]
        self.hp, self.max_hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense if defense < 0 else None
        self.pos_table = [0.5 * NUM_OF_CELLS_CHUNK * cell_size] * 2

    def move(self, direction):
        print(self.pos_table)
        directions = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        if direction in directions:
            direct_x, direct_y = directions[direction]
            self.x += self.speed * direct_x
            self.y += self.speed * direct_y
            self.pos_table[0] += self.speed * direct_x
            self.pos_table[1] += self.speed * direct_y

    def take_damage(self, damage):
        self.hp -= damage * self.defense * 0.01
        if self.hp <= 0:
            self.speed = 0

    def render(self):
        pass

    def get_pos(self):
        return self.x, self.y

    def get_pos_table(self):
        return self.pos_table

    def change_pos(self, pos):
        if pos is not None:
            self.pos_table = pos


class Player(Creature):
    def __init__(self, start_pos, hp, speed=cell_size, attack=5, defense=0,  level=1, experience=0, attributes=(1, 1, 1)):
        Creature.__init__(self, 'Player', start_pos, hp, speed, attack, defense)
        self.level = level
        self.experience = experience
        self.attributes = {'strength': attributes[0], 'agility': attributes[1], 'intelligence': attributes[2]}

    def level_up(self, attribute):
        if self.experience >= 100:
            self.experience -= 100
            self.level += 1
            self.attributes[attribute] += 1

    def gain_experience(self, exp):
        self.experience += exp

    def update(self, screen):
        pygame.draw.rect(screen, pygame.Color('red'), (NUM_OF_CELLS_CHUNK // 2 * cell_size,
                                                       cell_size * NUM_OF_CELLS_CHUNK // 2,
                                                       cell_size, cell_size))
