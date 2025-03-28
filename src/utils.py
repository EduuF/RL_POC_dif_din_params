import pygame
import random
import numpy as np
from typing import List, Dict
from dotenv import load_dotenv
import os
import random

from params import FOV_PLAYER

from Player.player import Player
from Boss.boss import Boss
from Minions.minion_arqueiro import Minion_arqueiro
from Minions.minion_guerreiro import Minion_guerreiro
from Traps.stun_trap import Stun_trap
from Traps.debuff_trap import Debuff_trap


load_dotenv()

# Definições básicas
GRID_SIZE = int(os.getenv('GRID_SIZE'))
CELL_SIZE = int(os.getenv('CELL_SIZE'))
INFO_PANEL_WIDTH = int(os.getenv('INFO_PANEL_WIDTH'))
LEGEND_PANEL_HEIGHT = int(os.getenv('LEGEND_PANEL_HEIGHT'))
GRID_WIDTH, GRID_HEIGHT = GRID_SIZE * CELL_SIZE + INFO_PANEL_WIDTH, GRID_SIZE * CELL_SIZE + LEGEND_PANEL_HEIGHT


def draw_shape(surface, shape, color, x, y, size, element_id=None, font=None):
    if shape == "circle":
        pygame.draw.circle(surface, color, (x + size // 2, y + size // 2), size // 2)
    elif shape == "triangle":
        #pygame.draw.polygon(surface, color, [(x + size // 2, y), (x, y + size), (x + size, y + size)])
        if element_id is not None and isinstance(element_id, int):  # Verifica se element é um número
            text_surface = font.render(str(element_id), True, color)
            text_rect = text_surface.get_rect(center=(x + size // 2, y + size // 2))
            surface.blit(text_surface, text_rect)
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
        if isinstance(grid[new_x][new_y], int) and grid[new_x][new_y] == 0:
            grid[player_pos[0]][player_pos[1]] = 0
            player_pos = (new_x, new_y)
            grid[new_x][new_y] = player
        elif grid[new_x][new_y].type in [5, 6]:
            grid[player_pos[0]][player_pos[1]] = 0
            player_pos = (new_x, new_y)
            grid = handle_traps(new_x, new_y, grid, player)
            grid[new_x][new_y] = player

    player.pos = player_pos


    return grid

def handle_traps(x: int, y: int, grid: np.ndarray, player: Player):
    if grid[x][y].type == 5:
        player.apply_debuff()
    elif grid[x][y].type == 6:
        player.apply_stun()
    return grid


def move_enemies(grid: np.ndarray, player: Player):
    px, py = player.pos

    for ex in range(max(0, px - FOV_PLAYER), min(GRID_SIZE, px + FOV_PLAYER + 1)):
        for ey in range(max(0, py - FOV_PLAYER), min(GRID_SIZE, py + FOV_PLAYER + 1)):
            # Verifica se a distância de Manhattan está dentro do FOV
            current_dist = abs(ex - px) + abs(ey - py) # Manhattan
            if current_dist > FOV_PLAYER or current_dist == 1:
                continue

            # Se a célula estiver vazia, não há inimigo para mover
            if grid[ex][ey] == 0:
                continue

            if random.random() < max(0, (player.Velocidade - 1)):
                continue

            enemy = grid[ex][ey]

            # **Movimento do Guerreiro (enemy.type == 3)**
            if hasattr(enemy, "type") and enemy.type == 3:
                temp_ex, temp_ey = ex, ey
                realizou_movimento = False

                if ex < px and ex + 1 < GRID_SIZE and grid[ex + 1][ey] == 0:
                    temp_ex = ex + 1
                    realizou_movimento = True
                elif ex > px and ex - 1 >= 0 and grid[ex - 1][ey] == 0:
                    temp_ex = ex - 1
                    realizou_movimento = True

                if ey < py and ey + 1 < GRID_SIZE and grid[ex][ey + 1] == 0 and not realizou_movimento:
                    temp_ey = ey + 1
                elif ey > py and ey - 1 >= 0 and grid[ex][ey - 1] == 0 and not realizou_movimento:
                    temp_ey = ey - 1

                # Atualiza o grid apenas se houver movimento válido
                if (temp_ex, temp_ey) != (ex, ey):
                    enemy.pos = (temp_ex, temp_ey)
                    grid[temp_ex][temp_ey] = enemy
                    grid[ex][ey] = 0

            # **Movimento do Inimigo que mantém distância (enemy.type == 2)**
            elif hasattr(enemy, "type") and enemy.type == 2:
                target_distance = max(1, FOV_PLAYER - 2)

                best_move = (ex, ey)
                min_diff = float('inf')

                # Lista de direções possíveis (Cima, Baixo, Esquerda, Direita)
                directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

                for dx, dy in directions:
                    nx, ny = ex + dx, ey + dy

                    # Garante que o movimento está dentro dos limites do grid e a célula está livre
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == 0:
                        new_distance = abs(nx - px) + abs(ny - py)
                        diff = abs(new_distance - target_distance)

                        # Se encontrar um movimento que mantém exatamente a distância alvo, prioriza esse
                        if diff == 0:
                            best_move = (nx, ny)
                            break

                        # Caso contrário, escolhe o movimento que minimiza a diferença para a distância alvo
                        if diff < min_diff:
                            min_diff = diff
                            best_move = (nx, ny)

                # Atualiza a posição do inimigo no grid
                new_ex, new_ey = best_move
                if (new_ex, new_ey) != (ex, ey):
                    enemy.pos = (new_ex, new_ey)
                    grid[new_ex][new_ey] = enemy
                    grid[ex][ey] = 0

    return grid



    # Decide o movimento na direção do player
