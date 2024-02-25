import pygame
import random
from collections import deque

from configuration import cell_size, NUM_OF_CELLS_CHUNK, load_image
from database import Base

num_id = -1


class Object:
    def __init__(self, name, group_sprites):
        global num_id
        self.id = num_id
        self.name = name

        self.sprites = group_sprites
        num_id += 1

    def get_id(self):
        return self.id


class Creature(Object):
    def __init__(self, name, start_pos, hp, group_sprites=None, speed=1, attack=0, defense=0):
        #  group_sprites потом поменять во всех дочерних классах
        Object.__init__(self, name, group_sprites)
        self.x, self.y = start_pos[0], start_pos[1]
        self.hp, self.max_hp = hp
        self.speed = speed
        self.attack = attack
        self.defense = defense if defense < 0 else None

    def move(self, direction):
        directions = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        if direction in directions:
            direct_x, direct_y = directions[direction]
            self.x += direct_x
            self.y += direct_y

    def take_damage(self, damage):
        self.hp -= damage * self.defense * 0.01
        if self.hp <= 0:
            self.speed = 0

    def get_pos(self):
        return self.x, self.y


class Item(Object):
    def __init__(self, name, group_sprites=None):
        #  group_sprites потом поменять
        Object.__init__(self, name, group_sprites)


class Player(Creature):
    def __init__(self, start_pos, hp, speed=cell_size, attack=5, defense=0,
                 level=1, experience=0, attributes=(1, 1, 1)):
        Creature.__init__(self, 'Player', start_pos, hp, speed, attack, defense)
        self.level = level
        self.experience = experience
        self.attributes = {'strength': attributes[0], 'agility': attributes[1], 'intelligence': attributes[2]}
        self.walk = {"West": [load_image(f"walk_left{i}.png", "anims/player") for i in range(1, 5)],
                     "East": [load_image(f"walk_right{i}.png", "anims/player") for i in range(1, 5)],
                     "North": [load_image(f"walk_up{i}.png", "anims/player") for i in range(1, 5)],
                     "South": [load_image(f"walk_down{i}.png", "anims/player") for i in range(1, 5)]}
        self.player_anim_count = 0

    def level_up(self, attribute):
        if self.experience >= 100:
            self.experience -= 100
            self.level += 1
            self.attributes[attribute] += 1

    def gain_experience(self, exp):
        self.experience += exp

    def update(self, screen, direction):
        if direction in self.walk.keys():
            self.player_anim_count = (self.player_anim_count + 1) % 4

    def render(self, screen, direction):
        x = y = (NUM_OF_CELLS_CHUNK // 2 * cell_size -
                 NUM_OF_CELLS_CHUNK * cell_size % NUM_OF_CELLS_CHUNK // 2 * cell_size)
        screen.blit(self.walk[direction][self.player_anim_count], (x + (0.1 * cell_size), y - (0.4 * cell_size)))


class Enemy(Creature):
    def __init__(self, name, start_pos, hp, giv_exp, speed=cell_size // 2, attack=5, defense=0):
        Creature.__init__(self, name, start_pos, hp, speed, attack, defense)
        self.giv_exp = giv_exp
        self.path = []
        self.frees = False  # Проверка появления на суше
        self.walk = load_image(f"{self.name.lower()}_idle.png", f"anims/{self.name.lower()}")

    def pathfinding(self, pos, chart):
        self.path = finding_path((self.x, self.y), pos, chart.get_graph(), chart.get_start_chunks())
        if not self.path:
            self.path = [' ']

    def examination(self, chart):
        x, y = chart.get_coord(self.x, self.y)
        try:
            while chart.get_board()[y][x] < 3:
                    x, y = chart.get_coord(self.x, self.y)
                    direct = random.randint(0, 1)
                    if direct:
                        self.x += (-1 if x > int(NUM_OF_CELLS_CHUNK * 1.5) else 1)
                    else:
                        self.y += (-1 if x > int(NUM_OF_CELLS_CHUNK * 1.5) else 1)
        except IndexError:
            self.frees = True
        

    def update(self, screen, pos, chart, moving=False):
        #directions = {'North': (0, -1), 'South': (0, 1), 'East': (1, 0), 'West': (-1, 0)}
        if not self.frees:
            x, y = ((self.x - pos[0] + NUM_OF_CELLS_CHUNK // 2),
                    (self.y - pos[1] + NUM_OF_CELLS_CHUNK // 2))
            if moving:
                self.examination(chart)
                self.move()
            screen.blit(self.walk, (x * cell_size - (0.3 * cell_size), y * cell_size - (0.5 * cell_size)))
            self.pathfinding(pos, chart)

    def move(self, direction=None):
        if self.path:
            Creature.move(self, self.path.pop(0))
                    
    def __str__(self):
        return self.name, self.get_pos()


def random_enemy(list_pos):
    res = []
    bd = Base()
    enemy_list = bd.get_all_information('*', 'Enemy')
    enemies = [enemy_list[random.randint(0, len(enemy_list) - 1)] for _ in range(len(list_pos))]
    i = 0
    for enemy in enemies:
        res.append(Enemy(enemy[1], list_pos[i], (enemy[2], enemy[2]), enemy[3]))
        i += 1
    return res


def finding_path(start, end, graph, grid_start):

    def bfs(start, goal, graph):
        queue = deque([start])
        visited = {start: None}
        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            if graph.get(cur_node):
                next_nodes = graph[cur_node]
            else:
                next_nodes = []
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        path_head, path_segment = goal, goal
        res = []
        while path_segment and path_segment in visited:
            res.append(path_segment)
            path_segment = visited[path_segment]

        return res[-1:0:-1]

    def transformation(path):
        transcription = {(1, 0): 'West', (0, 1): 'North', (-1, 0): 'East', (0, -1): 'South'}
        res = []
        x, y = path[0]
        for i in range(1, len(path)):
            res.append(transcription[(x - path[i][0], y - path[i][1])])
            x, y = path[i][0], path[i][1]
        return res

    start = (start[0] - grid_start[0], start[1] - grid_start[1])
    end = (end[0] - grid_start[0], end[1] - grid_start[1])
    if all(abs(i) < NUM_OF_CELLS_CHUNK * 3 for i in start):
        path = bfs(start, end, graph)
        if path:
            return transformation(path)
        else:
            return False
    return False