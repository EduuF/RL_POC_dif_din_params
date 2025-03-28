import pygame
import numpy as np

import os

from Player.player import Player
from Boss.boss import Boss
from params import SAFE_ZONE_RADIUS, NUM_MINION_ARQUEIRO, NUM_MINION_GUERREIRO, NUM_TRAP_DEBUFF, NUM_TRAP_STUN, STUN_TURNS, DEBUFF_TURNS
from utils import find_places_randomly, move_player, place_elements_on_board, move_enemies
from grid.utils import draw_grid
from Minions.minion_arqueiro import Minion_arqueiro
from Minions.minion_guerreiro import Minion_guerreiro
from Traps.stun_trap import Stun_trap
from Traps.debuff_trap import Debuff_trap
from combat.utils import search_fight

# Definições básicas
GRID_SIZE = int(os.getenv('GRID_SIZE'))
CELL_SIZE = int(os.getenv('CELL_SIZE'))
INFO_PANEL_WIDTH = int(os.getenv('INFO_PANEL_WIDTH'))
LEGEND_PANEL_HEIGHT = int(os.getenv('LEGEND_PANEL_HEIGHT'))
GRID_WIDTH, GRID_HEIGHT = GRID_SIZE * CELL_SIZE + INFO_PANEL_WIDTH, GRID_SIZE * CELL_SIZE + LEGEND_PANEL_HEIGHT

# Iniciando o objeto Player e Boss
player = Player()
boss = Boss(GRID_SIZE)

# Inicializa pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Inicializa o grid
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Posiciona o player e o boss
player_start_pos = player.pos
boss_start_pos = boss.pos
grid[player_start_pos[0]][player_start_pos[1]] = player
grid[boss_start_pos[0]][boss_start_pos[1]] = boss

# Inimigos
enemies = {}
traps = {}

enemies_id_counter = 0
traps_id_counter = 0

# Posiciona minions Arqueiros
arqueiros_positions = find_places_randomly(2, NUM_MINION_ARQUEIRO, GRID_SIZE, SAFE_ZONE_RADIUS, grid)
for position_tuple in arqueiros_positions:
    enemies[enemies_id_counter] = (Minion_arqueiro(enemies_id_counter, position_tuple))
    enemies_id_counter += 1

# Posiciona Minions guerreiros
guerreiros_positions = find_places_randomly(3, NUM_MINION_GUERREIRO, GRID_SIZE, SAFE_ZONE_RADIUS, grid)
for position_tuple in guerreiros_positions:
    enemies[enemies_id_counter] = (Minion_guerreiro(enemies_id_counter, position_tuple))
    enemies_id_counter += 1

# Posiciona Debuff Traps
debuff_positions = find_places_randomly(5, NUM_TRAP_DEBUFF, GRID_SIZE, SAFE_ZONE_RADIUS, grid)
for position_tuple in debuff_positions:
    traps[traps_id_counter] = (Debuff_trap(traps_id_counter, position_tuple))
    traps_id_counter += 1

# Posiciona Stun Traps
stun_positions = find_places_randomly(6, NUM_TRAP_STUN, GRID_SIZE, SAFE_ZONE_RADIUS, grid)
for position_tuple in stun_positions:
    traps[traps_id_counter] = (Stun_trap(traps_id_counter, position_tuple))
    traps_id_counter += 1

grid = place_elements_on_board(grid, player, boss, enemies, traps)
print(f'grid: {grid}')

for key, item in enemies.items():
    print(f'Tipo: {item.type} | Pos: {item.pos}')

for key, item in traps.items():
    print(f'Tipo: {item.type} | Pos: {item.pos}')

# Variáveis de monitoramento
turn_count = 0
potions_used = 0
time_taken = 0


running = True
while running:
    # Desenha o grid
    draw_grid(screen, player.get_player_status(), grid, font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif player.is_stuned():
                player.stun_countdown()
            elif event.key == pygame.K_UP:
                grid = move_player(0, -1, grid, player)
            elif event.key == pygame.K_DOWN:
                grid = move_player(0, 1, grid, player)
            elif event.key == pygame.K_LEFT:
                grid = move_player(-1, 0, grid, player)
            elif event.key == pygame.K_RIGHT:
                grid = move_player(1, 0, grid, player)



            grid = move_enemies(grid, player)
            grid = search_fight(grid, player)




            print(f'stun_turns_left | debuff_turns_left | turn_count {player.get_stun_turns_left()} | {player.get_debuff_turns_left()} | {turn_count}')

            turn_count += 1
            player.debuff_countdown()

    clock.tick(10)
pygame.quit()
