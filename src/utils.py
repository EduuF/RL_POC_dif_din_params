import pygame
import random
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
import os

from configs import COLORS, SHAPES
from params import SAFE_ZONE_RADIUS, DEBUFF_PERCENTAGE, DEBUFF_TURNS, STUN_TURNS, NUM_MINION_ARQUEIRO, \
    NUM_MINION_GUERREIRO, NUM_MINION_MAGO, NUM_TRAP_DEBUFF, NUM_TRAP_STUN

from Player.player import Player
from Boss.boss import Boss
from Minions.minion_arqueiro import Minion_arqueiro
from Minions.minion_guerreiro import Minion_guerreiro
from Minions.minion_mago import Minion_mago
from Traps.stun_trap import Stun_trap
from Traps.debuff_trap import Debuff_trap


load_dotenv()

# Definições básicas
GRID_SIZE = int(os.getenv('GRID_SIZE'))
CELL_SIZE = int(os.getenv('CELL_SIZE'))
INFO_PANEL_WIDTH = int(os.getenv('INFO_PANEL_WIDTH'))
LEGEND_PANEL_HEIGHT = int(os.getenv('LEGEND_PANEL_HEIGHT'))
GRID_WIDTH, GRID_HEIGHT = GRID_SIZE * CELL_SIZE + INFO_PANEL_WIDTH, GRID_SIZE * CELL_SIZE + LEGEND_PANEL_HEIGHT


def draw_shape(surface, shape, color, x, y, size):
    if shape == "circle":
        pygame.draw.circle(surface, color, (x + size // 2, y + size // 2), size // 2)
    elif shape == "triangle":
        pygame.draw.polygon(surface, color, [(x + size // 2, y), (x, y + size), (x + size, y + size)])
    elif shape == "square":
        pygame.draw.rect(surface, color, (x, y, size, size))
    elif shape == "x":
        pygame.draw.line(surface, color, (x, y), (x + size, y + size), 3)
        pygame.draw.line(surface, color, (x + size, y), (x, y + size), 3)
    elif shape == "square_x":
        pygame.draw.rect(surface, color, (x, y, size, size), 2)
        pygame.draw.line(surface, color, (x, y), (x + size, y + size), 2)
        pygame.draw.line(surface, color, (x + size, y), (x, y + size), 2)


def is_safe_position(x: int, y: int, SAFE_ZONE_RADIUS: int):
    """
    Checa se auma determinada posição é valida para spawn de minions ou traps
    :param x: Coordenada X a verificar
    :param y: Coordenada Y a verificar
    :param SAFE_ZONE_RADIUS: Distância mínima do ponto de spawn do usuário (0,0)
    :return:
    """
    return x >= SAFE_ZONE_RADIUS or y >= SAFE_ZONE_RADIUS


def find_places_randomly(element_type: int, count: int, GRID_SIZE: int, SAFE_ZONE_RADIUS: int, grid: np.ndarray):
    """
    Posiciona elementos no grid
    :param entity: Tipo do elemento a ser posicionado
    :param count: Quantidade de elementos a serem posicionados
    :param GRID_SIZE: Tamanho do grid
    :param SAFE_ZONE_RADIUS: Distância segura do local de spawn do player
    :param grid: objeto grid
    """

    placed = 0
    positions = []
    while placed < count:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == 0 and is_safe_position(x, y, SAFE_ZONE_RADIUS):
            grid[x][y] = element_type
            positions.append((x,y))
            placed += 1
    return positions

def place_elements_on_board(grid: np.ndarray, player: Player, boss: Boss, enemies: Dict, traps: Dict):
    grid = place_player_on_board(grid, player)
    grid = place_boss_on_board(grid, boss)
    grid = place_enemies_on_board(grid, enemies)
    grid = place_traps_on_board(grid, traps)
    return grid

def place_player_on_board(grid: np.ndarray, player: Player):
    player_position = player.pos
    grid[player_position[0]][player_position[1]] = player
    return grid

def place_boss_on_board(grid: np.ndarray, boss: Boss):
    boss_position = boss.pos
    grid[boss_position[0]][boss_position[1]] = boss
    return grid

def place_enemies_on_board(grid: np.ndarray, enemies: Dict):
    for id, enemy in enemies.items():
        enemy_position = enemy.pos
        grid[enemy_position[0]][enemy_position[1]] = enemy
    return grid

def place_traps_on_board(grid: np.ndarray, traps: Dict):
    for id, trap in traps.items():
        enemy_position = trap.pos
        grid[enemy_position[0]][enemy_position[1]] = trap
    return grid


def move_player(dx: int, dy: int, grid: np.ndarray, player: Player):
    """
    Movimenta o player no grid
    :param dx: Movimentação no eixo X
    :param dy: Movimentação no eixo Y
    :param grid: Objeto Grid
    :param player_pos: Posição atual do player no grid
    :param stun_turns_left: Quantos turnos de stun o player ainda tem se houver
    :param turn_count: Contador de turnos
    :param player: Objeto do jogador
    """
    player_pos = player.pos

    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
        # Se a proxima posição for vazia
        print(f'grid[new_y][new_x]: {grid[new_y][new_x]}')
        if isinstance(grid[new_y][new_x], int) and grid[new_y][new_x] == 0:
            grid[player_pos[1]][player_pos[0]] = 0
            player_pos = (new_x, new_y)
            grid[new_y][new_x] = player
        elif grid[new_y][new_x].type in [5, 6]:
            grid[player_pos[1]][player_pos[0]] = 0
            player_pos = (new_x, new_y)
            grid = handle_traps(new_x, new_y, grid, player)
            grid[new_y][new_x] = player

    player.pos = player_pos


    return grid




def handle_traps(x: int, y: int, grid: np.ndarray, player: Player):
    if grid[y][x].type == 5:
        player.apply_debuff()
    elif grid[y][x].type == 6:
        player.apply_stun()
    return grid
